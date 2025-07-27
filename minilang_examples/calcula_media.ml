let notas: int[5] = [10, 8, 7, 9, 6]
let tamanho: int = length(notas)

func calcula_media(notas: int[], tamanho: int) -> int
    let soma: int = 0
    let i: int = 0

    while i < tamanho do
        soma = soma + notas[i]
        i = i + 1
    end
    return soma / tamanho
end

print("A média das notas é: ")
print(calcula_media(notas, tamanho))
