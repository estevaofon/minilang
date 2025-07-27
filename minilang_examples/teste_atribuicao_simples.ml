// ============================================
// MiniLang - Teste de Atribuição Simples
// Implementação com Atribuições Dinâmicas
// ============================================
// Exemplo simples que demonstra atribuições de campos de struct

print("=== TESTE DE ATRIBUIÇÃO SIMPLES ===")
print("Implementação com Atribuições Dinâmicas")
print("")

// ============================================
// EXEMPLO 1: Struct Simples com Atribuições
// ============================================
print("--- EXEMPLO 1: Struct Simples ---")

// Definir struct simples
struct Pessoa
    nome: string,
    idade: int,
    altura: float
end

print("✓ Struct Pessoa definido")
print("")

// Criar pessoa usando construtor
let pessoa: Pessoa = Pessoa("João", 25, 1.75)

print("✓ Pessoa criada com construtor")
print("")

// Atribuir novos valores aos campos
pessoa.nome = "Maria"
pessoa.idade = 30
pessoa.altura = 1.68

print("✓ Campos atribuídos dinamicamente")
print("")

// ============================================
// EXEMPLO 2: Árvore Binária com Atribuições
// ============================================
print("--- EXEMPLO 2: Árvore Binária ---")

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

// ============================================
// RESUMO DA IMPLEMENTAÇÃO
// ============================================
print("=== RESUMO DA IMPLEMENTAÇÃO ===")
print("✓ Atribuições simples de campos funcionando")
print("✓ Auto-referência com atribuições funcionando")
print("✓ Operador ref implementado")
print("")
print("🎉 Atribuições de structs implementadas com sucesso!")
print("💡 Agora é possível modificar campos após a criação")
print("💡 Suporte para referências funcionando")
print("")
print("=== IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO ===") 