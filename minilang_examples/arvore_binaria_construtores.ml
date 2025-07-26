// Árvore binária usando apenas construtores - sem atribuição de campos
print("=== ÁRVORE BINÁRIA COM CONSTRUTORES ===")

// Definição do nó da árvore binária com auto-referência
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

print("✓ Struct TreeNode definido com auto-referência")

// Criar uma árvore simples usando apenas construtores
let raiz: TreeNode = TreeNode(10, null, null)
let filho_esq: TreeNode = TreeNode(5, null, null)
let filho_dir: TreeNode = TreeNode(15, null, null)

print("✓ Árvore básica criada com construtores")

// Criar uma árvore mais complexa usando construtores aninhados
let arvore_complexa: TreeNode = TreeNode(10, 
    TreeNode(5, 
        TreeNode(3, null, null), 
        TreeNode(7, null, null)
    ), 
    TreeNode(15, 
        TreeNode(12, null, null), 
        TreeNode(20, null, null)
    )
)

print("✓ Árvore complexa criada usando construtores aninhados")

print("=== TESTE CONCLUÍDO COM SUCESSO ===") 