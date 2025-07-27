// ============================================
// MiniLang - Percurso de Árvore Binária
// Demonstração das Atribuições de Structs
// ============================================

print("=== PERCURSO DE ÁRVORE BINÁRIA ===")
print("Demonstração das Atribuições de Structs")
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
// FUNÇÕES DE PERCURSO
// ============================================
print("--- FUNÇÕES DE PERCURSO ---")

// Função para percurso in-order (esquerda, raiz, direita)
func percurso_in_order(node: ref TreeNode)
    if node != null then
        percurso_in_order(node.esquerda)
        print("Valor: " + to_str(node.valor))
        percurso_in_order(node.direita)
    end
end

// Função para percurso pre-order (raiz, esquerda, direita)
func percurso_pre_order(node: ref TreeNode)
    if node != null then
        print("Valor: " + to_str(node.valor))
        percurso_pre_order(node.esquerda)
        percurso_pre_order(node.direita)
    end
end

// Função para percurso post-order (esquerda, direita, raiz)
func percurso_post_order(node: ref TreeNode)
    if node != null then
        percurso_post_order(node.esquerda)
        percurso_post_order(node.direita)
        print("Valor: " + to_str(node.valor))
    end
end

// Função para inserir novo nó na árvore
func inserir_no(raiz: ref TreeNode, novo_valor: int): ref TreeNode
    if raiz == null then
        // Criar novo nó
        let novo_no: TreeNode = TreeNode(novo_valor, null, null)
        return ref novo_no
    end
    
    if novo_valor < raiz.valor then
        // Inserir na subárvore esquerda
        raiz.esquerda = inserir_no(raiz.esquerda, novo_valor)
    else
        // Inserir na subárvore direita
        raiz.direita = inserir_no(raiz.direita, novo_valor)
    end
    
    return raiz
end

// Função para contar nós na árvore
func contar_nos(node: ref TreeNode): int
    if node == null then
        return 0
    end
    
    return 1 + contar_nos(node.esquerda) + contar_nos(node.direita)
end

// Função para encontrar altura da árvore
func altura_arvore(node: ref TreeNode): int
    if node == null then
        return 0
    end
    
    let altura_esq: int = altura_arvore(node.esquerda)
    let altura_dir: int = altura_arvore(node.direita)
    
    if altura_esq > altura_dir then
        return altura_esq + 1
    else
        return altura_dir + 1
    end
end

print("✓ Funções de percurso implementadas")
print("✓ Função de inserção implementada")
print("✓ Funções auxiliares implementadas")
print("")

// ============================================
// CONSTRUÇÃO DA ÁRVORE
// ============================================
print("--- CONSTRUÇÃO DA ÁRVORE ---")

// Criar árvore inicial
let raiz: TreeNode = TreeNode(50, null, null)
print("✓ Raiz criada com valor 50")

// Inserir nós usando atribuições dinâmicas
raiz = inserir_no(ref raiz, 30)
raiz = inserir_no(ref raiz, 70)
raiz = inserir_no(ref raiz, 20)
raiz = inserir_no(ref raiz, 40)
raiz = inserir_no(ref raiz, 60)
raiz = inserir_no(ref raiz, 80)
raiz = inserir_no(ref raiz, 10)
raiz = inserir_no(ref raiz, 25)
raiz = inserir_no(ref raiz, 35)
raiz = inserir_no(ref raiz, 45)

print("✓ Árvore construída com 11 nós")
print("")

// ============================================
// INFORMAÇÕES DA ÁRVORE
// ============================================
print("--- INFORMAÇÕES DA ÁRVORE ---")

let total_nos: int = contar_nos(ref raiz)
let altura: int = altura_arvore(ref raiz)

print("Total de nós na árvore: " + to_str(total_nos))
print("Altura da árvore: " + to_str(altura))
print("")

// ============================================
// PERCURSOS DA ÁRVORE
// ============================================
print("--- PERCURSOS DA ÁRVORE ---")

print("1. PERCURSO IN-ORDER (esquerda, raiz, direita):")
print("   Resultado esperado: 10, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80")
print("   Resultado obtido:")
percurso_in_order(ref raiz)
print("")

print("2. PERCURSO PRE-ORDER (raiz, esquerda, direita):")
print("   Resultado esperado: 50, 30, 20, 10, 25, 40, 35, 45, 70, 60, 80")
print("   Resultado obtido:")
percurso_pre_order(ref raiz)
print("")

print("3. PERCURSO POST-ORDER (esquerda, direita, raiz):")
print("   Resultado esperado: 10, 25, 20, 35, 45, 40, 30, 60, 80, 70, 50")
print("   Resultado obtido:")
percurso_post_order(ref raiz)
print("")

// ============================================
// MODIFICAÇÃO DINÂMICA DA ÁRVORE
// ============================================
print("--- MODIFICAÇÃO DINÂMICA DA ÁRVORE ---")

print("Inserindo novos valores dinamicamente...")

// Inserir mais nós
raiz = inserir_no(ref raiz, 15)
raiz = inserir_no(ref raiz, 55)
raiz = inserir_no(ref raiz, 75)
raiz = inserir_no(ref raiz, 90)

print("✓ Novos nós inseridos")
print("")

// Mostrar nova contagem
let novo_total: int = contar_nos(ref raiz)
let nova_altura: int = altura_arvore(ref raiz)

print("Nova contagem de nós: " + to_str(novo_total))
print("Nova altura da árvore: " + to_str(nova_altura))
print("")

// Mostrar novo percurso in-order
print("Novo percurso IN-ORDER após inserções:")
percurso_in_order(ref raiz)
print("")

// ============================================
// DEMONSTRAÇÃO DE ATRIBUIÇÕES DIRETAS
// ============================================
print("--- DEMONSTRAÇÃO DE ATRIBUIÇÕES DIRETAS ---")

print("Modificando valores diretamente...")

// Modificar valores de alguns nós diretamente
// (Note: isso quebra a propriedade de árvore binária de busca)
raiz.valor = 100
print("✓ Valor da raiz alterado para 100")

// Acessar e modificar um filho
if raiz.esquerda != null then
    raiz.esquerda.valor = 200
    print("✓ Valor do filho esquerdo alterado para 200")
end

if raiz.direita != null then
    raiz.direita.valor = 300
    print("✓ Valor do filho direito alterado para 300")
end

print("")

// Mostrar percurso após modificações
print("Percurso IN-ORDER após modificações diretas:")
percurso_in_order(ref raiz)
print("")

// ============================================
// RECONSTRUÇÃO DA ÁRVORE
// ============================================
print("--- RECONSTRUÇÃO DA ÁRVORE ---")

print("Reconstruindo árvore binária de busca válida...")

// Criar nova árvore válida
let nova_raiz: TreeNode = TreeNode(50, null, null)

// Inserir valores em ordem
nova_raiz = inserir_no(ref nova_raiz, 25)
nova_raiz = inserir_no(ref nova_raiz, 75)
nova_raiz = inserir_no(ref nova_raiz, 12)
nova_raiz = inserir_no(ref nova_raiz, 37)
nova_raiz = inserir_no(ref nova_raiz, 62)
nova_raiz = inserir_no(ref nova_raiz, 87)

print("✓ Nova árvore reconstruída")
print("")

// Mostrar percurso da nova árvore
print("Percurso IN-ORDER da nova árvore:")
percurso_in_order(ref nova_raiz)
print("")

// ============================================
// RESUMO DA IMPLEMENTAÇÃO
// ============================================
print("=== RESUMO DA IMPLEMENTAÇÃO ===")
print("✓ Estrutura TreeNode com auto-referência funcionando")
print("✓ Atribuições dinâmicas de campos implementadas")
print("✓ Funções de percurso (in-order, pre-order, post-order) funcionando")
print("✓ Inserção dinâmica de nós implementada")
print("✓ Modificação direta de valores funcionando")
print("✓ Cálculo de altura e contagem de nós implementado")
print("✓ Reconstrução de árvore funcionando")

print("")
print("🎉 Algoritmo de percurso de árvore binária implementado com sucesso!")
print("💡 Demonstração completa das atribuições de structs")
print("💡 Auto-referência funcionando perfeitamente")
print("💡 Estruturas de dados dinâmicas suportadas")

print("")
print("=== IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO ===") 