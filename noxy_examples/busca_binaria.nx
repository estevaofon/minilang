func busca_binaria(array: int[], tamanho: int, alvo: int) -> int
    let esquerda: int = 0
    let direita: int = tamanho - 1
    let conta_iteracoes: int = 0

    while esquerda <= direita do
        let meio: int = (esquerda + direita) / 2
        conta_iteracoes = conta_iteracoes + 1
        print("Iteracao "+to_str(conta_iteracoes)+": procurando na posicao "+to_str(meio))

        if array[meio] == alvo then
            print("Numero total de iteracoes: "+to_str(conta_iteracoes))
            return meio
        end

        if array[meio] < alvo then
            esquerda = meio + 1
        else
            direita = meio - 1
        end
    end

    print("Numero de iteracoes: "+to_str(conta_iteracoes))
    return -1
end

let array: int[10] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
let tamanho: int = 10
let indice: int = busca_binaria(array, tamanho, 3)

print("Indice do alvo: "+to_str(indice))