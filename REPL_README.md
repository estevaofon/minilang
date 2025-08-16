# Nox JIT Interpreter - REPL (Read-Eval-Print Loop)

Este documento descreve o REPL oficial para o Nox JIT Interpreter.

## 🚀 REPL Oficial: `nox_repl.py`

### **Características Principais:**
- ✅ **Sintaxe Nox correta**: `func/end`, `if/then/end`, `while/do/end`
- ✅ **Estado persistente**: Mantém variáveis entre linhas
- ✅ **Filtro de saída**: Evita repetição de prints
- ✅ **Blocos aninhados**: Entende estruturas complexas
- ✅ **Finalização flexível**: `end` automático ou duas linhas vazias

### **Como Usar:**
```bash
uv run .\nox_repl.py
```

## 📝 Comandos Especiais

| Comando | Descrição |
|---------|-----------|
| `.help` | Mostra ajuda |
| `.quit` ou `.exit` | Sai do REPL |
| `.clear` | Limpa a tela |
| `.version` | Mostra versão |
| `.test` | Executa teste simples |
| `.reset` | Limpa buffer de código |
| `.show` | Mostra código acumulado |
| `.run` | Executa código acumulado |
| `.undo` | Remove última linha |
| `.block` | Modo bloco manual |

## 🧱 Blocos de Código

O REPL suporta blocos de código da sintaxe Nox:

### Sintaxe Suportada
- **Funções**: `func nome() -> tipo ... end`
- **Condicionais**: `if condição then ... end`
- **Loops While**: `while condição do ... end`
- **Loops For**: `for i in 0..10 do ... end`
- **Else**: `else ... end`

### Detecção Automática
O REPL detecta automaticamente quando você está iniciando um bloco:

```bash
nox[1]> if x > 5 then
  > print("x é maior que 5")
  > end
x é maior que 5
```

### Como Usar Blocos
1. **Digite uma linha que inicie um bloco**:
   ```
   nox[1]> func fatorial(n: int) -> int
   ```

2. **Continue digitando as linhas do bloco**:
   ```
     > if n <= 1 then
     >   return 1
     > else
     >   return n * fatorial(n - 1)
     > end
     > end
   ```

3. **O bloco é executado automaticamente** quando encontra `end` ou duas linhas vazias

### Finalização de Blocos
- **Automática**: Quando todos os `end` são encontrados
- **Manual**: Duas linhas vazias consecutivas

## 💡 Exemplos Práticos

### Exemplo 1: Função Fatorial
```bash
nox[1]> func fatorial(n: int) -> int
  > if n <= 1 then
  >   return 1
  > else
  >   return n * fatorial(n - 1)
  > end
  > end
nox[2]> print(fatorial(5))
120
```

### Exemplo 2: Loop While
```bash
nox[1]> let i = 0
nox[2]> while i < 5 do
  > print(i)
  > i = i + 1
  > end
0
1
2
3
4
```

### Exemplo 3: Condicional If/Else
```bash
nox[1]> let x = 10
nox[2]> if x > 5 then
  > print("x é maior que 5")
  > else
  > print("x é menor ou igual a 5")
  > end
x é maior que 5
```

### Exemplo 4: Loop For
```bash
nox[1]> for i in 0..5 do
  > print(i * 2)
  > end
0
2
4
6
8
10
```

### Exemplo 5: Função com Loop Aninhado
```bash
nox[1]> func calcula_media(notas: int[], tamanho: int) -> int
  > let soma: int = 0
  > let i: int = 0
  > 
  > while i < tamanho do
  >     soma = soma + notas[i]
  >     i = i + 1
  > end
  > return soma / tamanho
  > 
  > 
Executando bloco com 10 linhas...
```

## 🔧 Funcionalidades

### Filtro de Saída
- **Problema**: REPLs normais repetem prints anteriores
- **Solução**: Filtra apenas a nova saída
- **Resultado**: Interface limpa e profissional

### Estado Persistente
- **Variáveis**: Mantidas entre linhas
- **Funções**: Definidas ficam disponíveis
- **Arrays**: Preservados no contexto

### Blocos Aninhados
- **Contagem inteligente**: Conta blocos abertos e fechados
- **Estruturas complexas**: Suporta funções com loops e condicionais
- **Finalização correta**: Só executa quando todos os blocos estão fechados

### Timeout de Execução
- **Proteção**: Evita loops infinitos
- **Timeout**: 10 segundos por execução
- **Recuperação**: Continua funcionando após timeout

### Tratamento de Erros
- **LLVM**: Filtra erros internos do LLVM
- **Syntax**: Mostra erros de sintaxe claramente
- **Runtime**: Exibe erros de execução

## ⚙️ Configuração

### Variáveis de Ambiente
```bash
# Ativar modo debug (se disponível)
set NOX_DEBUG=1
uv run .\nox_repl.py
```

### Arquivos de Configuração
- **Nenhum arquivo de configuração necessário**
- **Configuração automática** baseada no sistema
- **Compatibilidade** com Windows e Linux

## 🐛 Solução de Problemas

### Problema: "LLVM ERROR"
```
LLVM ERROR: Target does not support MC emission!
```
**Solução**: Use `nox_repl.py` que evita problemas de LLVM

### Problema: Prints Repetidos
```
Hello World
Hello World
Hello World
```
**Solução**: O REPL filtra automaticamente a saída

### Problema: Variáveis Não Persistem
```
Erro durante execução: Variável 'x' não definida
```
**Solução**: O REPL mantém estado automaticamente

### Problema: Blocos Não Funcionam
```
Erro de sintaxe: bloco não fechado
```
**Solução**: Use a sintaxe correta da Nox (`func/end`, `if/then/end`, etc.)

## 🎯 Recursos Avançados

### Modo Bloco Manual
Use o comando `.block` para entrar no modo bloco manualmente:

```bash
nox[1]> .block
Modo bloco ativado. Digite seu código:
(Digite duas linhas vazias consecutivas para finalizar)
  > let array = [1, 2, 3, 4, 5]
  > for i in 0..5 do
  >   print(array[i])
  > end
  > 
  > 
Executando bloco com 4 linhas...
1
2
3
4
5
```

### Comandos de Gerenciamento
- **`.show`**: Mostra todo o código acumulado
- **`.reset`**: Limpa o buffer de código
- **`.undo`**: Remove a última linha digitada
- **`.run`**: Executa todo o código acumulado

## 🔮 Limitações Conhecidas

### Limitações Gerais
- **Arquivos temporários**: Cria arquivos temporários para execução
- **Performance**: Cada execução recria o contexto LLVM
- **Memória**: Acumula código no buffer

### Limitações Específicas
- **Blocos muito complexos**: Pode ter problemas com estruturas extremamente aninhadas
- **Caracteres especiais**: Alguns caracteres podem não funcionar no Windows
- **Terminal**: Depende do terminal para input/output

## 📝 Histórico de Versões

### v1.0 - REPL Básico
- REPL simples sem estado
- Execução linha por linha

### v1.1 - REPL com Estado
- Estado persistente entre linhas
- Filtro de saída

### v1.2 - REPL com Blocos (C-style)
- Suporte a blocos de código com `{`/`}`
- Detecção automática de blocos

### v1.3 - REPL com Sintaxe Nox
- **Sintaxe correta da Nox**: `func/end`, `if/then/end`, `while/do/end`
- **Detecção automática** de blocos Nox
- **Blocos aninhados** com contagem inteligente
- **Finalização flexível** com `end` ou duas linhas vazias

## 🤝 Contribuindo

Para contribuir com melhorias no REPL:

1. **Teste** o REPL com diferentes cenários
2. **Reporte** bugs encontrados
3. **Sugira** novas funcionalidades
4. **Documente** melhorias

## 📞 Suporte

Para suporte ou dúvidas:
- **Issues**: Abra uma issue no repositório
- **Documentação**: Consulte este README
- **Exemplos**: Veja a pasta `nox_examples/` 