
func funcao1()
    let array1: int[5] = [1, 2, 3, 4, 5]
    print(array_to_str(array1, 5))
    print(to_str(array1))
end

let array2: int[5] = [1, 2, 3, 4, 5]
func funcao2(array: int[])
    print(array_to_str(array, 5))
    print(to_str(3.5))
end

funcao1()
funcao2(array2)