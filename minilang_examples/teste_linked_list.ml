// ============================================
// MiniLang - Teste Linked List (Lista Encadeada)
// Implementação de lista encadeada simples usando structs
// ============================================

print("=== TESTE LINKED LIST ===")

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

// Função para inserir no final da lista
func inserir_final(lista: ref Node, valor: int)
    let novo_no: Node = Node(valor, null)
    
    if lista == null then
        return ref novo_no
    end
    
    let atual: ref Node = ref lista
    while atual.proximo != null do
        atual = ref atual.proximo
    end
    
    atual.proximo = ref novo_no
    return ref lista
end

print("✓ Função inserir_final definida")

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

// Função para remover um valor da lista
func remover_valor(lista: ref Node, valor: int)
    if lista == null then
        return null
    end
    
    // Se o valor está no primeiro nó
    if lista.valor == valor then
        return ref lista.proximo
    end
    
    let atual: ref Node = ref lista
    while atual.proximo != null do
        if atual.proximo.valor == valor then
            atual.proximo = ref atual.proximo.proximo
            return ref lista
        end
        atual = ref atual.proximo
    end
    
    return ref lista
end

print("✓ Função remover_valor definida")

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

// Teste 2: Inserir elementos no final
print("")
print("--- Teste 2: Inserção no final ---")
lista = inserir_final(lista, 40)
imprimir_lista(lista)

lista = inserir_final(lista, 50)
imprimir_lista(lista)

print("Elementos na lista: " + to_str(contar_elementos(lista)))

// Teste 3: Buscar valores
print("")
print("--- Teste 3: Busca de valores ---")
let posicao_30: int = buscar_valor(lista, 30)
print("Valor 30 encontrado na posição: " + to_str(posicao_30))

let posicao_50: int = buscar_valor(lista, 50)
print("Valor 50 encontrado na posição: " + to_str(posicao_50))

let posicao_99: int = buscar_valor(lista, 99)
print("Valor 99 encontrado na posição: " + to_str(posicao_99))

// Teste 4: Remover valores
print("")
print("--- Teste 4: Remoção de valores ---")
print("Removendo valor 20...")
lista = remover_valor(lista, 20)
imprimir_lista(lista)

print("Removendo valor 30...")
lista = remover_valor(lista, 30)
imprimir_lista(lista)

print("Removendo valor 50...")
lista = remover_valor(lista, 50)
imprimir_lista(lista)

print("Elementos na lista: " + to_str(contar_elementos(lista)))

// Teste 5: Inserir mais elementos
print("")
print("--- Teste 5: Inserção adicional ---")
lista = inserir_inicio(lista, 100)
imprimir_lista(lista)

lista = inserir_final(lista, 200)
imprimir_lista(lista)

lista = inserir_inicio(lista, 300)
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

// Criar outro nó e fazer referência
let no_teste2: Node = Node(777, null)
no_teste.proximo = ref no_teste2
print("✓ Referência criada entre nós")

// Verificar a estrutura
print("Nó 1: valor = " + to_str(no_teste.valor))
if no_teste.proximo != null then
    print("Nó 1 -> Nó 2: valor = " + to_str(no_teste.proximo.valor))
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
print("✓ Inserção no início e final")
print("✓ Busca e remoção de elementos")
print("✓ Atribuição dinâmica de campos")
print("✓ Contagem de elementos")
print("✓ Estrutura de dados linear funcionando") 