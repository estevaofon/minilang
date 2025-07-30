#!/usr/bin/env python3
"""
MiniLang JIT Interpreter - Versão Corrigida
Com melhor suporte para printf no Windows

Uso:
    python interpreter_jit_fixed.py arquivo.ml
    python interpreter_jit_fixed.py arquivo.ml --debug
"""

import sys
import os
import ctypes
import struct
import llvmlite.binding as llvm
from pathlib import Path

# Importar o compilador existente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from compiler import MiniLangCompiler

# Configurar saída UTF-8 no início
if sys.platform == "win32":
    # Configurar console do Windows
    os.system("chcp 65001 > nul 2>&1")
    # Configurar Python
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

class MiniLangJIT:
    """Interpretador JIT para MiniLang usando LLVM"""
    
    def __init__(self, debug=False):
        self.compiler = MiniLangCompiler()
        self.debug = debug
        self.external_functions = {}
        self.allocated_memory = []
        self._init_llvm()
        
    def _init_llvm(self):
        """Inicializa LLVM"""
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        # Criar target machine
        target = llvm.Target.from_default_triple()
        self.target_machine = target.create_target_machine()
        
        if self.debug:
            print(f"[DEBUG] Target: {self.target_machine.triple}")
    
    def _create_printf_wrapper(self):
        """Cria um wrapper robusto para printf"""
        if sys.platform == "win32":
            libc = ctypes.CDLL("msvcrt")
            kernel32 = ctypes.windll.kernel32
            
            # Configurar console
            kernel32.SetConsoleOutputCP(65001)
            
            # Cache para strings já impressas (debug)
            printed_strings = []
            
            @ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)
            def printf_wrapper(fmt):
                """Printf wrapper que garante output no Windows"""
                try:
                    if fmt is None:
                        return 0
                    
                    # Converter para string Python
                    if isinstance(fmt, int):
                        # Se fmt é um endereço, tentar ler como string
                        try:
                            text = ctypes.string_at(fmt).decode('utf-8', errors='replace')
                        except:
                            return 0
                    elif isinstance(fmt, bytes):
                        text = fmt.decode('utf-8', errors='replace')
                    else:
                        text = str(fmt)
                    
                    # Imprimir usando Python (mais confiável)
                    print(text, end='', flush=True)
                    
                    # Debug
                    if self.debug:
                        printed_strings.append(text)
                    
                    return len(text.encode('utf-8'))
                    
                except Exception as e:
                    if self.debug:
                        print(f"\n[DEBUG] Erro no printf: {e}")
                        print(f"[DEBUG] fmt type: {type(fmt)}, value: {fmt}")
                    return 0
            
            return printf_wrapper, printed_strings
        else:
            # Em Unix, usar printf normal
            libc = ctypes.CDLL(None)
            printf = libc.printf
            printf.argtypes = [ctypes.c_char_p]
            printf.restype = ctypes.c_int
            return printf, []
    
    def _create_builtin_functions(self):
        """Define todas as funções built-in necessárias"""
        
        # Printf especial
        printf, self.printed_strings = self._create_printf_wrapper()
        
        # Bibliotecas C
        if sys.platform == "win32":
            libc = ctypes.CDLL("msvcrt")
        else:
            libc = ctypes.CDLL(None)
        
        # malloc e free
        malloc = libc.malloc
        malloc.argtypes = [ctypes.c_size_t]
        malloc.restype = ctypes.c_void_p
        
        free = libc.free
        free.argtypes = [ctypes.c_void_p]
        free.restype = None
        
        # strlen
        strlen = libc.strlen
        strlen.argtypes = [ctypes.c_char_p]
        strlen.restype = ctypes.c_size_t
        
        # strcpy
        strcpy = libc.strcpy
        strcpy.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        strcpy.restype = ctypes.c_char_p
        
        # strcat
        strcat = libc.strcat
        strcat.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        strcat.restype = ctypes.c_char_p
        
        # sprintf
        sprintf = libc.sprintf
        sprintf.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        sprintf.restype = ctypes.c_int
        
        # Wrapper para malloc que rastreia alocações
        @ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_size_t)
        def malloc_wrapper(size):
            ptr = malloc(size)
            if ptr:
                self.allocated_memory.append(ptr)
            return ptr
        
        # to_str_int
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_longlong)
        def to_str_int(value):
            result = str(value).encode('utf-8')
            ptr = malloc_wrapper(len(result) + 1)
            if ptr:
                ctypes.memmove(ptr, result, len(result) + 1)
            return ptr
        
        # to_str_float
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_double)
        def to_str_float(value):
            result = f"{value:.6f}".encode('utf-8')
            ptr = malloc_wrapper(len(result) + 1)
            if ptr:
                ctypes.memmove(ptr, result, len(result) + 1)
            return ptr
        
        # array_to_str_int
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(ctypes.c_longlong), ctypes.c_longlong)
        def array_to_str_int(arr, size):
            try:
                if not arr or size <= 0:
                    result = b"[]"
                else:
                    elements = []
                    for i in range(size):
                        elements.append(str(arr[i]))
                    result = f"[{', '.join(elements)}]".encode('utf-8')
                
                ptr = malloc_wrapper(len(result) + 1)
                if ptr:
                    ctypes.memmove(ptr, result, len(result) + 1)
                return ptr
            except Exception as e:
                if self.debug:
                    print(f"\n[DEBUG] Erro em array_to_str_int: {e}")
                return malloc_wrapper(3)  # "[]"
        
        # array_to_str_float
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_longlong)
        def array_to_str_float(arr, size):
            try:
                if not arr or size <= 0:
                    result = b"[]"
                else:
                    elements = []
                    for i in range(size):
                        elements.append(f"{arr[i]:.6f}")
                    result = f"[{', '.join(elements)}]".encode('utf-8')
                
                ptr = malloc_wrapper(len(result) + 1)
                if ptr:
                    ctypes.memmove(ptr, result, len(result) + 1)
                return ptr
            except Exception as e:
                if self.debug:
                    print(f"\n[DEBUG] Erro em array_to_str_float: {e}")
                return malloc_wrapper(3)
        
        # to_int
        @ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_double)
        def to_int(value):
            return int(value)
        
        # to_float
        @ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_longlong)
        def to_float(value):
            return float(value)
        
        # fmod
        if sys.platform == "win32":
            fmod = libc.fmod
        else:
            libm = ctypes.CDLL("libm.so.6")
            fmod = libm.fmod
        fmod.argtypes = [ctypes.c_double, ctypes.c_double]
        fmod.restype = ctypes.c_double
        
        # SetConsoleOutputCP para Windows
        if sys.platform == "win32":
            kernel32 = ctypes.windll.kernel32
            SetConsoleOutputCP = kernel32.SetConsoleOutputCP
            SetConsoleOutputCP.argtypes = [ctypes.c_uint]
            SetConsoleOutputCP.restype = ctypes.c_bool
        else:
            SetConsoleOutputCP = None
        
        result = {
            'printf': printf,
            'malloc': malloc_wrapper,
            'free': free,
            'strlen': strlen,
            'strcpy': strcpy,
            'strcat': strcat,
            'sprintf': sprintf,
            'to_str_int': to_str_int,
            'to_str_float': to_str_float,
            'array_to_str_int': array_to_str_int,
            'array_to_str_float': array_to_str_float,
            'to_int': to_int,
            'to_float': to_float,
            'fmod': fmod
        }
        
        if SetConsoleOutputCP:
            result['SetConsoleOutputCP'] = SetConsoleOutputCP
            
        return result
    
    def execute(self, source: str) -> int:
        """Executa código MiniLang"""
        try:
            if self.debug:
                print("[DEBUG] Compilando código...")
            
            # Compilar para LLVM IR usando a nova abordagem
            llvm_ir = self._compile_with_casting_functions(source)
            
            if self.debug:
                print("[DEBUG] LLVM IR gerado com sucesso")
                print(f"[DEBUG] Tamanho do IR: {len(llvm_ir)} bytes")
            
            # Parsear LLVM IR
            try:
                mod = llvm.parse_assembly(llvm_ir)
                if self.debug:
                    print("[DEBUG] Módulo LLVM verificado")
            except Exception as e:
                print(f"Erro ao parsear LLVM IR: {e}")
                if self.debug:
                    print("[DEBUG] Primeiras linhas do IR:")
                    lines = llvm_ir.split('\n')[:20]
                    for line in lines:
                        print(f"  {line}")
                return 1
            
            # Criar JIT engine
            try:
                engine = llvm.create_mcjit_compiler(mod, self.target_machine)
                if self.debug:
                    print("[DEBUG] JIT engine criado e módulo adicionado")
                
                # Armazenar referência do engine para uso nos wrappers
                self._engine = engine
                
                # Linkar funções de casting
                self._link_functions(engine)
                
                # Executar main
                main_ptr = engine.get_function_address("main")
                if self.debug:
                    print(f"[DEBUG] Endereço da função main: {main_ptr}")
                if not main_ptr:
                    print("Erro: Função 'main' não encontrada")
                    if self.debug:
                        print("[DEBUG] Funções disponíveis no módulo:")
                        for func in mod.functions:
                            print(f"  - {func.name}")
                    return 1
                
                # Executar
                main_func = ctypes.CFUNCTYPE(ctypes.c_int)(main_ptr)
                try:
                    result = main_func()
                    if self.debug:
                        print(f"[DEBUG] Função main executada com sucesso, retorno: {result}")
                except Exception as e:
                    if self.debug:
                        print(f"[DEBUG] Erro durante execução da função main: {e}")
                        import traceback
                        traceback.print_exc()
                    result = 1
                
                # Flush após executar
                import sys
                sys.stdout.flush()
                
                return result
                
            except Exception as e:
                print(f"Erro durante execução: {e}")
                if self.debug:
                    import traceback
                    traceback.print_exc()
                return 1
                
        except Exception as e:
            print(f"Erro durante execução: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return 1
    
    def _link_functions(self, engine):
        """Linka funções externas pré-compiladas"""
        try:
            if self.debug:
                print("[DEBUG] Carregando funções de casting pré-compiladas...")
            
            # Compilar casting_functions.c para biblioteca compartilhada
            import subprocess
            import tempfile
            import os
            
            # Verificar se já existe a biblioteca compilada
            lib_name = "casting_functions.dll" if sys.platform == "win32" else "libcasting_functions.so"
            lib_path = os.path.join(os.getcwd(), lib_name)
            
            if not os.path.exists(lib_path):
                if self.debug:
                    print(f"[DEBUG] Compilando {lib_name}...")
                
                # Compilar casting_functions.c para biblioteca compartilhada
                if sys.platform == "win32":
                    cmd = ["gcc", "-shared", "-o", lib_name, "casting_functions.c"]
                else:
                    cmd = ["gcc", "-shared", "-fPIC", "-o", lib_name, "casting_functions.c"]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    if self.debug:
                        print(f"[DEBUG] Erro ao compilar {lib_name}: {result.stderr}")
                    return
                
                if self.debug:
                    print(f"[DEBUG] {lib_name} compilado com sucesso")
            
            # Carregar a biblioteca compartilhada
            try:
                casting_lib = ctypes.CDLL(lib_path)
                
                # Obter as funções da biblioteca
                functions = {
                    'to_str_int': casting_lib.to_str_int,
                    'to_str_float': casting_lib.to_str_float,
                    'array_to_str_int': casting_lib.array_to_str_int,
                    'array_to_str_float': casting_lib.array_to_str_float,
                    'to_int': casting_lib.to_int,
                    'to_float': casting_lib.to_float,
                }
                
                # Configurar tipos de argumentos e retorno
                functions['to_str_int'].argtypes = [ctypes.c_longlong]
                functions['to_str_int'].restype = ctypes.c_char_p
                
                functions['to_str_float'].argtypes = [ctypes.c_double]
                functions['to_str_float'].restype = ctypes.c_char_p
                
                functions['array_to_str_int'].argtypes = [ctypes.POINTER(ctypes.c_longlong), ctypes.c_longlong]
                functions['array_to_str_int'].restype = ctypes.c_char_p
                
                functions['array_to_str_float'].argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_longlong]
                functions['array_to_str_float'].restype = ctypes.c_char_p
                
                functions['to_int'].argtypes = [ctypes.c_double]
                functions['to_int'].restype = ctypes.c_longlong
                
                functions['to_float'].argtypes = [ctypes.c_longlong]
                functions['to_float'].restype = ctypes.c_double
                
                # Armazenar referências
                self._function_refs = functions
                
                # Criar wrappers para as funções
                self._create_function_wrappers()
                
                # Por enquanto, vamos pular o linkamento manual
                # O LLVM JIT deve resolver as funções automaticamente
                if self.debug:
                    print("[DEBUG] Funções de casting carregadas com sucesso")
                    print("[DEBUG] Pulando linkamento manual - deixando LLVM resolver automaticamente")
                
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] Erro ao carregar {lib_name}: {e}")
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Erro no linkamento: {e}")
                import traceback
                traceback.print_exc()
    
    def _compile_with_casting_functions(self, source: str) -> str:
        """Compila o código MiniLang incluindo as funções de casting"""
        try:
            # Compilar o código MiniLang (que já inclui as declarações das funções de casting)
            llvm_ir = self.compiler.compile(source)
            
            # Usar o LLVM IR original sem modificações
            # Vamos usar uma abordagem de interceptação de chamadas
            combined_ir = llvm_ir
            
            if self.debug:
                print(f"[DEBUG] LLVM IR gerado com {len(combined_ir)} bytes")
            
            return combined_ir
            
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Erro na compilação: {e}")
            raise
    
    def _create_function_wrappers(self):
        """Cria wrappers para as funções de casting"""
        if not hasattr(self, '_function_refs') or not self._function_refs:
            return
        
        # Criar wrappers que interceptam as chamadas
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_longlong)
        def to_str_int_wrapper(value):
            try:
                return self._function_refs['to_str_int'](value)
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] Erro em to_str_int_wrapper: {e}")
                return None
        
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_double)
        def to_str_float_wrapper(value):
            try:
                return self._function_refs['to_str_float'](value)
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] Erro em to_str_float_wrapper: {e}")
                return None
        
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(ctypes.c_longlong), ctypes.c_longlong)
        def array_to_str_int_wrapper(arr, size):
            try:
                return self._function_refs['array_to_str_int'](arr, size)
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] Erro em array_to_str_int_wrapper: {e}")
                return None
        
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_longlong)
        def array_to_str_float_wrapper(arr, size):
            try:
                return self._function_refs['array_to_str_float'](arr, size)
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] Erro em array_to_str_float_wrapper: {e}")
                return None
        
        @ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_double)
        def to_int_wrapper(value):
            try:
                return self._function_refs['to_int'](value)
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] Erro em to_int_wrapper: {e}")
                return 0
        
        @ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_longlong)
        def to_float_wrapper(value):
            try:
                return self._function_refs['to_float'](value)
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] Erro em to_float_wrapper: {e}")
                return 0.0
        
        # Armazenar os wrappers
        self._wrappers = {
            'to_str_int': to_str_int_wrapper,
            'to_str_float': to_str_float_wrapper,
            'array_to_str_int': array_to_str_int_wrapper,
            'array_to_str_float': array_to_str_float_wrapper,
            'to_int': to_int_wrapper,
            'to_float': to_float_wrapper,
        }
        
        # Por enquanto, vamos pular o linkamento manual
        # O LLVM JIT resolve as funções automaticamente
        if self.debug:
            print("[DEBUG] Wrappers criados com sucesso")
            print("[DEBUG] Pulando linkamento manual - LLVM resolverá automaticamente")
    
    def _cleanup_memory(self):
        """Libera memória alocada"""
        # Por ora, deixar o OS limpar
        # Em produção, implementar free() apropriado
        self.allocated_memory.clear()
    
    def execute_file(self, filename: str) -> int:
        """Executa arquivo MiniLang"""
        try:
            # Garantir encoding UTF-8
            with open(filename, 'r', encoding='utf-8') as f:
                source = f.read()
            
            if self.debug:
                print(f"[DEBUG] Arquivo: {filename}")
                print(f"[DEBUG] Tamanho: {len(source)} bytes")
                print(f"[DEBUG] Linhas: {source.count(chr(10)) + 1}")
            
            return self.execute(source)
            
        except FileNotFoundError:
            print(f"Erro: Arquivo '{filename}' não encontrado")
            return 1
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return 1


def main():
    """Entry point"""
    if len(sys.argv) < 2:
        print("MiniLang JIT Interpreter v1.1 (Fixed)")
        print("Uso:")
        print("  python interpreter_jit_fixed.py arquivo.ml")
        print("  python interpreter_jit_fixed.py arquivo.ml --debug")
        print("")
        print("Exemplos:")
        print("  python interpreter_jit_fixed.py teste_simples.ml")
        print("  python interpreter_jit_fixed.py teste_dijkstra_simples.ml --debug")
        return 1
    
    filename = sys.argv[1]
    debug = "--debug" in sys.argv or "-d" in sys.argv
    
    # Mensagem inicial
    if debug:
        print(f"[DEBUG] MiniLang JIT Interpreter v1.1")
        print(f"[DEBUG] Python {sys.version}")
        print(f"[DEBUG] Platform: {sys.platform}")
        print("")
    
    interpreter = MiniLangJIT(debug=debug)
    return interpreter.execute_file(filename)


if __name__ == "__main__":
    sys.exit(main())
