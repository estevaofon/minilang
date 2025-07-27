// ============================================
// MiniLang - Teste de Chamada Simples
// Teste para isolar problema de chamada
// ============================================

print("=== TESTE DE CHAMADA SIMPLES ===")

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
// FUNÇÃO SIMPLES SEM RECURSÃO
// ============================================
func funcao_simples(node: ref TreeNode)
    print("Função simples chamada")
end

print("✓ Função simples definida")

// ============================================
// FUNÇÃO QUE CHAMA OUTRA FUNÇÃO
// ============================================
func funcao_chamadora(node: ref TreeNode)
    if node != null then
        print("Chamando outra função...")
        funcao_simples(node)  // ← Aqui está o problema!
    end
end

print("✓ Função chamadora definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Teste: Chamar função que chama outra função
print("")
print("Teste: Chamando função que chama outra...")
funcao_chamadora(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 