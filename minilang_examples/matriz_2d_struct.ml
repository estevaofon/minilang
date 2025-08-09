// ============================================
// IMPLEMENTAÇÃO DE MATRIZES 2D EM MINILANG
// Suporte para Matriz 100x10
// ============================================

// Struct principal para matriz 2D
struct Matriz2D
    elementos: int[1000], // Array interno para matriz 100x10
    linhas: int,          // Número de linhas
    colunas: int          // Número de colunas
end

// Função para calcular índice linear
func indice_linear(linha: int, coluna: int, colunas: int) -> int
    return linha * colunas + coluna
end

// Função para acessar elemento da matriz
func acessar_elemento(matriz: ref Matriz2D, linha: int, coluna: int) -> int
    let indice: int = indice_linear(linha, coluna, matriz.colunas)
    return matriz.elementos[indice]
end

// Função para definir elemento da matriz
func definir_elemento(matriz: ref Matriz2D, linha: int, coluna: int, valor: int) -> void
    let indice: int = indice_linear(linha, coluna, matriz.colunas)
    matriz.elementos[indice] = valor
end

// Função para imprimir matriz (versão otimizada para matrizes grandes)
func imprimir_matriz(matriz: ref Matriz2D) -> void
    let i: int = 0
    while i < matriz.linhas do
        let j: int = 0
        let linha_str: string = ""
        while j < matriz.colunas do
            let elemento: int = acessar_elemento(matriz, i, j)
            if j > 0 then
                linha_str = linha_str + " "
            end
            linha_str = linha_str + to_str(elemento)
            j = j + 1
        end
        print(linha_str)
        i = i + 1
    end
end

// Função para imprimir parte da matriz (útil para matrizes grandes)
func imprimir_matriz_parcial(matriz: ref Matriz2D, max_linhas: int, max_colunas: int) -> void
    let linhas_imprimir: int = max_linhas
    let colunas_imprimir: int = max_colunas
    
    if linhas_imprimir > matriz.linhas then
        linhas_imprimir = matriz.linhas
    end
    
    if colunas_imprimir > matriz.colunas then
        colunas_imprimir = matriz.colunas
    end
    
    let i: int = 0
    while i < linhas_imprimir do
        let j: int = 0
        let linha_str: string = ""
        while j < colunas_imprimir do
            let elemento: int = acessar_elemento(matriz, i, j)
            if j > 0 then
                linha_str = linha_str + " "
            end
            linha_str = linha_str + to_str(elemento)
            j = j + 1
        end
        if colunas_imprimir < matriz.colunas then
            linha_str = linha_str + " ..."
        end
        print(linha_str)
        i = i + 1
    end
    
    if linhas_imprimir < matriz.linhas then
        print("...")
    end
end

// Função para criar matriz vazia
func criar_matriz_vazia(linhas: int, colunas: int) -> Matriz2D
    // Criar array com capacidade para 100x10 = 1000 elementos
    let elementos: int[1000] = zeros(1000)
    return Matriz2D(elementos, linhas, colunas)
end

// Função para preencher matriz com valor
func preencher_matriz(matriz: ref Matriz2D, valor: int) -> void
    let i: int = 0
    while i < matriz.linhas do
        let j: int = 0
        while j < matriz.colunas do
            definir_elemento(matriz, i, j, valor)
            j = j + 1
        end
        i = i + 1
    end
end

// Função para somar todos elementos da matriz
func somar_elementos(matriz: ref Matriz2D) -> int
    let soma: int = 0
    let i: int = 0
    while i < matriz.linhas do
        let j: int = 0
        while j < matriz.colunas do
            soma = soma + acessar_elemento(matriz, i, j)
            j = j + 1
        end
        i = i + 1
    end
    return soma
end

// ============================================
// TESTES E DEMONSTRAÇÃO
// ============================================

print("=== IMPLEMENTAÇÃO DE MATRIZES 2D EM MINILANG ===")
print("Suporte para Matriz 100x10")
print("")

// Teste 1: Criar matriz pequena para validação
print("=== TESTE 1: Matriz 3x3 ===")
let matriz_pequena: Matriz2D = criar_matriz_vazia(3, 3)

// Preencher com valores sequenciais
let contador: int = 1
let i1: int = 0
while i1 < 3 do
    let j1: int = 0
    while j1 < 3 do
        definir_elemento(matriz_pequena, i1, j1, contador)
        contador = contador + 1
        j1 = j1 + 1
    end
    i1 = i1 + 1
end

print("Matriz 3x3 preenchida:")
imprimir_matriz(matriz_pequena)
print("")

// Teste 2: Criar matriz 100x10
print("=== TESTE 2: Matriz 100x10 ===")
let matriz_grande: Matriz2D = criar_matriz_vazia(100, 10)

print("Matriz 100x10 criada com sucesso!")
print("Dimensões: " + to_str(matriz_grande.linhas) + "x" + to_str(matriz_grande.colunas))
print("")

// Preencher algumas linhas com padrão
print("Preenchendo primeiras 5 linhas com padrão...")
let i2: int = 0
while i2 < 5 do
    let j2: int = 0
    while j2 < 10 do
        let valor: int = i2 * 10 + j2
        definir_elemento(matriz_grande, i2, j2, valor)
        j2 = j2 + 1
    end
    i2 = i2 + 1
end

// Preencher última linha
let i3: int = 99
let j3: int = 0
while j3 < 10 do
    definir_elemento(matriz_grande, i3, j3, 999)
    j3 = j3 + 1
end

print("Primeiras 5 linhas e 10 colunas da matriz 100x10:")
imprimir_matriz_parcial(matriz_grande, 5, 10)
print("")

// Teste 3: Validação de acesso em posições específicas
print("=== TESTE 3: Validação de Acesso ===")
print("Elemento [0,0]: " + to_str(acessar_elemento(matriz_grande, 0, 0)))
print("Elemento [0,9]: " + to_str(acessar_elemento(matriz_grande, 0, 9)))
print("Elemento [4,5]: " + to_str(acessar_elemento(matriz_grande, 4, 5)))
print("Elemento [99,0]: " + to_str(acessar_elemento(matriz_grande, 99, 0)))
print("Elemento [99,9]: " + to_str(acessar_elemento(matriz_grande, 99, 9)))
print("")

// Teste 4: Operações em matriz completa
print("=== TESTE 4: Operações em Matriz Completa ===")
let matriz_teste: Matriz2D = criar_matriz_vazia(10, 10)
preencher_matriz(matriz_teste, 5)
print("Matriz 10x10 preenchida com valor 5")
print("Soma de todos elementos: " + to_str(somar_elementos(matriz_teste)))
print("")

// Teste 5: Matriz com padrão diagonal
print("=== TESTE 5: Matriz com Padrão Diagonal ===")
let matriz_diagonal: Matriz2D = criar_matriz_vazia(10, 10)
let i4: int = 0
while i4 < 10 do
    let valor_diagonal: int = i4 + 1
    definir_elemento(matriz_diagonal, i4, i4, valor_diagonal)
    i4 = i4 + 1
end
print("Matriz 10x10 com diagonal preenchida:")
imprimir_matriz_parcial(matriz_diagonal, 10, 10)
print("")

print("=== RESUMO ===")
print("✓ Matrizes 2D implementadas com sucesso")
print("✓ Suporte completo para matriz 100x10 (1000 elementos)")
print("✓ Funções auxiliares: preencher, somar, impressão parcial")
print("✓ Operações básicas: acesso, modificação, impressão")
print("✓ Testado com matrizes de diferentes tamanhos")
print("")
print("Sistema pronto para trabalhar com matrizes até 100x10!")