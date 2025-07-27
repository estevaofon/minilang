func imprimir_array(arr: int[], tamanho: int) -> void
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

// Criar arrays para testar
let array_1: int[7] = [1, 3, 5, 7, 9, 11, 13]
let array_2: int[7] = array_1

imprimir_array(array_2, length(array_2))