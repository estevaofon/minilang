// ============================================
// MiniLang - Teste ref + Atribuição
// Teste para atribuições em structs passados por ref
// ============================================

print("=== TESTE REF + ATRIBUIÇÃO ===")

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
// FUNÇÃO QUE MODIFICA O STRUCT
// ============================================
func modificar_struct(node: ref TreeNode)
    print("Valor original: " + to_str(node.valor))
    
    // Modificar o valor
    node.valor = 42
    
    print("Valor modificado: " + to_str(node.valor))
end

print("✓ Função modificar_struct definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Teste: Modificar struct
print("")
print("Teste: Modificar struct...")
modificar_struct(ref raiz)

// Verificar se a modificação persistiu
print("")
print("Verificando se a modificação persistiu...")
print("Valor na main: " + to_str(raiz.valor))

print("")
print("=== TESTE CONCLUÍDO ===") 