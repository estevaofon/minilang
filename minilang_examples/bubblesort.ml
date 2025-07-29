
let desordenado:bool = true
let array: int[6] = [5, 3, 8, 6, 2, 7]

while desordenado do
    desordenado = false
    let i: int = 0
    while i < 5 do
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
print("Ordenado")

print(to_str(array))
    
