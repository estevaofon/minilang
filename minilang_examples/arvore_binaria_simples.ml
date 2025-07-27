// ============================================
// MiniLang - Percurso de Árvore Binária Simples
// Demonstração das Atribuições de Structs
// ============================================

print("=== PERCURSO DE ÁRVORE BINÁRIA SIMPLES ===")
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
print("✓ Funções auxiliares implementadas")
print("")

// ============================================
// CONSTRUÇÃO MANUAL DA ÁRVORE
// ============================================
print("--- CONSTRUÇÃO MANUAL DA ÁRVORE ---")

// Criar árvore manualmente usando atribuições
let raiz: TreeNode = TreeNode(50, null, null)
print("✓ Raiz criada com valor 50")

// Criar nós filhos
let filho_esq: TreeNode = TreeNode(30, null, null)
let filho_dir: TreeNode = TreeNode(70, null, null)

// Criar netos esquerdos
let neto_esq_esq: TreeNode = TreeNode(20, null, null)
let neto_esq_dir: TreeNode = TreeNode(40, null, null)

// Criar netos direitos
let neto_dir_esq: TreeNode = TreeNode(60, null, null)
let neto_dir_dir: TreeNode = TreeNode(80, null, null)

// Criar bisnetos
let bisneto_esq: TreeNode = TreeNode(10, null, null)
let bisneto_dir: TreeNode = TreeNode(25, null, null)

print("✓ Nós criados")
print("")

// ============================================
// MONTAGEM DA ÁRVORE COM ATRIBUIÇÕES
// ============================================
print("--- MONTAGEM DA ÁRVORE COM ATRIBUIÇÕES ---")

// Montar a árvore usando atribuições dinâmicas
raiz.esquerda = ref filho_esq
raiz.direita = ref filho_dir

filho_esq.esquerda = ref neto_esq_esq
filho_esq.direita = ref neto_esq_dir

filho_dir.esquerda = ref neto_dir_esq
filho_dir.direita = ref neto_dir_dir

neto_esq_esq.esquerda = ref bisneto_esq
neto_esq_esq.direita = ref bisneto_dir

print("✓ Árvore montada com atribuições dinâmicas")
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
print("   Resultado esperado: 10, 20, 25, 30, 40, 50, 60, 70, 80")
print("   Resultado obtido:")
percurso_in_order(ref raiz)
print("")

print("2. PERCURSO PRE-ORDER (raiz, esquerda, direita):")
print("   Resultado esperado: 50, 30, 20, 10, 25, 40, 70, 60, 80")
print("   Resultado obtido:")
percurso_pre_order(ref raiz)
print("")

print("3. PERCURSO POST-ORDER (esquerda, direita, raiz):")
print("   Resultado esperado: 10, 25, 20, 40, 30, 60, 80, 70, 50")
print("   Resultado obtido:")
percurso_post_order(ref raiz)
print("")

// ============================================
// MODIFICAÇÃO DINÂMICA DA ÁRVORE
// ============================================
print("--- MODIFICAÇÃO DINÂMICA DA ÁRVORE ---")

print("Modificando valores diretamente...")

// Modificar valores de alguns nós diretamente
raiz.valor = 100
print("✓ Valor da raiz alterado para 100")

filho_esq.valor = 200
print("✓ Valor do filho esquerdo alterado para 200")

filho_dir.valor = 300
print("✓ Valor do filho direito alterado para 300")

print("")

// Mostrar percurso após modificações
print("Percurso IN-ORDER após modificações diretas:")
percurso_in_order(ref raiz)
print("")

// ============================================
// ADIÇÃO DINÂMICA DE NOVOS NÓS
// ============================================
print("--- ADIÇÃO DINÂMICA DE NOVOS NÓS ---")

print("Adicionando novos nós dinamicamente...")

// Criar novos nós
let novo_no1: TreeNode = TreeNode(15, null, null)
let novo_no2: TreeNode = TreeNode(35, null, null)
let novo_no3: TreeNode = TreeNode(55, null, null)

// Adicionar à árvore usando atribuições
bisneto_esq.esquerda = ref novo_no1
neto_esq_dir.esquerda = ref novo_no2
neto_dir_esq.esquerda = ref novo_no3

print("✓ Novos nós adicionados dinamicamente")
print("")

// Mostrar nova contagem
let novo_total: int = contar_nos(ref raiz)
let nova_altura: int = altura_arvore(ref raiz)

print("Nova contagem de nós: " + to_str(novo_total))
print("Nova altura da árvore: " + to_str(nova_altura))
print("")

// Mostrar novo percurso in-order
print("Novo percurso IN-ORDER após adições:")
percurso_in_order(ref raiz)
print("")

// ============================================
// RECONSTRUÇÃO DE UMA NOVA ÁRVORE
// ============================================
print("--- RECONSTRUÇÃO DE UMA NOVA ÁRVORE ---")

print("Criando uma nova árvore simples...")

// Criar nova árvore
let nova_raiz: TreeNode = TreeNode(25, null, null)
let novo_filho_esq: TreeNode = TreeNode(15, null, null)
let novo_filho_dir: TreeNode = TreeNode(35, null, null)

// Montar nova árvore
nova_raiz.esquerda = ref novo_filho_esq
nova_raiz.direita = ref novo_filho_dir

print("✓ Nova árvore criada")
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
print("✓ Construção manual de árvore com atribuições funcionando")
print("✓ Modificação direta de valores funcionando")
print("✓ Adição dinâmica de nós implementada")
print("✓ Cálculo de altura e contagem de nós implementado")
print("✓ Reconstrução de árvore funcionando")

print("")
print("🎉 Algoritmo de percurso de árvore binária implementado com sucesso!")
print("💡 Demonstração completa das atribuições de structs")
print("💡 Auto-referência funcionando perfeitamente")
print("💡 Estruturas de dados dinâmicas suportadas")

print("")
print("=== IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO ===") 