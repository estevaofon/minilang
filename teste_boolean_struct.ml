struct Produto
    codigo: int,
    nome: string,
    preco: float,
    disponivel: bool
end

// Teste simples para verificar se o boolean está sendo inicializado corretamente
let produto: Produto = Produto(1, "Teste", 10.0, false)

// Verificar se o valor inicial é false
if produto.disponivel == false then
    print("✓ Boolean inicializado como false")
else
    print("✗ Boolean não foi inicializado como false")
end

// Verificar se podemos modificar o valor
produto.disponivel = true
if produto.disponivel == true then
    print("✓ Boolean modificado para true")
else
    print("✗ Boolean não foi modificado para true")
end

// Teste com true inicial
let produto2: Produto = Produto(2, "Teste2", 20.0, true)
if produto2.disponivel == true then
    print("✓ Boolean inicializado como true")
else
    print("✗ Boolean não foi inicializado como true")
end 