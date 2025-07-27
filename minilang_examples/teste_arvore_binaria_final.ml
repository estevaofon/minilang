// ============================================
// MiniLang - Teste Árvore Binária Final
// Demonstração completa de árvore binária com auto-referência
// ============================================

print("=== TESTE ÁRVORE BINÁRIA FINAL ===")

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
// FUNÇÃO DE INSERÇÃO
// ============================================
func inserir(node: ref TreeNode, valor: int)
    if node == null then
        return
    end
    
    if valor < node.valor then
        if node.esquerda == null then
            node.esquerda = ref TreeNode(valor, null, null)
        else
            inserir(node.esquerda, valor)
        end
    else
        if node.direita == null then
            node.direita = ref TreeNode(valor, null, null)
        else
            inserir(node.direita, valor)
        end
    end
end

print("✓ Função inserir definida")

// ============================================
// FUNÇÃO DE PERCURSO EM ORDEM
// ============================================
func percorrer_em_ordem(node: ref TreeNode)
    if node != null then
        percorrer_em_ordem(node.esquerda)
        print("Visitando: " + to_str(node.valor))
        percorrer_em_ordem(node.direita)
    end
end

print("✓ Função percorrer_em_ordem definida")

// ============================================
// FUNÇÃO DE PERCURSO PRÉ-ORDEM
// ============================================
func percorrer_pre_ordem(node: ref TreeNode)
    if node != null then
        print("Visitando: " + to_str(node.valor))
        percorrer_pre_ordem(node.esquerda)
        percorrer_pre_ordem(node.direita)
    end
end

print("✓ Função percorrer_pre_ordem definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(8, null, null)
print("✓ Raiz criada com valor: 8")

// Inserir vários nós para criar uma árvore interessante
inserir(ref raiz, 3)
inserir(ref raiz, 10)
inserir(ref raiz, 1)
inserir(ref raiz, 6)
inserir(ref raiz, 14)
inserir(ref raiz, 4)
inserir(ref raiz, 7)
inserir(ref raiz, 13)

print("✓ Árvore construída com 9 nós")

print("")
print("=== PERCURSO EM ORDEM (IN-ORDER) ===")
print("Esperado: 1, 3, 4, 6, 7, 8, 10, 13, 14")
percorrer_em_ordem(ref raiz)

print("")
print("=== PERCURSO PRÉ-ORDEM (PRE-ORDER) ===")
print("Esperado: 8, 3, 1, 6, 4, 7, 10, 14, 13")
percorrer_pre_ordem(ref raiz)

print("")
print("=== TESTE CONCLUÍDO COM SUCESSO ===")
print("✓ Atribuição dinâmica de structs funcionando")
print("✓ Auto-referência em structs funcionando")
print("✓ Recursão com referências funcionando")
print("✓ Árvore binária completa implementada") 