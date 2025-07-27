// ============================================
// MiniLang - Teste Debug de Referências
// Teste simples para isolar o problema
// ============================================

print("=== TESTE DEBUG DE REFERÊNCIAS ===")

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
// FUNÇÃO SIMPLES SEM PARÂMETROS
// ============================================
func teste_simples()
    print("Função simples funcionando")
end

print("✓ Função simples definida")

// ============================================
// FUNÇÃO COM PARÂMETRO REF
// ============================================
func modificar_no(node: ref TreeNode)
    print("Função com parâmetro ref definida")
end

print("✓ Função com parâmetro ref definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Teste 1: Função simples
print("")
print("Teste 1: Função simples...")
teste_simples()

// Teste 2: Função com parâmetro ref
print("")
print("Teste 2: Função com parâmetro ref...")
modificar_no(ref raiz)

print("")
print("=== TESTE DEBUG CONCLUÍDO ===") 