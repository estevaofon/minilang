# Auto-Referenciamento de Structs na MiniLang (Abordagem Conservadora)

## Problema Original

Originalmente, a MiniLang não suportava structs que se auto-referenciam, como:

```minilang
struct Node
    valor: int,
    proximo: Node  // ❌ Erro: dependência circular
end
```

Isso impedia a criação de estruturas de dados como listas encadeadas, árvores binárias, grafos, etc.

## Problema da Recursão Infinita

A implementação anterior podia causar recursão infinita durante a compilação quando:

1. Um struct se referenciava a si mesmo
2. Structs se referenciam mutuamente em ciclos complexos
3. Referências para structs não definidos

## Solução: Abordagem Conservadora

### 1. Sistema de Referências (`ref`)

Implementamos um sistema de referências usando a palavra-chave `ref`:

```minilang
struct Node
    valor: int,
    proximo: ref Node  // ✅ Referência para o próprio tipo
end
```

### 2. Tipo de Referência (`ReferenceType`)

```python
@dataclass
class ReferenceType(Type):
    """Tipo para referências que permitem auto-referenciamento"""
    target_type: Type
    is_mutable: bool = True
```

### 3. Abordagem Conservadora para Conversão

**Antes (problemático):**
```python
elif isinstance(ml_type, ReferenceType):
    target_type = self._convert_type(ml_type.target_type)  # ❌ Recursão infinita
    return target_type.as_pointer()
```

**Agora (conservador):**
```python
elif isinstance(ml_type, ReferenceType):
    if isinstance(ml_type.target_type, StructType):
        # Para referências a structs, usar ponteiro para void como placeholder
        return ir.IntType(8).as_pointer()  # void* equivalente
    else:
        # Para outros tipos, converter normalmente
        target_type = self._convert_type(ml_type.target_type)
        return target_type.as_pointer()
```

### 4. Validação de Referências Circulares

Implementamos validação robusta:

```python
def _validate_circular_references(self, struct_name: str, visited: set = None) -> bool:
    """
    Valida se um struct tem referências circulares válidas.
    Retorna True se as referências são válidas, False se há recursão infinita.
    """
    # Implementação que detecta ciclos inválidos
```

### 5. Processamento em Duas Fases

1. **Fase 1**: Criar todos os structs com placeholders (`void*`)
2. **Fase 2**: Validar referências circulares
3. **Fase 3**: Resolver referências quando necessário

## Vantagens da Abordagem Conservadora

### 1. **Segurança**
- Evita recursão infinita durante compilação
- Detecta referências circulares inválidas
- Validação em tempo de compilação

### 2. **Robustez**
- Usa placeholders seguros (`void*`) para referências
- Mantém funcionalidade de auto-referenciamento
- Suporta estruturas complexas

### 3. **Simplicidade**
- Sintaxe intuitiva com `ref`
- Detecção automática de problemas
- Mensagens de erro claras

## Como Usar

### Lista Encadeada

```minilang
struct Node
    valor: int,
    proximo: ref Node
end

// Criar lista: 1 -> 2 -> 3
let node3: Node = Node(3, null)
let node2: Node = Node(2, ref node3)
let node1: Node = Node(1, ref node2)
```

### Árvore Binária

```minilang
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

// Criar árvore:
//     5
//    / \
//   3   7
let folha3: TreeNode = TreeNode(3, null, null)
let folha7: TreeNode = TreeNode(7, null, null)
let raiz: TreeNode = TreeNode(5, ref folha3, ref folha7)
```

### Referências Circulares Válidas

```minilang
struct Pessoa
    nome: string,
    amigo: ref Amigo
end

struct Amigo
    nome: string,
    pessoa: ref Pessoa
end
```

## Detecção de Erros

### Referência para Struct Não Definido

```minilang
struct Teste
    valor: int,
    campo: ref StructNaoExiste  // ❌ Erro: struct não definido
end
```

**Erro gerado:**
```
Struct 'Teste' tem referências circulares inválidas que podem causar recursão infinita
```

## Implementação Técnica

### Lexer
- Adicionada palavra-chave `ref`
- Reconhecida como `TokenType.REF`

### Parser
- Suporte para `ref Tipo` na função `_parse_type()`
- Forward declaration para tipos não definidos

### Code Generator
- **Abordagem conservadora**: Usa `void*` para referências a structs
- **Validação robusta**: Detecta referências circulares inválidas
- **Processamento seguro**: Evita recursão infinita

## Exemplos de Uso

Veja os arquivos de teste:
- `teste_struct_auto_ref.ml` - Exemplo básico com abordagem conservadora
- `teste_referencia_circular_invalida.ml` - Demonstração de detecção de erros
- `exemplo_lista_encadeada.ml` - Implementação completa de lista encadeada

## Conclusão

A abordagem conservadora resolve completamente o problema de recursão infinita mantendo toda a funcionalidade de auto-referenciamento. O sistema agora é:

- **Seguro**: Evita recursão infinita
- **Robusto**: Detecta problemas em tempo de compilação
- **Flexível**: Suporta estruturas de dados complexas
- **Simples**: Mantém sintaxe intuitiva

O sistema de referências com validação robusta permite estruturas de dados complexas mantendo a tipagem estática da MiniLang. 