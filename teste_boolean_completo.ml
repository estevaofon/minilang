// Simulando o contexto completo do arquivo de testes
print("=== INICIANDO TESTES UNITÁRIOS AUTOMATIZADOS ===")
print("")

// Contador global de testes (como no arquivo original)
global contador_testes: int = 0
global testes_passaram: int = 0
global testes_falharam: int = 0

// Função assert para validação automática (como no arquivo original)
func assert(condicao: bool, mensagem: string) -> void
    contador_testes = contador_testes + 1
    
    if condicao then
        testes_passaram = testes_passaram + 1
        print("✓ Teste ")
        print(contador_testes)
        print(" passou: ")
        print(mensagem)
    else
        testes_falharam = testes_falharam + 1
        print("✗ Teste ")
        print(contador_testes)
        print(" FALHOU: ")
        print(mensagem)
    end
end

// Definindo o struct Produto
struct Produto
    codigo: int,
    nome: string,
    preco: float,
    disponivel: bool
end

// Simulando alguns testes anteriores para criar contexto
print(">> Simulando testes anteriores...")

let a: int = 10
let b: int = 5
assert(a + b == 15, "Teste básico de soma")

let texto: string = "Teste"
assert(texto == "Teste", "Teste básico de string")

// Agora o teste específico que falha
print(">> 16. TESTES DE CONSTRUTORES E INICIALIZAÇÃO")

let produto2: Produto = Produto(2, "Mouse", 45.99, false)

// Este é o teste que falha no arquivo original
assert(produto2.disponivel == false, "Disponibilidade do produto 2 deve ser false")

// Teste de modificação
produto2.disponivel = true
assert(produto2.disponivel == true, "Disponibilidade do produto 2 deve ser modificada para true") 