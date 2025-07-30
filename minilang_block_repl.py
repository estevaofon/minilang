#!/usr/bin/env python3
"""
MiniLang Block REPL - Versão que entende a sintaxe correta da MiniLang
"""

import sys
import os
import subprocess
import tempfile

class MiniLangBlockREPL:
    def __init__(self):
        self.code_buffer = []
        self.line_number = 1
        self.last_output = ""
        self.block_mode = False
        self.current_block = []
        self.block_stack = []  # Pilha para controlar blocos aninhados
        self.indent_level = 0
        self.empty_line_count = 0  # Contador de linhas vazias consecutivas
    
    def execute_line(self, line):
        """Executa a linha atual e filtra apenas a nova saída"""
        try:
            # Adicionar a linha atual ao buffer
            self.code_buffer.append(line)
            
            # Criar um arquivo temporário com todo o código acumulado
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ml', delete=False, encoding='utf-8') as f:
                f.write('\n'.join(self.code_buffer) + '\n')
                temp_file = f.name
            
            # Executar o arquivo temporário
            result = subprocess.run([
                sys.executable, 'interpreter_jit.py', temp_file
            ], capture_output=True, text=True, timeout=10)
            
            # Limpar arquivo temporário
            try:
                os.unlink(temp_file)
            except:
                pass
            
            # Filtrar apenas a nova saída
            current_output = result.stdout
            if current_output.startswith(self.last_output):
                new_output = current_output[len(self.last_output):]
                if new_output:
                    print(new_output, end='')
            else:
                # Se não conseguir filtrar, mostrar tudo
                if current_output:
                    print(current_output, end='')
            
            # Atualizar a saída anterior
            self.last_output = current_output
            
            # Mostrar erros (se houver)
            if result.stderr and "LLVM" not in result.stderr:
                print(result.stderr, end='')
            
            return result.returncode
            
        except subprocess.TimeoutExpired:
            print("Timeout: Execução demorou muito tempo")
            return 1
        except Exception as e:
            print(f"Erro: {e}")
            return 1
    
    def execute_block(self, block_lines):
        """Executa um bloco de código"""
        try:
            # Adicionar todas as linhas do bloco ao buffer
            for line in block_lines:
                self.code_buffer.append(line)
            
            # Criar um arquivo temporário com todo o código acumulado
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ml', delete=False, encoding='utf-8') as f:
                f.write('\n'.join(self.code_buffer) + '\n')
                temp_file = f.name
            
            # Executar o arquivo temporário
            result = subprocess.run([
                sys.executable, 'interpreter_jit.py', temp_file
            ], capture_output=True, text=True, timeout=10)
            
            # Limpar arquivo temporário
            try:
                os.unlink(temp_file)
            except:
                pass
            
            # Filtrar apenas a nova saída
            current_output = result.stdout
            if current_output.startswith(self.last_output):
                new_output = current_output[len(self.last_output):]
                if new_output:
                    print(new_output, end='')
            else:
                # Se não conseguir filtrar, mostrar tudo
                if current_output:
                    print(current_output, end='')
            
            # Atualizar a saída anterior
            self.last_output = current_output
            
            # Mostrar erros (se houver)
            if result.stderr and "LLVM" not in result.stderr:
                print(result.stderr, end='')
            
            return result.returncode
            
        except subprocess.TimeoutExpired:
            print("Timeout: Execução demorou muito tempo")
            return 1
        except Exception as e:
            print(f"Erro: {e}")
            return 1
    
    def analyze_line(self, line):
        """Analisa uma linha para detectar início/fim de blocos"""
        line = line.strip()
        
        # Detectar início de blocos
        if line.startswith('func '):
            return 'func_start'
        elif line.startswith('if ') and ' then' in line:
            return 'if_start'
        elif line.startswith('while ') and ' do' in line:
            return 'while_start'
        elif line.startswith('for ') and ' do' in line:
            return 'for_start'
        elif line == 'else':
            return 'else_start'
        elif line == 'end':
            return 'end'
        else:
            return 'normal'
    
    def count_block_changes(self, line):
        """Conta quantos blocos são abertos e fechados na linha"""
        line = line.strip()
        opens = 0
        closes = 0
        
        # Detectar blocos que abrem
        if line.startswith('func '):
            opens += 1
        if line.startswith('if ') and ' then' in line:
            opens += 1
        if line.startswith('while ') and ' do' in line:
            opens += 1
        if line.startswith('for ') and ' do' in line:
            opens += 1
        if line == 'else':
            opens += 1
        
        # Detectar blocos que fecham
        if line == 'end':
            closes += 1
        
        return opens, closes
    
    def is_block_start(self, line):
        """Verifica se a linha inicia um bloco"""
        analysis = self.analyze_line(line)
        return analysis in ['func_start', 'if_start', 'while_start', 'for_start', 'else_start']
    
    def add_line(self, line):
        """Adiciona uma linha ao buffer de código"""
        self.code_buffer.append(line)
    
    def clear_buffer(self):
        """Limpa o buffer de código"""
        self.code_buffer.clear()
        self.last_output = ""
    
    def get_buffer(self):
        """Retorna o código acumulado"""
        return '\n'.join(self.code_buffer)
    
    def remove_last_line(self):
        """Remove a última linha do buffer"""
        if self.code_buffer:
            self.code_buffer.pop()
            # Resetar a saída anterior para forçar recálculo
            self.last_output = ""

def handle_special_command(command, repl):
    """Manipula comandos especiais"""
    cmd = command.lower().strip()
    
    if cmd == '.help':
        print("Comandos especiais:")
        print("  .help     - Mostra esta ajuda")
        print("  .quit     - Sai do REPL")
        print("  .exit     - Sai do REPL")
        print("  .clear    - Limpa a tela")
        print("  .version  - Mostra a versão do interpretador")
        print("  .test     - Executa um teste simples")
        print("  .reset    - Limpa o buffer de código")
        print("  .show     - Mostra o código acumulado")
        print("  .run      - Executa o código acumulado")
        print("  .undo     - Remove a última linha")
        print("  .block    - Entra no modo bloco")
        print("")
        print("📝 BLOCOS DE CÓDIGO MINILANG:")
        print("  - func nome() -> tipo ... end")
        print("  - if condição then ... end")
        print("  - while condição do ... end")
        print("  - for i in 0..10 do ... end")
        print("  - else ... end")
        print("  - Digite duas linhas vazias consecutivas para finalizar bloco manual")
        return 0
    
    elif cmd in ['.quit', '.exit']:
        print("Saindo do REPL...")
        return -1
    
    elif cmd == '.clear':
        os.system('cls' if os.name == 'nt' else 'clear')
        return 0
    
    elif cmd == '.version':
        print("MiniLang JIT Interpreter v1.1")
        print("Python 3.13.1")
        print("LLVM JIT Compilation")
        return 0
    
    elif cmd == '.test':
        print("Executando teste simples...")
        repl.clear_buffer()
        repl.add_line('print("Teste funcionando!")')
        return repl.execute_line('print("Teste funcionando!")')
    
    elif cmd == '.reset':
        repl.clear_buffer()
        print("Buffer de código limpo")
        return 0
    
    elif cmd == '.show':
        if repl.code_buffer:
            print("Código acumulado:")
            for i, line in enumerate(repl.code_buffer, 1):
                print(f"  {i:2d}: {line}")
        else:
            print("Buffer vazio")
        return 0
    
    elif cmd == '.run':
        if repl.code_buffer:
            print("Executando código acumulado...")
            return repl.execute_block(repl.code_buffer)
        else:
            print("Buffer vazio - nada para executar")
            return 0
    
    elif cmd == '.undo':
        if repl.code_buffer:
            removed = repl.code_buffer.pop()
            print(f"Removida última linha: {removed}")
        else:
            print("Buffer vazio - nada para remover")
        return 0
    
    elif cmd == '.block':
        print("Modo bloco ativado. Digite seu código:")
        print("(Digite duas linhas vazias consecutivas para finalizar)")
        
        block_lines = []
        empty_count = 0
        while True:
            try:
                line = input("  > ")
                if not line.strip():
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                block_lines.append(line)
            except (KeyboardInterrupt, EOFError):
                print("\nBloco cancelado")
                return 0
        
        if block_lines:
            print(f"Executando bloco com {len(block_lines)} linhas...")
            return repl.execute_block(block_lines)
        return 0
    
    else:
        print(f"Comando desconhecido: {command}")
        print("Digite .help para ver os comandos disponíveis")
        return 0

def main():
    """Inicia o REPL com suporte a blocos MiniLang"""
    print("=" * 60)
    print("MiniLang JIT Interpreter - MiniLang Block REPL Mode")
    print("=" * 60)
    print("Digite código MiniLang linha por linha.")
    print("O estado é mantido entre as linhas.")
    print("Apenas a nova saída é mostrada (sem repetir prints).")
    print("")
    print("📝 BLOCOS DE CÓDIGO MINILANG:")
    print("  - func nome() -> tipo ... end")
    print("  - if condição then ... end")
    print("  - while condição do ... end")
    print("  - for i in 0..10 do ... end")
    print("  - else ... end")
    print("  - Digite duas linhas vazias consecutivas para finalizar bloco manual")
    print("")
    print("Comandos especiais começam com '.' (ex: .help)")
    print("Pressione Ctrl+C ou digite .quit para sair")
    print("=" * 60)
    
    repl = MiniLangBlockREPL()
    
    try:
        while True:
            try:
                # Prompt personalizado
                if repl.block_mode:
                    prompt = "  > "
                else:
                    prompt = f"minilang[{repl.line_number}]> "
                
                # Capturar input
                line = input(prompt)
                
                # Verificar se é comando especial
                if line.startswith('.'):
                    result = handle_special_command(line, repl)
                elif repl.block_mode:
                    # Modo bloco ativo
                    if not line.strip():
                        # Linha vazia - incrementar contador
                        repl.empty_line_count += 1
                        repl.current_block.append(line)
                        
                        # Se duas linhas vazias consecutivas, finalizar bloco
                        if repl.empty_line_count >= 2:
                            repl.block_mode = False
                            repl.empty_line_count = 0
                            if repl.current_block:
                                print(f"Executando bloco com {len(repl.current_block)} linhas...")
                                result = repl.execute_block(repl.current_block)
                                repl.current_block = []
                            else:
                                result = 0
                        else:
                            continue  # Continuar no modo bloco
                    else:
                        # Linha não vazia - resetar contador e adicionar ao bloco
                        repl.empty_line_count = 0
                        repl.current_block.append(line)
                        
                        # Contar blocos abertos e fechados
                        opens, closes = repl.count_block_changes(line)
                        
                        # Atualizar contador de blocos
                        repl.indent_level += opens - closes
                        
                        # Se todos os blocos foram fechados, finalizar
                        if repl.indent_level <= 0:
                            repl.block_mode = False
                            repl.indent_level = 0
                            repl.empty_line_count = 0
                            if repl.current_block:
                                print(f"Executando bloco com {len(repl.current_block)} linhas...")
                                result = repl.execute_block(repl.current_block)
                                repl.current_block = []
                            else:
                                result = 0
                        else:
                            continue  # Continuar no modo bloco
                else:
                    # Verificar se é início de bloco
                    if repl.is_block_start(line):
                        repl.block_mode = True
                        repl.current_block = [line]
                        repl.indent_level = 0
                        repl.empty_line_count = 0
                        opens, closes = repl.count_block_changes(line)
                        repl.indent_level += opens - closes
                        print("  > (Modo bloco ativado. Digite 'end' ou duas linhas vazias para finalizar)")
                        continue
                    else:
                        # Linha única
                        result = repl.execute_line(line)
                
                # Verificar se deve sair
                if result == -1:
                    break
                
                repl.line_number += 1
                
            except KeyboardInterrupt:
                print("\nSaindo do REPL...")
                break
            except EOFError:
                print("\nSaindo do REPL...")
                break
            except Exception as e:
                print(f"Erro inesperado: {e}")
    
    except Exception as e:
        print(f"Erro fatal no REPL: {e}")
    
    print("REPL finalizado.")

if __name__ == "__main__":
    main() 