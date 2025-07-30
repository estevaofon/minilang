struct Produto
    codigo: int,
    nome: string,
    preco: float,
    disponivel: bool
end

let produto: Produto = Produto(1, "Laptop", 2500.50, true)
print(produto.nome) 