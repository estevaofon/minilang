// ============================================
// TESTE DE LENGTH EM VARIÁVEIS GLOBAIS
// ============================================

print("=== TESTE DE LENGTH EM VARIÁVEIS GLOBAIS ===")

// Criar array global
global notas: int[7] = [85, 92, 78, 96, 88, 91, 87]

// Tentar usar length em variável global
global tamanho: int = length(notas)

print("1. Array global criado:")
print("Tamanho do array: " + to_str(tamanho))

print("2. Verificação direta:")
print("Tamanho usando length(notas): " + to_str(length(notas)))

print("3. Acesso aos elementos:")
print("Primeira nota: " + to_str(notas[0]))
print("Última nota: " + to_str(notas[6]))

print("=== TESTE CONCLUÍDO ===")