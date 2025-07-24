// ===================================
// MiniLang v2.0 - Exemplo de teste
// ===================================

print("=== MiniLang v2.0 - Teste de Arquivo ===")
print("")

// Demonstração básica
print(">> Teste básico:")
let x: int = 42
let y: float = 3.14
let texto: string = "Olá, mundo!"

print("x = ")
print(x)
print("y = ")
print(y)
print("texto = " ++ texto)
print("")

// Arrays
print(">> Teste de arrays:")
let numeros: int[5] = [1, 2, 3, 4, 5]
print("Array criado com sucesso!")
print("Primeiro elemento: ")
print(numeros[0])
print("Último elemento: ")
print(numeros[4])
print("")

// Função simples
func dobrar(valor: int) -> int
    return valor * 2
end

let resultado: int = dobrar(10)
print("Dobro de 10 = ")
print(resultado)
print("")

print("=== Teste concluído com sucesso! ===") 