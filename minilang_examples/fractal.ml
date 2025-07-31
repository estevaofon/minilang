print("=== TRIANGULO DE SIERPINSKI ===")
print("")

// Funcao para criar string com espacos
func criar_espacos(n: int) -> string
    let resultado: string = ""
    let i: int = 0
    while i < n do
        resultado = resultado + " "
        i = i + 1
    end
    return resultado
end

// Funcao para potencia de 2
func pot2(n: int) -> int
    let res: int = 1
    let i: int = 0
    while i < n do
        res = res * 2
        i = i + 1
    end
    return res
end

// Funcao principal do Sierpinski
func sierpinski(ordem: int) -> void
    let tamanho: int = pot2(ordem)
    print("Ordem: " + to_str(ordem) + " - Tamanho: " + to_str(tamanho))
    print("")
    
    let linha: int = 0
    while linha < tamanho do
        // Construir a linha como uma string
        let linha_str: string = ""
        
        // Adicionar espacos iniciais para centralizar
        linha_str = linha_str + criar_espacos(tamanho - linha - 1)
        
        let coluna: int = 0
        while coluna <= linha do
            // Logica do triangulo de Pascal
            // Se (linha & coluna) == coluna, desenha
            let l: int = linha
            let c: int = coluna
            let desenha: bool = true
            
            // Simula AND bit a bit
            while c > 0 do
                if (l % 2 == 0) & (c % 2 == 1) then
                    desenha = false
                    c = 0  // Sair do loop
                else
                    l = l / 2
                    c = c / 2
                end
            end
            
            if desenha then
                linha_str = linha_str + "* "
            else
                linha_str = linha_str + "  "
            end
            
            coluna = coluna + 1
        end
        
        // Imprimir a linha completa
        print(linha_str)
        linha = linha + 1
    end
end

// Versao com array de strings
func sierpinski_array(ordem: int) -> void
    let tamanho: int = pot2(ordem)
    print("")
    print("Sierpinski com Array - Ordem: " + to_str(ordem))
    print("")
    
    // Array para armazenar as linhas (suporta até ordem 6 = 64 linhas)
    let linhas: string[64] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 
                              "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                              "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                              "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    
    let linha: int = 0
    while linha < tamanho do
        // Construir cada linha
        let linha_atual: string = criar_espacos(tamanho - linha - 1)
        
        let coluna: int = 0
        while coluna <= linha do
            let l: int = linha
            let c: int = coluna
            let desenha: bool = true
            
            // Simula AND bit a bit
            while c > 0 do
                if (l % 2 == 0) & (c % 2 == 1) then
                    desenha = false
                    c = 0
                else
                    l = l / 2
                    c = c / 2
                end
            end
            
            if desenha then
                linha_atual = linha_atual + "*"
            else
                linha_atual = linha_atual + " "
            end
            
            if coluna < linha then
                linha_atual = linha_atual + " "
            end
            
            coluna = coluna + 1
        end
        
        linhas[linha] = linha_atual
        linha = linha + 1
    end
    
    // Imprimir todas as linhas
    let i: int = 0
    while i < tamanho do
        print(linhas[i])
        i = i + 1
    end
end

print("")
print("1. Sierpinski com array de strings - Ordem 5:")
sierpinski_array(5)

print("")
print("=== PROPRIEDADES DO FRACTAL ===")
print("- Auto-similaridade em todas as escalas")
print("- Dimensao fractal: log(3)/log(2) = 1.585")
print("- Construido com triangulo de Pascal mod 2")
print("")
print("=== FIM ===")
