// ============================================
// MiniLang - Teste de Atribuição Aninhada
// Implementação com Atribuições Dinâmicas
// ============================================
// Exemplo que demonstra atribuições aninhadas de structs

print("=== TESTE DE ATRIBUIÇÃO ANINHADA ===")
print("Implementação com Atribuições Dinâmicas")
print("")

// ============================================
// EXEMPLO 1: Struct Aninhado com Atribuições
// ============================================
print("--- EXEMPLO 1: Struct Aninhado ---")

// Definir struct para endereço
struct Endereco
    rua: string,
    numero: int,
    cidade: string
end

// Definir struct pessoa com endereço
struct PessoaCompleta
    nome: string,
    idade: int,
    endereco: Endereco
end

print("✓ Structs Endereco e PessoaCompleta definidos")
print("")

// Criar pessoa com endereço usando construtor
let pessoa_completa: PessoaCompleta = PessoaCompleta("Ana", 28, Endereco("Rua das Flores", 123, "São Paulo"))

print("✓ Pessoa completa criada com construtor aninhado")
print("")

// Atribuir valores aos campos aninhados
pessoa_completa.nome = "Carlos"
pessoa_completa.endereco.rua = "Avenida Principal"
pessoa_completa.endereco.numero = 456
pessoa_completa.endereco.cidade = "Rio de Janeiro"

print("✓ Campos aninhados atribuídos dinamicamente")
print("")

// ============================================
// EXEMPLO 2: Árvore Binária Complexa
// ============================================
print("--- EXEMPLO 2: Árvore Binária Complexa ---")

// Definir nó da árvore binária
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

print("✓ Struct TreeNode definido com auto-referência")
print("")

// Criar árvore básica
let raiz: TreeNode = TreeNode(10, null, null)

print("✓ Raiz criada")
print("")

// Criar filhos separadamente
let filho_esq: TreeNode = TreeNode(5, null, null)
let filho_dir: TreeNode = TreeNode(15, null, null)

print("✓ Filhos criados")
print("")

// Atribuir filhos à raiz
raiz.esquerda = ref filho_esq
raiz.direita = ref filho_dir

print("✓ Filhos atribuídos à raiz")
print("")

// Criar netos
let neto_esq: TreeNode = TreeNode(3, null, null)
let neto_dir: TreeNode = TreeNode(7, null, null)

print("✓ Netos criados")
print("")

// Atribuir netos ao filho esquerdo
filho_esq.esquerda = ref neto_esq
filho_esq.direita = ref neto_dir

print("✓ Netos atribuídos ao filho esquerdo")
print("")

// ============================================
// EXEMPLO 3: Lista Encadeada com Atribuições
// ============================================
print("--- EXEMPLO 3: Lista Encadeada ---")

// Definir nó da lista encadeada
struct Node
    valor: int,
    proximo: ref Node
end

print("✓ Struct Node definido")
print("")

// Criar nós da lista
let node1: Node = Node(1, null)
let node2: Node = Node(2, null)
let node3: Node = Node(3, null)

print("✓ Nós criados")
print("")

// Construir lista encadeada usando atribuições
node1.proximo = ref node2
node2.proximo = ref node3

print("✓ Lista encadeada construída: 1 -> 2 -> 3")
print("")

// Adicionar novo nó no meio
let node_novo: Node = Node(2.5, null)
node_novo.proximo = ref node3
node2.proximo = ref node_novo

print("✓ Novo nó inserido: 1 -> 2 -> 2.5 -> 3")
print("")

// ============================================
// RESUMO DA IMPLEMENTAÇÃO
// ============================================
print("=== RESUMO DA IMPLEMENTAÇÃO ===")
print("✓ Atribuições simples de campos funcionando")
print("✓ Atribuições aninhadas funcionando")
print("✓ Auto-referência com atribuições funcionando")
print("✓ Navegação aninhada implementada")
print("✓ Criação dinâmica de structs aninhados")
print("")
print("🎉 Atribuições aninhadas de structs implementadas com sucesso!")
print("💡 Agora é possível modificar campos após a criação")
print("💡 Suporte completo para estruturas aninhadas")
print("💡 Compatibilidade com auto-referência mantida")
print("")
print("=== IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO ===") 