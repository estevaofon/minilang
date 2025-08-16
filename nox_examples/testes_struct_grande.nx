// Função assert para validação automática
func assert(condicao: bool, mensagem: string) -> void
    if condicao then
        print("✓ Teste passou: ")
        print(mensagem)
    else
        print("✗ Teste FALHOU: ")
        print(mensagem)
    end
end

struct ProdutoGrande
    codigo: int,
    nome: string,
    preco: float,
    disponivel: bool,
    quantidade: int,
    categoria: string,
    peso: float,
    promocao: bool,
    vendas: int,
    fornecedor: string
end

struct Cliente
    id: int,
    nome: string,
    email: string,
    ativo: bool,
    credito: float
end

struct Pedido
    numero: int,
    cliente: Cliente,
    produto: ProdutoGrande,
    quantidade: int,
    valor_total: float,
    pago: bool
end

// Teste com struct grande
let produto1: ProdutoGrande = ProdutoGrande(1, "Laptop Gaming", 3500.00, true, 10, "Eletronicos", 2.5, false, 150, "TechCorp")

// Teste com struct aninhado
let cliente1: Cliente = Cliente(1001, "Joao Silva", "joao@email.com", true, 5000.00)
let pedido1: Pedido = Pedido(2001, cliente1, produto1, 2, 7000.00, false)

// Verificações
assert(produto1.codigo == 1, "Codigo do produto deve ser 1")
assert(produto1.nome == "Laptop Gaming", "Nome do produto deve ser 'Laptop Gaming'")
assert(produto1.disponivel == true, "Produto deve estar disponivel")
assert(produto1.quantidade == 10, "Quantidade deve ser 10")

assert(cliente1.id == 1001, "ID do cliente deve ser 1001")
assert(cliente1.nome == "Joao Silva", "Nome do cliente deve ser 'Joao Silva'")
assert(cliente1.ativo == true, "Cliente deve estar ativo")

assert(pedido1.numero == 2001, "Numero do pedido deve ser 2001")
assert(pedido1.quantidade == 2, "Quantidade do pedido deve ser 2")
assert(pedido1.pago == false, "Pedido nao deve estar pago")

print("✓ Teste com structs grandes passou!") 
