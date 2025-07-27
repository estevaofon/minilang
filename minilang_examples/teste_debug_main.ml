// ============================================
// MiniLang - Teste Debug Main
// Teste simples para debugar problema na main
// ============================================

print("=== TESTE DEBUG MAIN ===")

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
    print("Valor na função: " + to_str(node.valor))
end

print("✓ Função simples definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Verificar valor antes da função
print("Valor antes da função: " + to_str(raiz.valor))

// Chamar função
print("")
print("Chamando função...")
funcao_simples(ref raiz)

// Verificar valor depois da função
print("")
print("Valor depois da função: " + to_str(raiz.valor))

print("")
print("=== TESTE CONCLUÍDO ===") 