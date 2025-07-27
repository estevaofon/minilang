// ============================================
// MiniLang - Teste de Recursão Simples
// Teste para isolar problema de recursão
// ============================================

print("=== TESTE DE RECURSÃO SIMPLES ===")

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
// FUNÇÃO RECURSIVA SIMPLES
// ============================================
func percorrer_simples(node: ref TreeNode)
    if node != null then
        print("Visitando nó: " + to_str(node.valor))
        // Chamada recursiva simples
        percorrer_simples(node.esquerda)
    end
end

print("✓ Função recursiva simples definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Teste: Chamar função recursiva
print("")
print("Teste: Chamando função recursiva...")
percorrer_simples(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 