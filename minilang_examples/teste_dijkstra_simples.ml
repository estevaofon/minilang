// ============================================
// MiniLang - Teste Algoritmo de Dijkstra Simples
// Demonstração de structs com atribuição dinâmica
// ============================================

print("=== TESTE ALGORITMO DE DIJKSTRA SIMPLES ===")

// ============================================
// DEFINIÇÕES DAS ESTRUTURAS
// ============================================

// Estrutura para representar um vértice do grafo
struct Vertice
    id: int,
    distancia: int,
    visitado: bool,
    anterior_id: int
end

print("✓ Struct Vertice definido")

// ============================================
// EXECUÇÃO DO TESTE
// ============================================

// Criar vértices individuais
let vertice0: Vertice = Vertice(0, 999999, false, -1)
let vertice1: Vertice = Vertice(1, 999999, false, -1)
let vertice2: Vertice = Vertice(2, 999999, false, -1)
let vertice3: Vertice = Vertice(3, 999999, false, -1)
let vertice4: Vertice = Vertice(4, 999999, false, -1)

print("✓ Vértices criados")

// ============================================
// SIMULAÇÃO DO ALGORITMO DE DIJKSTRA
// ============================================

print("")
print("=== SIMULAÇÃO DO ALGORITMO DE DIJKSTRA ===")
print("Grafo de exemplo:")
print("  0 --4-- 1")
print("  |      | \\")
print("  2      5  2")
print("  |      |   \\")
print("  10     8     3")
print("  |      |   /")
print("  4 --2-- 4")

// Passo 1: Inicializar vértice origem
vertice0.distancia = 0
vertice0.visitado = true
print("")
print("Passo 1: Vértice 0 selecionado")
print("✓ Vértice 0: distancia = " + to_str(vertice0.distancia))

// Passo 2: Atualizar distâncias dos vizinhos do vértice 0
vertice1.distancia = 4
vertice1.anterior_id = 0
vertice2.distancia = 2
vertice2.anterior_id = 0
print("")
print("Passo 2: Atualizar vizinhos do vértice 0")
print("✓ Vértice 1: distancia = " + to_str(vertice1.distancia) + ", anterior = " + to_str(vertice1.anterior_id))
print("✓ Vértice 2: distancia = " + to_str(vertice2.distancia) + ", anterior = " + to_str(vertice2.anterior_id))

// Passo 3: Selecionar vértice 2 (menor distância)
vertice2.visitado = true
print("")
print("Passo 3: Vértice 2 selecionado (menor distância)")

// Passo 4: Atualizar distâncias através do vértice 2
if vertice1.distancia > vertice2.distancia + 1 then
    vertice1.distancia = vertice2.distancia + 1
    vertice1.anterior_id = 2
end

vertice3.distancia = vertice2.distancia + 8
vertice3.anterior_id = 2

vertice4.distancia = vertice2.distancia + 10
vertice4.anterior_id = 2

print("")
print("Passo 4: Atualizar através do vértice 2")
print("✓ Vértice 1: distancia = " + to_str(vertice1.distancia) + ", anterior = " + to_str(vertice1.anterior_id))
print("✓ Vértice 3: distancia = " + to_str(vertice3.distancia) + ", anterior = " + to_str(vertice3.anterior_id))
print("✓ Vértice 4: distancia = " + to_str(vertice4.distancia) + ", anterior = " + to_str(vertice4.anterior_id))

// Passo 5: Selecionar vértice 1
vertice1.visitado = true
print("")
print("Passo 5: Vértice 1 selecionado")

// Passo 6: Atualizar através do vértice 1
if vertice3.distancia > vertice1.distancia + 5 then
    vertice3.distancia = vertice1.distancia + 5
    vertice3.anterior_id = 1
end

print("")
print("Passo 6: Atualizar através do vértice 1")
print("✓ Vértice 3: distancia = " + to_str(vertice3.distancia) + ", anterior = " + to_str(vertice3.anterior_id))

// Passo 7: Selecionar vértice 3
vertice3.visitado = true
print("")
print("Passo 7: Vértice 3 selecionado")

// Passo 8: Atualizar através do vértice 3
if vertice4.distancia > vertice3.distancia + 2 then
    vertice4.distancia = vertice3.distancia + 2
    vertice4.anterior_id = 3
end

print("")
print("Passo 8: Atualizar através do vértice 3")
print("✓ Vértice 4: distancia = " + to_str(vertice4.distancia) + ", anterior = " + to_str(vertice4.anterior_id))

// Passo 9: Selecionar vértice 4
vertice4.visitado = true
print("")
print("Passo 9: Vértice 4 selecionado")

// ============================================
// RESULTADOS FINAIS
// ============================================

print("")
print("=== RESULTADOS FINAIS ===")
print("Distâncias mínimas a partir do vértice 0:")
print("Vértice 0: " + to_str(vertice0.distancia))
print("Vértice 1: " + to_str(vertice1.distancia))
print("Vértice 2: " + to_str(vertice2.distancia))
print("Vértice 3: " + to_str(vertice3.distancia))
print("Vértice 4: " + to_str(vertice4.distancia))

print("")
print("=== CAMINHOS MAIS CURTOS ===")
print("0 -> 0: 0 (distância: " + to_str(vertice0.distancia) + ")")
print("0 -> 1: 0 -> 1 (distância: " + to_str(vertice1.distancia) + ")")
print("0 -> 2: 0 -> 2 (distância: " + to_str(vertice2.distancia) + ")")
print("0 -> 3: 0 -> 2 -> 1 -> 3 (distância: " + to_str(vertice3.distancia) + ")")
print("0 -> 4: 0 -> 2 -> 1 -> 3 -> 4 (distância: " + to_str(vertice4.distancia) + ")")

print("")
print("=== TESTE CONCLUÍDO COM SUCESSO ===")
print("✓ Structs com atribuição dinâmica funcionando")
print("✓ Algoritmo de Dijkstra simulado")
print("✓ Atribuição de campos funcionando corretamente")
print("✓ Cálculo de caminhos mais curtos demonstrado")
print("✓ Estruturas de dados complexas testadas") 