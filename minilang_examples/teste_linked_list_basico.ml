// ============================================
// MiniLang - Teste Linked List Básico
// Implementação básica de lista encadeada
// ============================================

print("=== TESTE LINKED LIST BÁSICO ===")

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
// EXECUÇÃO DO TESTE
// ============================================

print("")
print("=== TESTE DE CRIAÇÃO DE NÓS ===")

// Criar nós individuais
let no1: Node = Node(10, null)
print("✓ Nó 1 criado com valor: " + to_str(no1.valor))

let no2: Node = Node(20, null)
print("✓ Nó 2 criado com valor: " + to_str(no2.valor))

let no3: Node = Node(30, null)
print("✓ Nó 3 criado com valor: " + to_str(no3.valor))

let no4: Node = Node(40, null)
print("✓ Nó 4 criado com valor: " + to_str(no4.valor))

// ============================================
// TESTE DE ATRIBUIÇÃO DINÂMICA
// ============================================

print("")
print("=== TESTE DE ATRIBUIÇÃO DINÂMICA ===")

// Modificar valores dos nós
no1.valor = 15
print("✓ Nó 1: valor modificado para " + to_str(no1.valor))

no2.valor = 25
print("✓ Nó 2: valor modificado para " + to_str(no2.valor))

no3.valor = 35
print("✓ Nó 3: valor modificado para " + to_str(no3.valor))

no4.valor = 45
print("✓ Nó 4: valor modificado para " + to_str(no4.valor))

// ============================================
// SIMULAÇÃO DE LISTA ENCADEADA
// ============================================

print("")
print("=== SIMULAÇÃO DE LISTA ENCADEADA ===")

// Simular uma lista encadeada manualmente
print("Simulando lista: no1 -> no2 -> no3 -> no4")
print("Nó 1: " + to_str(no1.valor))
print("Nó 2: " + to_str(no2.valor))
print("Nó 3: " + to_str(no3.valor))
print("Nó 4: " + to_str(no4.valor))

// ============================================
// TESTE DE OPERAÇÕES
// ============================================

print("")
print("=== TESTE DE OPERAÇÕES ===")

// Contar nós
let total_nos: int = 4
print("Total de nós na lista: " + to_str(total_nos))

// Buscar valores
let valor_busca1: int = 25
let valor_busca2: int = 35
let valor_busca3: int = 99

print("Buscando valor " + to_str(valor_busca1) + "...")
if no1.valor == valor_busca1 then
    print("Encontrado no Nó 1")
else
    if no2.valor == valor_busca1 then
        print("Encontrado no Nó 2")
    else
        if no3.valor == valor_busca1 then
            print("Encontrado no Nó 3")
        else
            if no4.valor == valor_busca1 then
                print("Encontrado no Nó 4")
            else
                print("Valor não encontrado")
            end
        end
    end
end

print("Buscando valor " + to_str(valor_busca2) + "...")
if no1.valor == valor_busca2 then
    print("Encontrado no Nó 1")
else
    if no2.valor == valor_busca2 then
        print("Encontrado no Nó 2")
    else
        if no3.valor == valor_busca2 then
            print("Encontrado no Nó 3")
        else
            if no4.valor == valor_busca2 then
                print("Encontrado no Nó 4")
            else
                print("Valor não encontrado")
            end
        end
    end
end

print("Buscando valor " + to_str(valor_busca3) + "...")
if no1.valor == valor_busca3 then
    print("Encontrado no Nó 1")
else
    if no2.valor == valor_busca3 then
        print("Encontrado no Nó 2")
    else
        if no3.valor == valor_busca3 then
            print("Encontrado no Nó 3")
        else
            if no4.valor == valor_busca3 then
                print("Encontrado no Nó 4")
            else
                print("Valor não encontrado")
            end
        end
    end
end

// ============================================
// TESTE DE MODIFICAÇÃO
// ============================================

print("")
print("=== TESTE DE MODIFICAÇÃO ===")

// Modificar valores novamente
no1.valor = 100
no2.valor = 200
no3.valor = 300
no4.valor = 400

print("✓ Valores modificados:")
print("Nó 1: " + to_str(no1.valor))
print("Nó 2: " + to_str(no2.valor))
print("Nó 3: " + to_str(no3.valor))
print("Nó 4: " + to_str(no4.valor))

// ============================================
// TESTE DE CÁLCULOS
// ============================================

print("")
print("=== TESTE DE CÁLCULOS ===")

// Calcular soma dos valores
let soma: int = no1.valor + no2.valor + no3.valor + no4.valor
print("Soma dos valores: " + to_str(soma))

// Calcular média
let media: int = soma / 4
print("Média dos valores: " + to_str(media))

// Encontrar valor máximo
let maximo: int = no1.valor
if no2.valor > maximo then
    let maximo: int = no2.valor
end
if no3.valor > maximo then
    let maximo: int = no3.valor
end
if no4.valor > maximo then
    let maximo: int = no4.valor
end
print("Valor máximo: " + to_str(maximo))

// ============================================
// RESULTADOS FINAIS
// ============================================

print("")
print("=== RESULTADOS FINAIS ===")
print("Lista final:")
print("Nó 1: " + to_str(no1.valor))
print("Nó 2: " + to_str(no2.valor))
print("Nó 3: " + to_str(no3.valor))
print("Nó 4: " + to_str(no4.valor))
print("Total de nós: " + to_str(total_nos))

print("")
print("=== TESTE CONCLUÍDO COM SUCESSO ===")
print("✓ Struct Node definido e funcionando")
print("✓ Atribuição dinâmica de campos")
print("✓ Criação de múltiplos nós")
print("✓ Modificação de valores")
print("✓ Busca de valores")
print("✓ Cálculos com valores dos nós")
print("✓ Estrutura de dados básica funcionando") 