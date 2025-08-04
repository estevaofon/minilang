// Função assert para validação automática
func assert(condicao: bool, mensagem: str) -> void
    if condicao then
        print("✓ Teste passou: ")
        print(mensagem)
    else
        print("✗ Teste FALHOU: ")
        print(mensagem)
    end
end

struct Produto
    codigo: int,
    nome: str,
    preco: float,
    disponivel: bool
end

// Teste simples
let produto1: Produto = Produto(1, "Laptop", 2500.00, true)

// Verificações
assert(produto1.codigo == 1, "Codigo do produto deve ser 1")
assert(produto1.disponivel == true, "Produto deve estar disponivel")

print("✓ Teste com struct simples passou!") 