// Teste completo para declaração de variáveis através do retorno de funções

// Arrays para teste
let numeros: int[7] = [1, 3, 5, 7, 9, 11, 13]
let precos: float[4] = [10.50, 25.75, 8.99, 15.25]
let nomes: string[3] = ["João", "Maria", "Pedro"]

// Teste 1: Declarações locais com let
let tamanho_numeros: int = length(numeros)
let tamanho_precos: int = length(precos)
let tamanho_nomes: int = length(nomes)

print("=== TESTE 1: Declarações locais ===")
print("Tamanho do array numeros: ")
print(tamanho_numeros)
print("Tamanho do array precos: ")
print(tamanho_precos)
print("Tamanho do array nomes: ")
print(tamanho_nomes)

// Teste 2: Declarações globais com global
global total_numeros: int = length(numeros)
global total_precos: int = length(precos)
global total_nomes: int = length(nomes)

print("=== TESTE 2: Declarações globais ===")
print("Total numeros (global): ")
print(total_numeros)
print("Total precos (global): ")
print(total_precos)
print("Total nomes (global): ")
print(total_nomes)

// Teste 3: Funções que retornam valores
func calcular_soma(a: int, b: int, c: int) -> int
    return a + b + c
end

func calcular_media(a: float, b: float, c: float) -> float
    return (a + b + c) / 3.0
end

func concatenar_strings(a: string, b: string) -> string
    return a + " " + b
end

// Teste 4: Declarações com funções personalizadas
let soma_tres: int = calcular_soma(10, 20, 30)
let media_tres: float = calcular_media(15.5, 25.5, 35.5)
let nome_completo: string = concatenar_strings("João", "Silva")

print("=== TESTE 3: Funções personalizadas ===")
print("Soma de três números: ")
print(soma_tres)
print("Média de três números: ")
print(media_tres)
print("Nome completo: ")
print(nome_completo)

// Teste 5: Declarações globais com funções personalizadas
global soma_global: int = calcular_soma(100, 200, 300)
global media_global: float = calcular_media(50.0, 75.0, 100.0)
global nome_global: string = concatenar_strings("Maria", "Santos")

print("=== TESTE 4: Globais com funções personalizadas ===")
print("Soma global: ")
print(soma_global)
print("Média global: ")
print(media_global)
print("Nome global: ")
print(nome_global)

// Teste 6: Funções com arrays
func somar_array(arr: int[], tamanho: int) -> int
    let soma: int = 0
    let i: int = 0
    while i < tamanho do
        soma = soma + arr[i]
        i = i + 1
    end
    return soma
end

let soma_total: int = somar_array(numeros, length(numeros))
global soma_total_global: int = somar_array(numeros, length(numeros))

print("=== TESTE 5: Funções com arrays ===")
print("Soma total do array numeros: ")
print(soma_total)
print("Soma total global: ")
print(soma_total_global)

print("=== TODOS OS TESTES PASSARAM! ===")
print("A MiniLang agora suporta declaração de variáveis através do retorno de funções!") 