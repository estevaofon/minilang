// ===================================
// MiniLang v2.0 - Demonstração Completa
// ===================================

print("=== MiniLang v2.0 - Demonstração Completa ===")
print("")

// 1. Tipos básicos e variáveis
print(">> 1. Tipos básicos:")
let inteiro: int = 42
let decimal: float = 3.14159
let texto: string = "MiniLang é incrível!"

print("Inteiro: ")
print(inteiro)
print("Decimal: ")
print(decimal)
print("Texto: " ++ texto)
print("")

// 2. Arrays
print(">> 2. Arrays:")
let numeros: int[5] = [10, 20, 30, 40, 50]
let temperaturas: float[7] = [23.5, 24.0, 22.8, 25.3, 26.1, 24.7, 23.9]

print("Array de números:")
print(numeros)
print("")

print("Array de temperaturas:")
print(temperaturas)
print("")

// 3. Arrays grandes com zeros()
print(">> 3. Arrays grandes:")
let array_grande: int[100] = zeros(100)
array_grande[0] = 999
array_grande[50] = 555
array_grande[99] = 111

print("Array de 100 elementos criado!")
print(array_grande)
print("")

// 4. Conversão de tipos (casting)
print(">> 4. Conversão de tipos:")
let num_int: int = 123
let num_float: float = 45.67

let int_para_str: string = to_str(num_int)
let float_para_str: string = to_str(num_float)
let float_para_int: int = to_int(num_float)
let int_para_float: float = to_float(num_int)

print("Int para string: " ++ int_para_str)
print("Float para string: " ++ float_para_str)
print("Float para int: ")
print(float_para_int)
print("Int para float: ")
print(int_para_float)
print("")

// 5. Concatenação de strings
print(">> 5. Concatenação:")
let nome: string = "MiniLang"
let versao: string = "2.0"
let mensagem: string = nome ++ " v" ++ versao ++ " é poderoso!"
print(mensagem)
print("")

// 6. Funções
print(">> 6. Funções:")
func calcular_area_circulo(raio: float) -> float
    let pi: float = 3.14159
    return pi * raio * raio
end

func calcular_media(arr: float[], tamanho: int) -> float
    let soma: float = 0.0
    let i: int = 0
    while i < tamanho do
        soma = soma + arr[i]
        i = i + 1
    end
    return soma / to_float(tamanho)
end

let raio: float = 5.0
let area: float = calcular_area_circulo(raio)
print("Área do círculo com raio ")
print(raio)
print(" = ")
print(area)

let media_temp: float = calcular_media(temperaturas, 7)
print("Temperatura média: ")
print(media_temp)
print("°C")
print("")

// 7. Estruturas condicionais
print(">> 7. Estruturas condicionais:")
let nota: float = 8.5
if nota >= 7.0 then
    print("Aprovado! Nota: ")
    print(nota)
else
    print("Reprovado! Nota: ")
    print(nota)
end
print("")

// 8. Loops
print(">> 8. Loops:")
print("Contagem regressiva:")
let contador: int = 5
while contador > 0 do
    print(contador)
    print("... ")
    contador = contador - 1
end
print("Fogo!")
print("")

// 9. QuickSort para demonstração
print(">> 9. Algoritmo QuickSort:")
func trocar(arr: int[], i: int, j: int) -> void
    let temp: int = arr[i]
    arr[i] = arr[j]
    arr[j] = temp
end

func particionar(arr: int[], baixo: int, alto: int) -> int
    let pivo: int = arr[alto]
    let i: int = baixo - 1
    let j: int = baixo
    
    while j < alto do
        if arr[j] <= pivo then
            i = i + 1
            trocar(arr, i, j)
        end
        j = j + 1
    end
    
    trocar(arr, i + 1, alto)
    return i + 1
end

func quicksort(arr: int[], baixo: int, alto: int) -> void
    if baixo < alto then
        let pi: int = particionar(arr, baixo, alto)
        quicksort(arr, baixo, pi - 1)
        quicksort(arr, pi + 1, alto)
    end
end

let array_para_ordenar: int[6] = [64, 34, 25, 12, 22, 11]
print("Array antes da ordenação:")
print(array_para_ordenar)
print("")

quicksort(array_para_ordenar, 0, 5)

print("Array após ordenação:")
print(array_para_ordenar)
print("")

let arr: int[3] = [1, 2, 3]
print(arr)  // Saída: [1, 2, 3]

let arrf: float[3] = [1.1, 2.2, 3.3]
print(arrf)  // Saída: [1.100000, 2.200000, 3.300000]

let arrs: string[2] = ["abc", "def"]
print(arrs)  // Saída: [abc, def]

print("=== Demonstração concluída com sucesso! ===") 