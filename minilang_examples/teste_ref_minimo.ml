// ============================================
// MiniLang - Teste Mínimo de Referências
// Verificação do problema com ref
// ============================================

print("=== TESTE MÍNIMO DE REFERÊNCIAS ===")

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
// TESTE 1: FUNÇÃO SEM TIPO DE RETORNO
// ============================================
func teste1(node: ref TreeNode)
    print("Teste 1 funcionando")
end

print("✓ Função sem tipo de retorno definida")

// ============================================
// TESTE 2: FUNÇÃO COM TIPO DE RETORNO SIMPLES
// ============================================
func teste2(node: ref TreeNode): int
    return 42
end

print("✓ Função com tipo de retorno simples definida")

// ============================================
// TESTE 3: FUNÇÃO COM TIPO DE RETORNO REF
// ============================================
func teste3(node: ref TreeNode): ref TreeNode
    return node
end

print("✓ Função com tipo de retorno ref definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

teste1(ref raiz)
let resultado: int = teste2(ref raiz)
print("Resultado do teste 2: " + to_str(resultado))

let resultado_ref: ref TreeNode = teste3(ref raiz)
print("✓ Teste 3 executado")

print("=== TESTE MÍNIMO CONCLUÍDO ===") 