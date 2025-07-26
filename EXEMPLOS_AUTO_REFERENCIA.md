# Exemplos de Auto-Referência na MiniLang

Este documento apresenta uma coleção de exemplos que demonstram o uso de structs com auto-referência na MiniLang, implementados com a abordagem conservadora que evita recursão infinita.

## 📁 Arquivos de Exemplo

### 1. **teste_struct_auto_ref.ml**
**Descrição**: Exemplo básico demonstrando auto-referência simples
- Struct `Node` com campo `proximo: ref Node`
- Struct `TreeNode` com campos `esquerda: ref TreeNode` e `direita: ref TreeNode`
- Struct `GraphNode` com campo `vizinho: ref GraphNode`

**Funcionalidades demonstradas**:
- Auto-referência básica
- Múltiplas auto-referências
- Validação de referências circulares

### 2. **arvore_binaria_completa.ml**
**Descrição**: Implementação completa de árvore binária
- Struct `TreeNode` com auto-referência
- Funções de inserção, busca, percorrimento
- Operações: valor mínimo, máximo, contagem, altura

**Funcionalidades demonstradas**:
- Inserção ordenada
- Busca eficiente
- Percorrimentos (pré, em, pós-ordem)
- Cálculo de propriedades da árvore
- Recursão com auto-referência

### 3. **lista_dupla_encadeada.ml**
**Descrição**: Lista dupla encadeada com navegação bidirecional
- Struct `Node` com campos `anterior: ref Node` e `proximo: ref Node`
- Operações de inserção e remoção
- Navegação em ambas as direções

**Funcionalidades demonstradas**:
- Inserção no início, fim e posição específica
- Remoção do início e fim
- Navegação bidirecional
- Busca e contagem de elementos

### 4. **grafo_simples.ml**
**Descrição**: Implementação de grafo usando array de referências
- Struct `GraphNode` com campo `vizinhos: ref GraphNode[5]`
- Operações de criação de nós e arestas
- Verificação de conexões

**Funcionalidades demonstradas**:
- Criação de nós do grafo
- Adição de arestas
- Verificação de conexões
- Contagem de vizinhos
- Array de referências

### 5. **teste_referencia_circular_invalida.ml**
**Descrição**: Demonstração de detecção de erros
- Exemplos de referências válidas e inválidas
- Teste de validação do sistema

**Funcionalidades demonstradas**:
- Detecção de referências para structs não definidos
- Validação de referências circulares complexas
- Prevenção de recursão infinita

## 🏗️ Estruturas de Dados Implementadas

### Árvore Binária
```minilang
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end
```

### Lista Dupla Encadeada
```minilang
struct Node
    valor: int,
    anterior: ref Node,
    proximo: ref Node
end
```

### Grafo
```minilang
struct GraphNode
    id: int,
    valor: int,
    vizinhos: ref GraphNode[5]
end
```

## ✅ Vantagens da Abordagem Conservadora

### Segurança
- **Evita recursão infinita**: Usa placeholders seguros (`void*`)
- **Validação robusta**: Detecta referências circulares inválidas
- **Compilação segura**: Não trava durante a análise de tipos

### Flexibilidade
- **Auto-referência simples**: Structs podem se referenciar a si mesmos
- **Referências cruzadas**: Structs podem se referenciar mutuamente
- **Arrays de referências**: Suporte para estruturas complexas

### Simplicidade
- **Sintaxe intuitiva**: Palavra-chave `ref` clara e simples
- **Detecção automática**: Sistema identifica problemas automaticamente
- **Mensagens claras**: Erros de compilação informativos

## 🚀 Como Executar os Exemplos

### Compilação
```bash
uv run --compile <arquivo>.ml
```

### Exemplos de uso:
```bash
uv run --compile teste_struct_auto_ref.ml
uv run --compile arvore_binaria_completa.ml
uv run --compile lista_dupla_encadeada.ml
uv run --compile grafo_simples.ml
```

## 📊 Resultados Esperados

### Árvore Binária
- Criação de árvore com valores: 50, 30, 70, 20, 40, 60, 80
- Percorrimentos corretos (pré, em, pós-ordem)
- Busca eficiente de valores
- Cálculo de propriedades (altura, número de nós)

### Lista Dupla Encadeada
- Inserção e remoção em ambas as extremidades
- Navegação bidirecional
- Busca e contagem de elementos
- Manutenção correta dos ponteiros

### Grafo
- Criação de nós e arestas
- Verificação de conexões
- Contagem de vizinhos
- Busca de nós por ID

## 🔧 Implementação Técnica

### Sistema de Referências
- **Tipo `ReferenceType`**: Representa referências tipadas
- **Palavra-chave `ref`**: Sintaxe para criar referências
- **Placeholders seguros**: `void*` para evitar recursão

### Validação
- **Detecção de ciclos**: Identifica referências circulares
- **Verificação de tipos**: Valida existência de structs referenciados
- **Prevenção de recursão**: Evita loops infinitos

### Conversão LLVM
- **Ponteiros seguros**: Conversão para `void*` quando necessário
- **Forward declaration**: Suporte para referências futuras
- **Resolução em fases**: Processamento seguro de dependências

## 🎯 Conclusão

Os exemplos demonstram que a abordagem conservadora de auto-referência na MiniLang é:

- **Robusta**: Suporta estruturas de dados complexas
- **Segura**: Evita problemas de recursão infinita
- **Flexível**: Permite implementação de algoritmos avançados
- **Simples**: Mantém sintaxe intuitiva e clara

A implementação permite criar estruturas de dados sofisticadas mantendo a tipagem estática e a segurança da linguagem. 