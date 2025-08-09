// Teste de acesso a caracteres individuais de strings
let texto: string = "hello"
let primeiro: string = texto[0]
let segundo: string = texto[1]
let terceiro: string = texto[2]

print("Primeiro caractere: ")
print(primeiro)

print("Segundo caractere: ")
print(segundo)

print("Terceiro caractere: ")
print(terceiro)

// Teste com string literal direta
let letra: string = "world"[1]
print("Letra de 'world'[1]: ")
print(letra)

// Teste com índice variável
let i: int = 0
let char: string = texto[i]
print("Caractere no índice ")
print(to_str(i))
print(": ")
print(char)

let first_three_chars: string[3] = ["", "", ""]
first_three_chars[0] = texto[0]
first_three_chars[1] = texto[1]
first_three_chars[2] = texto[2]

while i < strlen(texto) do
    print(texto[i])
    i = i + 1
end

print(first_three_chars[1])