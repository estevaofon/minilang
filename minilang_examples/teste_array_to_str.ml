// TESTE DAS NOVAS FUNCIONALIDADES: array_to_str E to_str COM ARRAYS

// Teste 1: Função array_to_str nativa
let array1: int[5] = [1, 2, 3, 4, 5]
let array2: float[3] = [1.5, 2.7, 3.14]

print("=== TESTE 1: Função array_to_str nativa ===")
print("Array de int: " + array_to_str(array1, 5))
print("Array de float: " + array_to_str(array2, 3))

// Teste 2: Função to_str com arrays
print("\n=== TESTE 2: Função to_str com arrays ===")
print("to_str(array1): " + to_str(array1))
print("to_str(array2): " + to_str(array2))

// Teste 3: Arrays vazios
let array_vazio: int[0] = []
print("\n=== TESTE 3: Arrays vazios ===")
print("Array vazio: " + array_to_str(array_vazio, 0))
print("to_str(array_vazio): " + to_str(array_vazio))

// Teste 4: Arrays com um elemento
let array_um: int[1] = [42]
let array_um_float: float[1] = [3.14159]
print("\n=== TESTE 4: Arrays com um elemento ===")
print("Array com um int: " + array_to_str(array_um, 1))
print("Array com um float: " + array_to_str(array_um_float, 1))
print("to_str(array_um): " + to_str(array_um))
print("to_str(array_um_float): " + to_str(array_um_float))

// Teste 5: Arrays grandes
let array_grande: int[10] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print("\n=== TESTE 5: Arrays grandes ===")
print("Array grande: " + array_to_str(array_grande, 10))
print("to_str(array_grande): " + to_str(array_grande))

// Teste 6: Concatenação com strings
print("\n=== TESTE 6: Concatenação com strings ===")
print("Resultado: " + "Array: " + to_str(array1) + " e " + to_str(array2))

// Teste 7: Comparação de strings
let str1: string = to_str(array1)
let str2: string = array_to_str(array1, 5)
print("\n=== TESTE 7: Comparação de strings ===")
print("to_str(array1): " + str1)
print("array_to_str(array1, 5): " + str2)

// Teste 8: Arrays com valores negativos
let array_neg: int[4] = [-1, -2, -3, -4]
print("\n=== TESTE 8: Arrays com valores negativos ===")
print("Array com negativos: " + to_str(array_neg))

// Teste 9: Arrays com floats pequenos e grandes
let array_floats: float[4] = [0.001, 1234.5678, -0.5, 999999.999999]
print("\n=== TESTE 9: Arrays com floats variados ===")
print("Array com floats: " + to_str(array_floats))

print("\n=== TESTES CONCLUÍDOS ===") 