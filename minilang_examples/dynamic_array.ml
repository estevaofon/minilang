// ============================================
// IMPLEMENTAÇÃO DE ARRAY DINÂMICO EM MINILANG
// ============================================

// Definir a estrutura do array dinâmico
struct DynamicArray
    elementos: int[100],      // Array interno para armazenar os elementos
    capacidade: int,          // Capacidade máxima atual
    tamanho: int              // Número atual de elementos
end

// Função para criar um novo array dinâmico
func criar_array_dinamico() -> DynamicArray
    let array: int[100] = zeros(100)  // Array fixo de 100 elementos
    return DynamicArray(array, 100, 0)  // Capacidade fixa de 100, tamanho inicial 0
end

// Função para adicionar elemento ao final do array
func adicionar_elemento(arr: ref DynamicArray, elemento: int) -> void
    if arr.tamanho >= arr.capacidade then
        print("ERRO: Array está cheio! Não é possível adicionar mais elementos.")
        return
    end
    
    arr.elementos[arr.tamanho] = elemento
    arr.tamanho = arr.tamanho + 1
    
    //print("Elemento " + to_str(elemento) + " adicionado na posição " + to_str(arr.tamanho - 1))
end

// Função para obter elemento de uma posição
func obter_elemento(arr: ref DynamicArray, posicao: int) -> int
    if posicao < 0 | posicao >= arr.tamanho then
        print("ERRO: Posição inválida: " + to_str(posicao))
        return 0
    end
    
    return arr.elementos[posicao]
end

// Função para imprimir o array
func imprimir_array(arr: ref DynamicArray) -> void
    print("Array Dinâmico:")
    print("  Tamanho: " + to_str(arr.tamanho))
    print("  Capacidade: " + to_str(arr.capacidade))
    
    // Construir a string dos elementos em uma linha
    let elementos_str: string = "["
    
    let i: int = 0
    while i < arr.tamanho do
        if i > 0 then
            elementos_str = elementos_str + ", "
        end
        elementos_str = elementos_str + to_str(arr.elementos[i])
        i = i + 1
    end
    
    elementos_str = elementos_str + "]"
    print("  Elementos: " + elementos_str)
end

// ============================================
// TESTES DO ARRAY DINÂMICO
// ============================================

// Criar array dinâmico como variável local (sem malloc)
let meu_array: DynamicArray = criar_array_dinamico()
// imprimir_array(meu_array)

print("")
print("=== ADICIONANDO ELEMENTOS ===")

// Adicionar elementos
adicionar_elemento(meu_array, 10)
adicionar_elemento(meu_array, 25)
adicionar_elemento(meu_array, 7)
adicionar_elemento(meu_array, 42)
adicionar_elemento(meu_array, 100)
adicionar_elemento(meu_array, 200)
adicionar_elemento(meu_array, 300)
adicionar_elemento(meu_array, 400)
adicionar_elemento(meu_array, 500)
adicionar_elemento(meu_array, 600)
adicionar_elemento(meu_array, 700)
adicionar_elemento(meu_array, 800)
adicionar_elemento(meu_array, 900)
adicionar_elemento(meu_array, 1000)

imprimir_array(meu_array)