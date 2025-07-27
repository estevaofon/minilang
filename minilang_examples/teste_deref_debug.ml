// ============================================
// MiniLang - Teste de Dereferenciação Debug
// Teste simples para debugar o problema
// ============================================

print("=== TESTE DE DEREFERENCIAÇÃO DEBUG ===")

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
    print("Função simples chamada")
end

print("✓ Função simples definida")

// ============================================
// FUNÇÃO QUE CHAMA COM CAMPO
// ============================================
func funcao_chamadora(node: ref TreeNode)
    if node != null then
        print("Chamando com campo...")
        funcao_simples(node.esquerda)  // ← AQUI ESTÁ O PROBLEMA!
    end
end

print("✓ Função chamadora definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Árvore criada")

// Teste: Chamar função que chama com campo
print("")
print("Teste: Chamando função que chama com campo...")
funcao_chamadora(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 