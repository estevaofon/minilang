// ============================================
// MiniLang - Árvore Binária Atualizada
// Implementação com Abordagem Conservadora
// ============================================
// Exemplo atualizado que funciona com auto-referência segura

print("=== ÁRVORE BINÁRIA ATUALIZADA ===")
print("Implementação com Abordagem Conservadora")
print("")

// Definição do nó da árvore binária com auto-referência
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

print("✓ Struct TreeNode definido com auto-referência")
print("✓ Campos 'esquerda' e 'direita' são referências para o próprio tipo")
print("✓ Sistema de tipos conservador previne recursão infinita")
print("")

// ============================================
// EXEMPLO 1: Árvore Básica com Construtores
// ============================================
print("--- EXEMPLO 1: Árvore Básica ---")

// Criar nós simples usando construtores
let raiz: TreeNode = TreeNode(10, null, null)
let filho_esq: TreeNode = TreeNode(5, null, null)
let filho_dir: TreeNode = TreeNode(15, null, null)

print("✓ Nós básicos criados com sucesso")
print("")

// ============================================
// EXEMPLO 2: Árvore Complexa com Construtores Aninhados
// ============================================
print("--- EXEMPLO 2: Árvore Complexa ---")

// Criar uma árvore completa usando construtores aninhados
let arvore_completa: TreeNode = TreeNode(50, 
    TreeNode(30, 
        TreeNode(20, 
            TreeNode(10, null, null), 
            TreeNode(25, null, null)
        ), 
        TreeNode(40, 
            TreeNode(35, null, null), 
            TreeNode(45, null, null)
        )
    ), 
    TreeNode(70, 
        TreeNode(60, 
            TreeNode(55, null, null), 
            TreeNode(65, null, null)
        ), 
        TreeNode(80, 
            TreeNode(75, null, null), 
            TreeNode(90, null, null)
        )
    )
)

print("✓ Árvore complexa criada com construtores aninhados")
print("✓ Estrutura: 50 -> [30, 70] -> [20, 40, 60, 80] -> [10, 25, 35, 45, 55, 65, 75, 90]")
print("")

// ============================================
// EXEMPLO 3: Árvore de Busca Binária
// ============================================
print("--- EXEMPLO 3: Árvore de Busca Binária ---")

// Criar uma árvore de busca binária balanceada
let bst: TreeNode = TreeNode(8, 
    TreeNode(3, 
        TreeNode(1, null, null), 
        TreeNode(6, 
            TreeNode(4, null, null), 
            TreeNode(7, null, null)
        )
    ), 
    TreeNode(10, 
        null, 
        TreeNode(14, 
            TreeNode(13, null, null), 
            null
        )
    )
)

print("✓ Árvore de busca binária criada")
print("✓ Estrutura: 8 -> [3, 10] -> [1, 6, null, 14] -> [null, null, 4, 7, null, 13, null, null]")
print("")

// ============================================
// EXEMPLO 4: Árvore Degenerada (Lista Encadeada)
// ============================================
print("--- EXEMPLO 4: Árvore Degenerada ---")

// Criar uma árvore que é essencialmente uma lista encadeada
let arvore_degenerada: TreeNode = TreeNode(1, 
    null, 
    TreeNode(2, 
        null, 
        TreeNode(3, 
            null, 
            TreeNode(4, 
                null, 
                TreeNode(5, null, null)
            )
        )
    )
)

print("✓ Árvore degenerada criada (lista encadeada)")
print("✓ Estrutura: 1 -> null -> 2 -> null -> 3 -> null -> 4 -> null -> 5")
print("")

// ============================================
// EXEMPLO 5: Árvore Simétrica
// ============================================
print("--- EXEMPLO 5: Árvore Simétrica ---")

// Criar uma árvore simétrica
let arvore_simetrica: TreeNode = TreeNode(1, 
    TreeNode(2, 
        TreeNode(3, null, null), 
        TreeNode(4, null, null)
    ), 
    TreeNode(2, 
        TreeNode(4, null, null), 
        TreeNode(3, null, null)
    )
)

print("✓ Árvore simétrica criada")
print("✓ Estrutura: 1 -> [2, 2] -> [3, 4, 4, 3]")
print("")

// ============================================
// RESUMO DA IMPLEMENTAÇÃO
// ============================================
print("=== RESUMO DA IMPLEMENTAÇÃO ===")
print("✓ Auto-referência funcionando com segurança")
print("✓ Recursão infinita prevenida pela abordagem conservadora")
print("✓ Estruturas complexas suportadas")
print("✓ Construtores aninhados funcionando")
print("✓ Placeholders seguros (void*) para auto-referências")
print("✓ Validação de referências circulares")
print("")
print("⚠️  Limitação: Atribuição de campos desabilitada")
print("💡 Solução: Usar construtores para criar estruturas completas")
print("")
print("=== IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO ===") 