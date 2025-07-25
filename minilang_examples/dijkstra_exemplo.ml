// MiniLang v2.0 - Algoritmo de Dijkstra
// =====================================

// Função strlen para MiniLang
func len(s: string) -> int
    let i: int = 0
    while s[i] != "\0" do
        i = i + 1
    end
    return i
end

print("=== MiniLang v2.0 - Algoritmo de Dijkstra ===")
print("")

// Constantes para o algoritmo
global INFINITY: int = 999999
global MAX_VERTICES: int = 6

// Matriz de adjacência do grafo (pesos das arestas)
// Representada como array unidimensional: graph[i*6 + j] = peso da aresta i->j
// INFINITY significa que não há aresta entre os vértices
global graph: int[36] = [
    0, 2, 999999, 1, 999999, 999999,      // Vértice 0
    2, 0, 3, 2, 999999, 999999,            // Vértice 1
    999999, 3, 0, 999999, 1, 5,            // Vértice 2
    1, 2, 999999, 0, 4, 999999,            // Vértice 3
    999999, 999999, 1, 4, 0, 2,            // Vértice 4
    999999, 999999, 5, 999999, 2, 0        // Vértice 5
]

// Arrays para armazenar as distâncias e vértices visitados
global distances: int[6] = [0, 0, 0, 0, 0, 0]
global visited: int[6] = [0, 0, 0, 0, 0, 0]
global previous: int[6] = [-1, -1, -1, -1, -1, -1]

// Função para acessar elemento da matriz (i, j)
func getMatrixElement(i: int, j: int) -> int
    return graph[i * 6 + j]
end

// Função para definir elemento da matriz (i, j)
func setMatrixElement(i: int, j: int, value: int) -> void
    graph[i * 6 + j] = value
end

// Função para encontrar o vértice com menor distância não visitado
func findMinDistance() -> int
    let min_dist: int = INFINITY
    let min_vertex: int = -1
    let i: int = 0
    
    while i < MAX_VERTICES do
        if visited[i] == 0 then
            if distances[i] < min_dist then
                min_dist = distances[i]
                min_vertex = i
            end
        end
        i = i + 1
    end
    
    return min_vertex
end

// Função para imprimir o caminho do vértice inicial até o destino
func printPath(destination: int) -> void
    if previous[destination] == -1 then
        print("  ")
        print(destination)
    else
        printPath(previous[destination])
        print(" -> ")
        print(destination)
    end
end

// Função para imprimir todas as distâncias
func printDistances() -> void
    let i: int = 0
    print("Distâncias mínimas:")
    while i < MAX_VERTICES do
        print("  Vértice ")
        print(i)
        print(": ")
        if distances[i] == INFINITY then
            print("INFINITO")
        else
            print(distances[i])
        end
        print("")
        i = i + 1
    end
end

// Função para imprimir todos os caminhos
func printAllPaths() -> void
    let i: int = 0
    print("Caminhos mínimos:")
    while i < MAX_VERTICES do
        print("  Para vértice ")
        print(i)
        print(": ")
        if distances[i] == INFINITY then
            print("Sem caminho")
        else
            printPath(i)
        end
        print(" (distância: ")
        if distances[i] == INFINITY then
            print("INFINITO")
        else
            print(distances[i])
        end
        print(")")
        print("")
        i = i + 1
    end
end

// Função para obter o peso da aresta entre dois vértices
func getEdgeWeight(from: int, to: int) -> int
    return getMatrixElement(from, to)
end

// Função para verificar se um vértice foi visitado
func isVisited(vertex: int) -> int
    return visited[vertex]
end

// Função para marcar um vértice como visitado
func markVisited(vertex: int) -> void
    visited[vertex] = 1
end

// Função para atualizar a distância de um vértice
func updateDistance(vertex: int, new_distance: int) -> void
    distances[vertex] = new_distance
end

// Função para atualizar o vértice anterior no caminho
func updatePrevious(vertex: int, prev: int) -> void
    previous[vertex] = prev
end

// Função para obter a distância atual de um vértice
func getDistance(vertex: int) -> int
    return distances[vertex]
end

// Função para inicializar as distâncias
func initializeDistances(start: int) -> void
    let i: int = 0
    while i < MAX_VERTICES do
        if i == start then
            distances[i] = 0
        else
            distances[i] = INFINITY
        end
        visited[i] = 0
        previous[i] = -1
        i = i + 1
    end
end

// Algoritmo de Dijkstra principal
func dijkstra(start: int) -> void
    // Inicializar distâncias
    initializeDistances(start)
    
    print("Executando Dijkstra a partir do vértice ")
    print(start)
    print("")
    
    let count: int = 0
    while count < MAX_VERTICES do
        // Encontrar o vértice com menor distância não visitado
        let current: int = findMinDistance()
        
        if current == -1 then
            print("Erro: Não foi possível encontrar vértice não visitado")
            return
        end
        
        // Marcar o vértice atual como visitado
        markVisited(current)
        
        print("Visitando vértice ")
        print(current)
        print(" (distância: ")
        print(distances[current])
        print(")")
        
        // Atualizar distâncias dos vizinhos
        let neighbor: int = 0
        while neighbor < MAX_VERTICES do
            let weight: int = getEdgeWeight(current, neighbor)
            
            // Se há uma aresta e o vizinho não foi visitado
            if weight != INFINITY then
                if isVisited(neighbor) == 0 then
                    let new_distance: int = distances[current] + weight
                    
                    // Se encontramos um caminho mais curto
                    if new_distance < distances[neighbor] then
                        updateDistance(neighbor, new_distance)
                        updatePrevious(neighbor, current)
                        print("  Atualizando vértice ")
                        print(neighbor)
                        print(": nova distância = ")
                        print(new_distance)
                        print("")
                    end
                end
            end
            neighbor = neighbor + 1
        end
        
        count = count + 1
    end
end

// Função para imprimir a matriz de adjacência
func printGraph() -> void
    print("Matriz de adjacência do grafo:")
    let i: int = 0
    while i < MAX_VERTICES do
        let j: int = 0
        while j < MAX_VERTICES do
            let weight: int = getMatrixElement(i, j)
            if weight == INFINITY then
                print("INF ")
            else
                print(weight)
                print(" ")
            end
            j = j + 1
        end
        print("")
        i = i + 1
    end
    print("")
end

// Função para imprimir o grafo de forma visual
func printGraphVisual() -> void
    print("Representação visual do grafo:")
    print("")
    print("    0 --2-- 1 --3-- 2")
    print("    |      |       |")
    print("    1      2       1")
    print("    |      |       |")
    print("    3 --4-- 4 --2-- 5")
    print("")
    print("Vértices: 0, 1, 2, 3, 4, 5")
    print("")
end

// Demonstração do algoritmo
print(">> Grafo de exemplo:")
printGraphVisual()
printGraph()

// Executar Dijkstra a partir do vértice 0
let start_vertex: int = 0
dijkstra(start_vertex)

print("")
print(">> Resultados:")
print("")

printDistances()
print("")
printAllPaths()

print("")
print(">> Explicação do algoritmo:")
print("")
print("O algoritmo de Dijkstra encontra o caminho mais curto")
print("de um vértice inicial para todos os outros vértices")
print("em um grafo ponderado com pesos não-negativos.")
print("")
print("Passos do algoritmo:")
print("1. Inicializar distâncias: 0 para o vértice inicial,")
print("   INFINITO para todos os outros")
print("2. Encontrar o vértice não visitado com menor distância")
print("3. Marcar esse vértice como visitado")
print("4. Atualizar distâncias dos vizinhos não visitados")
print("5. Repetir até visitar todos os vértices")
print("")
print("Complexidade: O(V²) onde V é o número de vértices")
print("")

print("=== Fim da demonstração do algoritmo de Dijkstra ===") 