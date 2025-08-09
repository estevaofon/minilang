// Teste da função ord
// A função ord deve receber um caractere (string de uma letra) e retornar seu valor Unicode

let char_a: string = "a"
let char_A: string = "A"
let char_0: string = "0"
let char_espaco: string = " "
let char_exclamacao: string = "!"

let valor_a: int = ord(char_a)
let valor_A: int = ord(char_A)
let valor_0: int = ord(char_0)
let valor_espaco: int = ord(char_espaco)
let valor_exclamacao: int = ord(char_exclamacao)

print("Valor Unicode de 'a': " + to_str(valor_a))
print("Valor Unicode de 'A': " + to_str(valor_A))
print("Valor Unicode de '0': " + to_str(valor_0))
print("Valor Unicode de ' ': " + to_str(valor_espaco))
print("Valor Unicode de '!': " + to_str(valor_exclamacao))

// Teste com caractere direto
let valor_direto: int = ord("z")
print("Valor Unicode de 'z': " + to_str(valor_direto))
