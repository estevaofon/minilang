struct Produto
    codigo: int,
    nome: string,
    preco: float,
    disponivel: bool
end

let produto: Produto = Produto(1, "Teste", 10.0, false)

print("Valor do campo disponivel: ")
print(produto.disponivel)

assert(produto.disponivel == false, "Disponibilidade deve ser false") 