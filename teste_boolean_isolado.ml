// Teste isolado que reproduz o problema do teste 67
struct Produto
    codigo: int,
    nome: string,
    preco: float,
    disponivel: bool
end

// Função assert para simular o contexto dos testes
func assert(condicao: bool, mensagem: string) -> void
    if condicao == false then
        print("FALHOU: ")
        print(mensagem)
    else
        print("✓ Teste passou")
    end
end

// Teste exato do produto2 que falha
let produto2: Produto = Produto(2, "Mouse", 45.99, false)

// Verificar se o valor inicial é false (este é o teste que falha)
assert(produto2.disponivel == false, "Disponibilidade do produto 2 deve ser false")

// Verificar se podemos modificar o valor
produto2.disponivel = true
assert(produto2.disponivel == true, "Disponibilidade do produto 2 deve ser modificada para true") 