// ============================================
// MiniLang - Teste Debug Null
// Teste para debugar problema de verificação de null
// ============================================

print("=== TESTE DEBUG NULL ===")

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
// FUNÇÃO PARA VERIFICAR NULL
// ============================================
func verificar_null(node: ref TreeNode)
    print("Verificando se node é null...")
    
    if node == null then
        print("✓ node é null")
    else
        print("✓ node NÃO é null, valor: " + to_str(node.valor))
        
        print("Verificando se node.esquerda é null...")
        if node.esquerda == null then
            print("✓ node.esquerda é null")
        else
            print("✓ node.esquerda NÃO é null, valor: " + to_str(node.esquerda.valor))
        end
    end
end

print("✓ Função verificar_null definida")

// ============================================
// FUNÇÃO RECURSIVA SIMPLES
// ============================================
func recursiva_simples(node: ref TreeNode)
    print("Entrando na recursiva...")
    
    if node == null then
        print("✓ Saindo - node é null")
        return
    end
    
    print("✓ Processando node: " + to_str(node.valor))
    
    // Verificar explicitamente se esquerda é null
    if node.esquerda == null then
        print("✓ Saindo - esquerda é null")
        return
    end
    
    print("✓ Chamando recursivamente para esquerda...")
    recursiva_simples(node.esquerda)
    print("✓ Voltou da recursão")
end

print("✓ Função recursiva_simples definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(10, null, null)
let filho: TreeNode = TreeNode(5, null, null)

print("✓ Árvore criada")

// Conectar filho
raiz.esquerda = ref filho

print("✓ Filho conectado")

// Teste 1: Verificar null
print("")
print("Teste 1: Verificar null...")
verificar_null(ref raiz)

// Teste 2: Recursiva simples
print("")
print("Teste 2: Recursiva simples...")
recursiva_simples(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 