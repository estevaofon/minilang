// Teste simples para verificar comparação com caractere nulo
func len(s: string) -> int
    let i: int = 0
    while s[i] != "\0" do
        i = i + 1
    end
    return i
end

let texto: string = "abc"
print("Tamanho de 'abc': ")
print(len(texto)) 