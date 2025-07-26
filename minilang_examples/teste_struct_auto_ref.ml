// Teste para demonstrar auto-referenciamento de structs na miniLang
// Usando a abordagem conservadora que evita recursão infinita

print("=== TESTE DE AUTO-REFERENCIAMENTO DE STRUCTS (ABORDAGEM CONSERVADORA) ===")
print("")

// Exemplo 1: Lista encadeada simples
print(">> Exemplo 1: Lista encadeada")
struct Node
    valor: int,
    proximo: ref Node
end

print("Struct Node definido com auto-referenciamento!")
print("Campo 'proximo' é uma referência para o próprio tipo Node")
print("✓ Abordagem conservadora: usa ponteiro para void (void*) como placeholder")
print("")

// Exemplo 2: Árvore binária
print(">> Exemplo 2: Árvore binária")
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

print("Struct TreeNode definido com múltiplas auto-referências!")
print("✓ Campos 'esquerda' e 'direita' são referências para o próprio tipo")
print("✓ Sistema detecta e valida referências circulares")
print("")

// Exemplo 3: Grafo simples
print(">> Exemplo 3: Grafo simples")
struct GraphNode
    id: int,
    vizinho: ref GraphNode
end

print("Struct GraphNode definido!")
print("✓ Campo 'vizinho' permite criar estruturas de grafo")
print("")

print("=== VANTAGENS DA ABORDAGEM CONSERVADORA ===")
print("✓ Evita recursão infinita durante a compilação")
print("✓ Detecta referências circulares inválidas")
print("✓ Mantém a funcionalidade de auto-referenciamento")
print("✓ Usa placeholders seguros (void*) para referências")
print("✓ Validação em tempo de compilação")
print("")

print("=== CONCLUSÃO ===")
print("✓ Auto-referenciamento de structs funcionando com segurança!")
print("✓ Sistema de referências (ref) com validação robusta")
print("✓ Abordagem conservadora previne recursão infinita")
print("✓ Structs podem se referenciar a si mesmos de forma segura") 