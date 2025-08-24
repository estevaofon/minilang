
func bubblesort(array: int[], tamanho: int) -> void
    let desordenado: bool = true
    while desordenado do
        desordenado = false
        let i: int = 0
        while i < (tamanho - 1) do
            if array[i] > array[i + 1] then
                let temp: int = 0
                temp = array[i]
                array[i] = array[i + 1]
                array[i + 1] = temp
                desordenado = true
            end
            i = i + 1
        end
    end
end

let arr: int[6] = [5, 3, 8, 6, 2, 7]
bubblesort(arr, 6)
print(to_str(arr))

func bubblesort_ref(array: int[], tamanho: int) -> int[]
    let desordenado: bool = true
    while desordenado do
        desordenado = false
        let i: int = 0
        while i < (tamanho - 1) do
            if array[i] > array[i + 1] then
                let temp: int = 0
                temp = array[i]
                array[i] = array[i + 1]
                array[i + 1] = temp
                desordenado = true
            end
            i = i + 1
        end
    end
    return array
end

let arr_ref: int[6] = [23, 6, 32, 64, 2, 7]

func print_ref(array: int[], tamanho: int) -> void
    let i: int = 0
    while i < tamanho  do
        print(to_str(array[i]) + " ")
        i = i + 1
    end
end

print_ref(bubblesort_ref(arr_ref, 6),6)
