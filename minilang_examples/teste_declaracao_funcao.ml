// Teste para declaração de variáveis através do retorno de funções

let notas: int[5] = [10, 8, 9, 7, 6]

// Teste 1: Declaração local com let
let len: int = length(notas)
print("Tamanho do array: ")
print(len)

// Teste 2: Declaração global com global
global tamanho: int = length(notas)
print("Tamanho global: ")
print(tamanho)

// Teste 3: Função que retorna um valor
func soma(a: int, b: int) -> int
    return a + b
end

let resultado: int = soma(5, 3)
print("Resultado da soma: ")
print(resultado)

// Teste 4: Função que retorna float
func media(a: float, b: float) -> float
    return (a + b) / 2.0
end

let media_valor: float = media(10.5, 8.5)
print("Média: ")
print(media_valor)

print("Todos os testes de declaração por função passaram!") 