// ============================================
// MiniLang - Teste Simples de Referências
// Verificação básica de ref em funções
// ============================================

print("=== TESTE SIMPLES DE REFERÊNCIAS ===")
print("Verificação básica de ref em funções")
print("")

// ============================================
// DEFINIÇÃO DA ESTRUTURA
// ============================================
print("--- DEFINIÇÃO DA ESTRUTURA ---")

// Definir nó da árvore binária
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

print("✓ Struct TreeNode definido com auto-referência")
print("")

// ============================================
// TESTE 1: FUNÇÃO COM PARÂMETRO REF
// ============================================
print("--- TESTE 1: FUNÇÃO COM PARÂMETRO REF ---")

// Função que recebe uma referência como parâmetro
func modificar_no(node: ref TreeNode)
    if node != null then
        node.valor = node.valor * 2
        print("Valor modificado para: " + to_str(node.valor))
    end
end

print("✓ Função com parâmetro ref definida")

// ============================================
// TESTE 2: FUNÇÃO QUE RETORNA REF
// ============================================
print("--- TESTE 2: FUNÇÃO QUE RETORNA REF ---")

// Função que retorna uma referência
func obter_filho_esquerdo(node: ref TreeNode): ref TreeNode
    if node != null then
        return node.esquerda
    else
        return null
    end
end

print("✓ Função que retorna ref definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
print("--- EXECUÇÃO DOS TESTES ---")

// Criar árvore de teste
let raiz: TreeNode = TreeNode(10, null, null)
let filho_esq: TreeNode = TreeNode(5, null, null)

print("✓ Árvore de teste criada")

// Conectar filho
raiz.esquerda = ref filho_esq

// Teste 1: Modificar nó usando função com parâmetro ref
print("")
print("Teste 1: Modificando nó...")
modificar_no(ref raiz)

// Teste 2: Obter filho usando função que retorna ref
print("")
print("Teste 2: Obtendo filho esquerdo...")
let filho_obtido: ref TreeNode = obter_filho_esquerdo(ref raiz)
if filho_obtido != null then
    print("Filho esquerdo encontrado com valor: " + to_str(filho_obtido.valor))
else
    print("Filho esquerdo é null")
end

// ============================================
// RESUMO DOS TESTES
// ============================================
print("")
print("=== RESUMO DOS TESTES ===")
print("✓ Parâmetros ref em funções: TESTADO")
print("✓ Retorno de referências: TESTADO")

print("")
print("🎉 TESTES DE REFERÊNCIAS SIMPLES CONCLUÍDOS!")
print("💡 Verificação de suporte a ref em funções")

print("")
print("=== TESTES CONCLUÍDOS ===") 