# 🧪 Testes de Mensagens de Erro - Compilador Noxy

Esta pasta contém uma suíte completa de testes para validar o sistema de relatório de erros do compilador Noxy.

## 📋 Tipos de Erro Testados

### 🔧 Erros de Sintaxe
- **01_syntax_error_missing_let.nx** - Declaração de variável sem `let`
- **02_syntax_error_unterminated_string.nx** - String não terminada
- **03_syntax_error_missing_parentheses.nx** - Parênteses ausentes
- **10_invalid_character_error.nx** - Caracteres inválidos no código

### 🔍 Erros Semânticos
- **04_semantic_error_undefined_variable.nx** - Variável não declarada
- **05_semantic_error_undefined_function.nx** - Função não declarada
- **06_semantic_error_struct_field.nx** - Campo de struct inexistente

### 🏗️ Erros de Estrutura
- **08_struct_error_wrong_constructor.nx** - Construtor de struct incorreto
- **09_array_error_wrong_access.nx** - Acesso incorreto a arrays

### ⚙️ Erros de Geração de Código
- **11_codegen_error_print_struct.nx** - Tentativa de imprimir struct diretamente

### 🔀 Erros de Tipo
- **07_type_error_incompatible_types.nx** - Tipos incompatíveis

### 🔄 Múltiplos Erros
- **12_multiple_errors.nx** - Arquivo com vários tipos de erro

## 🚀 Como Executar os Testes

### Executar Teste Individual
```bash
# Navegar para o diretório do projeto
cd D:\OneDrive\Documentos\python_projects\noxy

# Testar um arquivo específico
uv run python compiler.py --compile test_error_messages/01_syntax_error_missing_let.nx
```

### Executar Todos os Testes
```bash
# Usando o script Python
cd test_error_messages
python run_error_tests.py
```

### Executar Teste Manual
```bash
# Para cada arquivo .nx na pasta
uv run python compiler.py --compile test_error_messages/<arquivo>.nx
```

## 📊 Exemplo de Saída Esperada

### ✅ Erro de Sintaxe
```
ERRO DE SINTAXE:
Erro na linha 5, coluna 1: Token inesperado 'x'. Esperado: let, print, if, while, func, struct
  x: int = 10
  ^
```

### ✅ Erro Semântico
```
ERRO SEMÂNTICO:
Erro: Variável 'y' não foi declarada
```

### ✅ Erro de Geração de Código
```
ERRO DE GERAÇÃO DE CÓDIGO:
Erro na geração de código LLVM: invalid operation
Isso pode ser causado por um problema no código Nox, como:
- Acesso incorreto a campos de struct
- Tipos incompatíveis em expressões
- Uso de variáveis não declaradas
```

## 🎯 Objetivos dos Testes

1. **Validar** que todos os tipos de erro são detectados
2. **Verificar** que as mensagens são claras e úteis
3. **Confirmar** que linha e coluna são reportadas corretamente
4. **Garantir** que o contexto do código é mostrado
5. **Testar** a categorização correta dos erros

## 📝 Adicionando Novos Testes

Para adicionar um novo teste de erro:

1. Crie um arquivo `.nx` seguindo o padrão de nomenclatura
2. Inclua comentários explicando o erro esperado
3. Adicione exemplos de código que devem falhar
4. Execute o teste para verificar a mensagem de erro
5. Atualize este README se necessário

## 🔧 Estrutura dos Arquivos de Teste

Cada arquivo de teste segue este padrão:
```nox
// TIPO DE ERRO: Descrição do erro
print("Teste: Nome do teste")

// Código que deve funcionar normalmente
let x: int = 10

// Esta linha deve causar erro - comentário explicativo
linha_com_erro()

// Código adicional se necessário
```
