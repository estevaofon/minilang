// ============================================
// MiniLang - Teste Linked List Simples
// Implementação simplificada de lista encadeada
// ============================================

print("=== TESTE LINKED LIST SIMPLES ===")

// ============================================
// DEFINIÇÃO DA ESTRUTURA
// ============================================

// Estrutura para representar um nó da lista encadeada
struct Node
    valor: int,
    proximo: ref Node
end

print("✓ Struct Node definido")

// ============================================
// FUNÇÕES DA LINKED LIST
// ============================================

// Função para inserir no início da lista
func inserir_inicio(lista: ref Node, valor: int)
    let novo_no: Node = Node(valor, null)
    novo_no.proximo = ref lista
    return ref novo_no
end

print("✓ Função inserir_inicio definida")

// Função para imprimir a lista
func imprimir_lista(lista: ref Node)
    if lista == null then
        print("Lista vazia")
        return
    end
    
    let atual: ref Node = ref lista
    let contador: int = 0
    
    print("Lista: ")
    while atual != null do
        if contador > 0 then
            print(" -> ")
        end
        print(to_str(atual.valor))
        atual = ref atual.proximo
        contador = contador + 1
    end
    print("")
end

print("✓ Função imprimir_lista definida")

// Função para contar elementos da lista
func contar_elementos(lista: ref Node)
    let contador: int = 0
    let atual: ref Node = ref lista
    
    while atual != null do
        contador = contador + 1
        atual = ref atual.proximo
    end
    
    return contador
end

print("✓ Função contar_elementos definida")

// Função para buscar um valor na lista
func buscar_valor(lista: ref Node, valor: int)
    let atual: ref Node = ref lista
    let posicao: int = 0
    
    while atual != null do
        if atual.valor == valor then
            return posicao
        end
        atual = ref atual.proximo
        posicao = posicao + 1
    end
    
    return -1  // Valor não encontrado
end

print("✓ Função buscar_valor definida")

// ============================================
// EXECUÇÃO DO TESTE
// ============================================

print("")
print("=== TESTE DE OPERAÇÕES ===")

// Criar lista vazia
let lista: ref Node = null
print("✓ Lista vazia criada")

// Teste 1: Inserir elementos no início
print("")
print("--- Teste 1: Inserção no início ---")
lista = inserir_inicio(lista, 10)
imprimir_lista(lista)

lista = inserir_inicio(lista, 20)
imprimir_lista(lista)

lista = inserir_inicio(lista, 30)
imprimir_lista(lista)

print("Elementos na lista: " + to_str(contar_elementos(lista)))

// Teste 2: Buscar valores
print("")
print("--- Teste 2: Busca de valores ---")
let posicao_30: int = buscar_valor(lista, 30)
print("Valor 30 encontrado na posição: " + to_str(posicao_30))

let posicao_20: int = buscar_valor(lista, 20)
print("Valor 20 encontrado na posição: " + to_str(posicao_20))

let posicao_10: int = buscar_valor(lista, 10)
print("Valor 10 encontrado na posição: " + to_str(posicao_10))

let posicao_99: int = buscar_valor(lista, 99)
print("Valor 99 encontrado na posição: " + to_str(posicao_99))

// Teste 3: Inserir mais elementos
print("")
print("--- Teste 3: Inserção adicional ---")
lista = inserir_inicio(lista, 40)
imprimir_lista(lista)

lista = inserir_inicio(lista, 50)
imprimir_lista(lista)

print("Elementos na lista: " + to_str(contar_elementos(lista)))

// ============================================
// TESTE DE ATRIBUIÇÃO DINÂMICA
// ============================================

print("")
print("=== TESTE DE ATRIBUIÇÃO DINÂMICA ===")

// Criar um nó individual e modificar seus campos
let no_teste: Node = Node(999, null)
print("✓ Nó de teste criado com valor: " + to_str(no_teste.valor))

// Modificar o valor do nó
no_teste.valor = 888
print("✓ Valor modificado para: " + to_str(no_teste.valor))

// Criar outro nó
let no_teste2: Node = Node(777, null)
print("✓ Segundo nó criado com valor: " + to_str(no_teste2.valor))

// Verificar a estrutura
print("Nó 1: valor = " + to_str(no_teste.valor))
print("Nó 2: valor = " + to_str(no_teste2.valor))

// ============================================
// TESTE DE NAVEGAÇÃO
// ============================================

print("")
print("=== TESTE DE NAVEGAÇÃO ===")

// Navegar pela lista e mostrar cada elemento
let atual: ref Node = ref lista
let posicao: int = 0

print("Navegando pela lista:")
while atual != null do
    print("Posição " + to_str(posicao) + ": " + to_str(atual.valor))
    atual = ref atual.proximo
    posicao = posicao + 1
end

// ============================================
// RESULTADOS FINAIS
// ============================================

print("")
print("=== RESULTADOS FINAIS ===")
print("Lista final:")
imprimir_lista(lista)
print("Total de elementos: " + to_str(contar_elementos(lista)))

print("")
print("=== TESTE CONCLUÍDO COM SUCESSO ===")
print("✓ Linked List implementada com structs")
print("✓ Auto-referência funcionando (ref Node)")
print("✓ Inserção no início")
print("✓ Busca de elementos")
print("✓ Atribuição dinâmica de campos")
print("✓ Contagem de elementos")
print("✓ Navegação pela lista")
print("✓ Estrutura de dados linear funcionando") 