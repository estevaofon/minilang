// ============================================
// MiniLang - Teste ref + to_str
// Teste para identificar problema específico
// ============================================

print("=== TESTE REF + TO_STR ===")

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
// FUNÇÃO SIMPLES
// ============================================
func funcao_simples(node: ref TreeNode)
    print("Valor do nó: " + to_str(node.valor))
end

print("✓ Função simples definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Teste: Função simples
print("")
print("Teste: Função simples...")
funcao_simples(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 