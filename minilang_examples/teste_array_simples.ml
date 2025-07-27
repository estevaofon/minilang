// ============================================
// MiniLang - Teste de Array Simples
// ============================================

print("=== TESTE DE ARRAY SIMPLES ===")

// Definir struct com array
struct Aluno
    nome: string,
    notas: int[5],
    media: float
end

print("✓ Struct Aluno definido com array")

// Criar aluno
let aluno: Aluno = Aluno("Pedro", [0, 0, 0, 0, 0], 0.0)

print("✓ Aluno criado")

// Atribuir notas
aluno.notas[0] = 8
aluno.notas[1] = 9
aluno.notas[2] = 7
aluno.notas[3] = 10
aluno.notas[4] = 8

print("✓ Notas atribuídas")

// Calcular e atribuir média
aluno.media = 8.4

print("✓ Média calculada e atribuída")

print("=== TESTE CONCLUÍDO ===") 