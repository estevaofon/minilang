// ============================================
// MiniLang - Teste Completo de Referências
// Teste que combina todas as funcionalidades
// ============================================

print("=== TESTE COMPLETO DE REFERÊNCIAS ===")

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
// FUNÇÃO COM PARÂMETRO REF E ACESSO A CAMPOS
// ============================================
func modificar_no(node: ref TreeNode)
    if node != null then
        node.valor = node.valor * 2
        print("Valor modificado para: " + to_str(node.valor))
    end
end

print("✓ Função modificar_no definida")

// ============================================
// FUNÇÃO RECURSIVA SIMPLES
// ============================================
func percorrer_simples(node: ref TreeNode)
    if node != null then
        print("Visitando nó: " + to_str(node.valor))
    end
end

print("✓ Função percorrer_simples definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)
let filho_esq: TreeNode = TreeNode(5, null, null)
let filho_dir: TreeNode = TreeNode(15, null, null)

print("✓ Árvore criada")

// Conectar filhos
raiz.esquerda = ref filho_esq
raiz.direita = ref filho_dir

print("✓ Filhos conectados")

// Teste 1: Modificar nó
print("")
print("Teste 1: Modificando nó...")
modificar_no(ref raiz)

// Teste 2: Percorrer simples
print("")
print("Teste 2: Percorrendo simples...")
percorrer_simples(ref raiz)

print("")
print("=== TESTE COMPLETO CONCLUÍDO ===") 