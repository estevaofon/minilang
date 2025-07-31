print("=== TRIANGULO DE SIERPINSKI RECURSIVO ===")
print("")

// Funcao recursiva para potencia de 2
func pot2_recursiva(n: int) -> int
    if n == 0 then
        return 1
    else
        return 2 * pot2_recursiva(n - 1)
    end
end

// Funcao recursiva para verificar se deve desenhar (AND bit a bit)
func deve_desenhar_recursivo(linha: int, coluna: int) -> bool
    if coluna == 0 then
        return true
    else
        if (linha % 2 == 0) & (coluna % 2 == 1) then
            return false
        else
            let nova_linha: int = linha / 2
            let nova_coluna: int = coluna / 2
            return deve_desenhar_recursivo(nova_linha, nova_coluna)
        end
    end
end

// Funcao para criar string com espacos
func criar_espacos(n: int) -> string
    let resultado: string = ""
    let i: int = 0
    while i < n do
        resultado = resultado + " "
        i = i + 1
    end
    return resultado
end

// Funcao para imprimir uma linha do triangulo
func imprimir_linha_sierpinski(linha: int, tamanho: int) -> void
    // Construir a linha como uma string
    let linha_str: string = ""
    
    // Adicionar espacos iniciais para centralizar
    linha_str = linha_str + criar_espacos(tamanho - linha - 1)
    
    let coluna: int = 0
    while coluna <= linha do
        let deve_desenhar: bool = deve_desenhar_recursivo(linha, coluna)
        if deve_desenhar then
            linha_str = linha_str + "* "
        else
            linha_str = linha_str + "  "
        end
        coluna = coluna + 1
    end
    
    // Imprimir a linha completa
    print(linha_str)
end

// Funcao iterativa para imprimir o triangulo (sem recursao)
func imprimir_triangulo_sierpinski(ordem: int) -> void
    let tamanho: int = pot2_recursiva(ordem)
    let linha: int = 0
    
    while linha < tamanho do
        imprimir_linha_sierpinski(linha, tamanho)
        linha = linha + 1
    end
end

// Funcao wrapper para iniciar o triangulo
func desenhar_sierpinski(ordem: int) -> void
    print("Triangulo de Sierpinski - Ordem: " + to_str(ordem))
    print("Tamanho: " + to_str(pot2_recursiva(ordem)) + " linhas")
    print("")
    
    imprimir_triangulo_sierpinski(ordem)
end

// Teste
print("=== TESTE: Versao Recursiva Elegante ===")
desenhar_sierpinski(6)

print("")
print("=== PROPRIEDADES DO FRACTAL ===")
print("- Auto-similaridade em todas as escalas")
print("- Dimensao fractal: log(3)/log(2) = 1.585")
print("- Construido recursivamente com triangulo de Pascal mod 2")
print("- Versao recursiva mais elegante e matematica")
print("")

print("=== VANTAGENS DA VERSAO RECURSIVA ===")
print("✓ Codigo mais limpo e legivel")
print("✓ Logica mais proxima da definicao matematica")
print("✓ Facil de entender e modificar")
print("✓ Melhor para demonstracoes educacionais")
print("✓ Suporta diferentes estrategias recursivas")
print("")

print("=== FIM ===") 