func partition(array: int[], low: int, high: int) -> int
    let i: int = low - 1
    let j: int = low
    let pivot: int = array[high]
    while j < high do
        if array[j] <= pivot then
            let temp: int = 0
            i = i + 1
            temp = array[i]
            array[i] = array[j]
            array[j] = temp
        end
        j = j + 1
    end
    
    let temp: int = 0
    temp = array[high]
    array[high] = array[i +1]
    array[i + 1] = temp
    return i + 1
end


func quicksort(array: int[], low: int, high: int)
    if low < high then
        let pi: int = partition(array, low, high)
        quicksort(array, low, pi - 1)
        quicksort(array, pi+1, high)
    end
end

let array: int[15] = [10, 7, 8, 9, 1, 5, 2, 6, 3, 4, 15, 12, 11, 14, 13, 0]
quicksort(array, 0, 15)
print(to_str(array))
