// ============================================
// MiniLang - Teste de Acesso a Campos
// Teste específico para debugar o problema
// ============================================

print("=== TESTE DE ACESSO A CAMPOS ===")

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
// FUNÇÃO QUE ACESSA CAMPOS
// ============================================
func acessar_campo(node: ref TreeNode)
    print("Função acessar_campo definida")
    print("Valor do nó: " + to_str(node.valor))
end

print("✓ Função acessar_campo definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Teste: Chamar função sem acessar campos
print("")
print("Teste: Chamando função...")
acessar_campo(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 