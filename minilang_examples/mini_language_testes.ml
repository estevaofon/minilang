// ============================================
// FUNÇÃO DE IMPRESSÃO DE ARRAY USANDO TO_STR
// ============================================

func imprimir_array_com_to_str(arr: int[], tamanho: int) -> void
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
    print(resultado)
end

// ============================================
// TESTE DA FUNÇÃO DE IMPRESSÃO
// ============================================

print("=== TESTE FUNÇÃO DE IMPRESSÃO DE ARRAY ===")

// Criar arrays para testar
let array_1: int[7] = [1, 3, 5, 7, 9, 11, 13]
let array_2: int[5] = [10, 20, 30, 40, 50]

// Testar a função length
print("0. Teste da função length:")
print("Tamanho do array_1: " + to_str(length(array_1)))
print("Tamanho do array_2: " + to_str(length(array_2)))

// Testar a função com detecção automática de tamanho
print("1. Primeiro array usando função com detecção automática:")
imprimir_array_com_to_str(array_1, length(array_1))

print("2. Segundo array usando função com detecção automática:")
imprimir_array_com_to_str(array_2, length(array_2))

// Demonstrar uso individual do to_str
print("3. Elementos individuais com to_str:")
print("Primeiro elemento: " + to_str(array_1[0]))
print("Soma dos dois primeiros: " + to_str(array_1[0] + array_1[1]))
print("Média dos três primeiros: " + to_str((array_1[0] + array_1[1] + array_1[2]) / 3))

print("=== TESTE CONCLUÍDO ===")

