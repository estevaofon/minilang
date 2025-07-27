print("Testando a keyword break em loops while")

// Teste básico do break
let i: int = 0
while i < 10 do
    print("i = ")
    print(i)
    if i == 5 then
        break
    end
    i = i + 1
end

print("Loop terminado com break")

// Teste do break em loop aninhado
let x: int = 0
let y: int = 0

while x < 3 do
    print("x = ")
    print(x)
    y = 0
    while y < 5 do
        print("  y = ")
        print(y)
        if x == 1 & y == 2 then
            break
        end
        y = y + 1
    end
    x = x + 1
end

print("Loops aninhados terminados")

// Teste do break com condição complexa
let contador: int = 0
let encontrado: bool = false

while contador < 20 do
    print("Contador: ")
    print(contador)
    
    if contador > 10 & contador % 3 == 0 then
        print("Encontrado número > 10 e divisível por 3!")
        break
    end
    
    contador = contador + 1
end

print("Programa finalizado com sucesso!") 