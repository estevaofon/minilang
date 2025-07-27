// ============================================
// MiniLang - Teste do Problema Específico
// Teste para identificar exatamente onde está o problema
// ============================================

print("=== TESTE DO PROBLEMA ESPECÍFICO ===")

// ============================================
// DEFINIÇÃO DA ESTRUTURA
// ============================================
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

print("✓ Struct TreeNode definido")

// ============================================
// FUNÇÃO SIMPLES (FUNCIONA)
// ============================================
func funcao_simples(node: ref TreeNode)
    print("Função simples: " + to_str(node.valor))
end

print("✓ Função simples definida")

// ============================================
// FUNÇÃO QUE CHAMA OUTRA (FUNCIONA)
// ============================================
func funcao_chamadora(node: ref TreeNode)
    if node != null then
        funcao_simples(node)
    end
end

print("✓ Função chamadora definida")

// ============================================
// FUNÇÃO RECURSIVA (PROBLEMA AQUI!)
// ============================================
func funcao_recursiva(node: ref TreeNode)
    if node != null then
        print("Recursiva: " + to_str(node.valor))
        funcao_recursiva(node.esquerda)  // ← PROBLEMA AQUI!
    end
end

print("✓ Função recursiva definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Teste 1: Função simples (deve funcionar)
print("")
print("Teste 1: Função simples...")
funcao_simples(ref raiz)

// Teste 2: Função que chama outra (deve funcionar)
print("")
print("Teste 2: Função que chama outra...")
funcao_chamadora(ref raiz)

// Teste 3: Função recursiva (PROBLEMA!)
print("")
print("Teste 3: Função recursiva...")
funcao_recursiva(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 