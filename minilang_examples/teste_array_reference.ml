// ============================================
// TESTE DE REFERÊNCIAS DE ARRAYS
// ============================================

print("=== TESTE DE REFERÊNCIAS DE ARRAYS ===")

func array_to_str(arr: int[], tamanho: int) -> string
    let resultado: string = "["
    
    let i: int = 0
    while i < tamanho do
        let elemento: int = arr[i]
        
        if i > 0 then
            resultado = resultado + ", "
        end
        
        resultado = resultado + to_str(elemento)
        i = i + 1
    end
    
    resultado = resultado + "]"
    return resultado
end

// Criar arrays para testar
let array_original: int[5] = [10, 20, 30, 40, 50]
let array_referencia: ref int[5] = ref array_original

print("1. Array original:")
print("Tamanho: " + to_str(length(array_original)))
print("Primeiro elemento: " + to_str(array_original[0]))

print("Array original: " + array_to_str(array_original, length(array_original)))

print("2. Tentativa de referência:")
print("Tamanho da referência: " + to_str(length(array_referencia)))

// Testar modificação através da referência
array_referencia[0] = 100

print("3. Após modificação:")
print("Array original[0]: " + to_str(array_original[0]))
print("Array referência[0]: " + to_str(array_referencia[0]))
print("Array referência: " + array_to_str(array_referencia, length(array_referencia)))
print("Array original: " + array_to_str(array_original, length(array_original)))

print("=== TESTE CONCLUÍDO ===") 