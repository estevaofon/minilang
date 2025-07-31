#!/usr/bin/env python3
"""
MiniLang Block REPL - Versão que entende a sintaxe correta da MiniLang
Com Syntax Highlighting Opcional e Isolamento de Erros
"""

import sys
import os
import subprocess
import tempfile
import re
from colorama import init, Fore, Back, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style as PromptStyle
from prompt_toolkit.completion import WordCompleter
from pygments.lexers import PythonLexer
from pygments.lexer import RegexLexer, bygroups
from pygments.token import *

# Inicializar colorama para suporte cross-platform
init(autoreset=True)

class MiniLangLexer(RegexLexer):
    """Lexer customizado para MiniLang"""
    name = 'MiniLang'
    aliases = ['minilang', 'ml']
    filenames = ['*.ml']
    
    tokens = {
        'root': [
            # Keywords
            (r'\b(func|if|then|else|while|do|end|return|let|global|print|struct|length|to_str)\b', Keyword),
            # Types
            (r'\b(int|float|string|void|bool)\b', Keyword.Type),
            # Strings
            (r'"[^"]*"', String),
            # Numbers
            (r'\b\d+\b', Number.Integer),
            (r'\b\d+\.\d+\b', Number.Float),
            # Comments
            (r'#.*$', Comment),
            # Operators
            (r'[+\-*/=<>!&|]', Operator),
            # Punctuation
            (r'[(),;:]', Punctuation),
            # Identifiers
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', Name),
            # Whitespace
            (r'\s+', Text),
        ]
    }

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
        self.syntax_highlighting = True  # Ativado por padrão
        self.error_count = 0  # Contador de erros para estatísticas
        self.last_error = None  # Último erro ocorrido
        
        # Completador
        commands = ['.help', '.quit', '.exit', '.clear', '.version', 
                   '.test', '.reset', '.show', '.run', '.undo', '.block', '.syntax',
                   '.status', '.errors', '.fast']
        keywords = ['func', 'if', 'then', 'else', 'while', 'do', 'end', 'return',
                   'let', 'global', 'print', 'struct', 'length', 'to_str']
        types = ['int', 'float', 'string', 'void', 'bool']
        
        self.completer = WordCompleter(commands + keywords + types, ignore_case=True)
        
        # Estilo para as cores (simplificado)
        self.style = PromptStyle.from_dict({
            'pygments.keyword': 'ansicyan bold',
            'pygments.keyword.type': 'ansigreen bold',
            'pygments.string': 'ansimagenta',
            'pygments.number': 'ansiyellow',
            'pygments.comment': 'ansiblue',
            'pygments.operator': 'ansired',
            'pygments.name': 'ansiwhite',
            'pygments.punctuation': 'ansiwhite',
        })
        
        # Sessão do prompt (com lexer por padrão)
        self.lexer = PygmentsLexer(MiniLangLexer)
        self.session = PromptSession(
            lexer=self.lexer,  # Com syntax highlighting por padrão
            completer=self.completer,
            style=self.style,
            enable_history_search=True,
            complete_while_typing=False,  # Desativado para evitar bloqueios
            mouse_support=False,  # Desativado para evitar conflitos
            enable_system_prompt=False,  # Desativado para melhor performance
            enable_suspend=False,  # Desativado para evitar problemas
        )
    
    def toggle_syntax_highlighting(self):
        """Ativa/desativa syntax highlighting"""
        self.syntax_highlighting = not self.syntax_highlighting
        
        # Recriar sessão com novo lexer
        if self.syntax_highlighting:
            self.lexer = PygmentsLexer(MiniLangLexer)
            self.session = PromptSession(
                lexer=self.lexer,
                completer=self.completer,
                style=self.style,
                enable_history_search=True,
                complete_while_typing=False,  # Desativado para evitar bloqueios
                mouse_support=False,  # Desativado para evitar conflitos
                enable_system_prompt=False,  # Desativado para melhor performance
                enable_suspend=False,  # Desativado para evitar problemas
            )
        else:
            self.session = PromptSession(
                lexer=None,
                completer=self.completer,
                style=self.style,
                enable_history_search=True,
                complete_while_typing=False,  # Desativado para evitar bloqueios
                mouse_support=False,  # Desativado para evitar conflitos
                enable_system_prompt=False,  # Desativado para melhor performance
                enable_suspend=False,  # Desativado para evitar problemas
            )
        
        status = "ativado" if self.syntax_highlighting else "desativado"
        print(f"Syntax highlighting {status}")
    
    def enable_fast_mode(self):
        """Ativa modo rápido (sem syntax highlighting)"""
        if self.syntax_highlighting:
            self.toggle_syntax_highlighting()
        print("🚀 Modo rápido ativado - Syntax highlighting desativado para melhor performance")
    
    def get_input(self, prompt):
        """Obtém input usando prompt_toolkit otimizado"""
        try:
            return self.session.prompt(prompt)
        except KeyboardInterrupt:
            raise KeyboardInterrupt  # Re-raise para ser capturado no main
        except EOFError:
            raise EOFError  # Re-raise para ser capturado no main
        except Exception as e:
            # Fallback para input simples em caso de erro
            print(f"{Fore.YELLOW}⚠️  Erro no input, usando modo simples: {e}{Style.RESET_ALL}")
            try:
                return input(prompt)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except EOFError:
                raise EOFError
            except:
                return ""
    

    
    def safe_execute(self, execution_func, *args, **kwargs):
        """Executa uma função de forma segura com isolamento de erros"""
        try:
            return execution_func(*args, **kwargs)
        except subprocess.TimeoutExpired:
            error_msg = "⏰ Timeout: Execução demorou muito tempo"
            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
            self.error_count += 1
            self.last_error = error_msg
            return 1
        except subprocess.CalledProcessError as e:
            error_msg = f"🚫 Erro de execução (código {e.returncode}): {e.stderr if e.stderr else 'Erro desconhecido'}"
            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
            self.error_count += 1
            self.last_error = error_msg
            return e.returncode
        except FileNotFoundError:
            error_msg = "❌ Erro: Interpreter não encontrado (interpreter_jit.py)"
            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
            self.error_count += 1
            self.last_error = error_msg
            return 1
        except PermissionError:
            error_msg = "🔒 Erro: Sem permissão para executar o interpretador"
            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
            self.error_count += 1
            self.last_error = error_msg
            return 1
        except Exception as e:
            error_msg = f"💥 Erro inesperado: {str(e)}"
            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
            self.error_count += 1
            self.last_error = error_msg
            return 1
    
    def execute_line(self, line):
        """Executa a linha atual e filtra apenas a nova saída com isolamento de erros"""
        def _execute():
            # Salvar o estado atual do buffer
            original_buffer = self.code_buffer.copy()
            original_output = self.last_output
            
            # Adicionar a linha atual ao buffer
            self.code_buffer.append(line)
            
            # Criar um arquivo temporário com todo o código acumulado
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ml', delete=False, encoding='utf-8') as f:
                f.write('\n'.join(self.code_buffer) + '\n')
                temp_file = f.name
            
            try:
                # Executar o arquivo temporário
                result = subprocess.run([
                    sys.executable, 'interpreter_jit.py', temp_file
                ], capture_output=True, text=True, timeout=10)
                
                # Se houve erro (returncode != 0), fazer rollback
                if result.returncode != 0:
                    # Restaurar o buffer original
                    self.code_buffer = original_buffer
                    self.last_output = original_output
                    
                    # Mostrar o erro de forma clara
                    error_msg = result.stderr.strip() if result.stderr else "Erro desconhecido"
                    if error_msg and "LLVM" not in error_msg:
                        print(f"{Fore.RED}❌ ERRO: {error_msg}{Style.RESET_ALL}")
                    
                    return result.returncode
                
                # Se não houve erro, processar a saída normalmente
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
                
                # Mostrar warnings (se houver) mas não quebrar a execução
                if result.stderr and "LLVM" not in result.stderr:
                    print(f"{Fore.YELLOW}⚠️  WARNING: {result.stderr.strip()}{Style.RESET_ALL}")
                
                return result.returncode
                
            finally:
                # Limpar arquivo temporário
                try:
                    os.unlink(temp_file)
                except:
                    pass
        
        return self.safe_execute(_execute)
    
    def execute_block(self, block_lines):
        """Executa um bloco de código com isolamento de erros"""
        def _execute():
            # Salvar o estado atual do buffer
            original_buffer = self.code_buffer.copy()
            original_output = self.last_output
            
            # Adicionar todas as linhas do bloco ao buffer
            for line in block_lines:
                self.code_buffer.append(line)
            
            # Criar um arquivo temporário com todo o código acumulado
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ml', delete=False, encoding='utf-8') as f:
                f.write('\n'.join(self.code_buffer) + '\n')
                temp_file = f.name
            
            try:
                # Executar o arquivo temporário
                result = subprocess.run([
                    sys.executable, 'interpreter_jit.py', temp_file
                ], capture_output=True, text=True, timeout=10)
                
                # Se houve erro (returncode != 0), fazer rollback
                if result.returncode != 0:
                    # Restaurar o buffer original
                    self.code_buffer = original_buffer
                    self.last_output = original_output
                    
                    # Mostrar o erro de forma clara
                    error_msg = result.stderr.strip() if result.stderr else "Erro desconhecido"
                    if error_msg and "LLVM" not in error_msg:
                        print(f"{Fore.RED}❌ ERRO: {error_msg}{Style.RESET_ALL}")
                    
                    return result.returncode
                
                # Se não houve erro, processar a saída normalmente
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
                
                # Mostrar warnings (se houver) mas não quebrar a execução
                if result.stderr and "LLVM" not in result.stderr:
                    print(f"{Fore.YELLOW}⚠️  WARNING: {result.stderr.strip()}{Style.RESET_ALL}")
                
                return result.returncode
                
            finally:
                # Limpar arquivo temporário
                try:
                    os.unlink(temp_file)
                except:
                    pass
        
        return self.safe_execute(_execute)
    
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
        elif line.startswith('struct '):
            return 'struct_start'
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
        if line.startswith('struct '):
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
        return analysis in ['func_start', 'if_start', 'while_start', 'struct_start', 'else_start']
    
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
    
    def get_status(self):
        """Retorna o status atual do REPL"""
        return {
            'line_number': self.line_number,
            'buffer_size': len(self.code_buffer),
            'error_count': self.error_count,
            'last_error': self.last_error,
            'block_mode': self.block_mode,
            'indent_level': self.indent_level
        }

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
        print("  .syntax   - Ativa/desativa syntax highlighting")
        print("  .status   - Mostra status do REPL")
        print("  .errors   - Mostra estatísticas de erros")
        print("  .fast     - Ativa modo rápido (sem syntax highlighting)")
        print("")
        print("🎨 SYNTAX HIGHLIGHTING:")
        print("  - Ativado por padrão para melhor performance")
        print("  - Use .syntax para desativar")
        print("  - Cores: Ciano (keywords), Verde (tipos), Magenta (strings), Amarelo (números)")
        print("  - Em tempo real quando ativado")
        print("")
        print("📝 BLOCOS: func/if/while/struct ... end")
        print("  - Duas linhas vazias para finalizar bloco manual")
        print("")
        print("🛡️ ISOLAMENTO DE ERROS:")
        print("  - Erros não afetam comandos subsequentes")
        print("  - Estado do REPL mantido após erros")
        print("  - Feedback claro sobre erros")
        print("")
        print("✨ RECURSOS:")
        print("  - Input otimizado responsivo (sem bloqueios)")
        print("  - Autocompletar com Tab")
        print("  - Histórico de comandos")
        print("  - Copiar/colar funcionando normalmente")
        print("  - Ctrl+C para sair a qualquer momento")
        print("  - Syntax highlighting ativado por padrão")
        return 0
    
    elif cmd in ['.quit', '.exit']:
        print("Saindo do REPL...")
        return -1
    
    elif cmd == '.clear':
        os.system('cls' if os.name == 'nt' else 'clear')
        return 0
    
    elif cmd == '.version':
        print("MiniLang JIT Interpreter v2.4")
        print("Python 3.13.1")
        print("LLVM JIT Compilation")
        print("Syntax Highlighting Ativado")
        print("Isolamento de Erros Ativo")
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
                line = repl.get_input("  > ")
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
    
    elif cmd == '.syntax':
        repl.toggle_syntax_highlighting()
        return 0
    
    elif cmd == '.fast':
        repl.enable_fast_mode()
        return 0
    
    elif cmd == '.status':
        status = repl.get_status()
        print(f"📊 Status do REPL:")
        print(f"  Linha atual: {status['line_number']}")
        print(f"  Buffer: {status['buffer_size']} linhas")
        print(f"  Erros: {status['error_count']}")
        print(f"  Modo bloco: {'Sim' if status['block_mode'] else 'Não'}")
        print(f"  Nível de indentação: {status['indent_level']}")
        if status['last_error']:
            print(f"  Último erro: {status['last_error']}")
        return 0
    
    elif cmd == '.errors':
        status = repl.get_status()
        print(f"📈 Estatísticas de Erros:")
        print(f"  Total de erros: {status['error_count']}")
        if status['last_error']:
            print(f"  Último erro: {status['last_error']}")
        else:
            print("  Nenhum erro registrado")
        return 0
    
    else:
        print(f"Comando desconhecido: {command}")
        print("Digite .help para ver os comandos disponíveis")
        return 0

def main():
    """Inicia o REPL com suporte a blocos MiniLang e isolamento de erros"""
    print("=" * 60)
    print("MiniLang JIT Interpreter - REPL v2.4")
    print("=" * 60)
    print("Digite código linha por linha. Estado mantido entre linhas.")
    print("🎨 SYNTAX HIGHLIGHTING: Ativado por padrão")
    print("📝 BLOCOS: func/if/while/struct ... end")
    print("  - Duas linhas vazias para finalizar bloco manual")
    print("🛡️ ISOLAMENTO DE ERROS: Erros não afetam comandos subsequentes")
    print("✨ RECURSOS: Autocompletar | Histórico | Copiar/Colar | Ctrl+C para sair")
    print("Comandos: .help .quit .clear .reset .syntax .fast .status .errors")
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
                
                # Capturar input com syntax highlighting opcional
                line = repl.get_input(prompt)
                
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
                print(f"{Fore.RED}Erro inesperado no REPL: {e}{Style.RESET_ALL}")
                repl.error_count += 1
                repl.last_error = f"Erro interno: {e}"
                # Continuar executando mesmo após erro interno
    
    except Exception as e:
        print(f"{Fore.RED}Erro fatal no REPL: {e}{Style.RESET_ALL}")
    
    print("REPL finalizado.")

if __name__ == "__main__":
    main() 