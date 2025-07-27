// ============================================
// DEBUG - TESTE DE MÉDIA SIMPLIFICADO
// ============================================

print("=== DEBUG - TESTE DE MÉDIA ===")

global notas: int[5] = [10, 8, 7, 9, 6]

// Teste 1: Verificar length global
let tamanho_global: int = length(notas)
print("1. Tamanho global: " + to_str(tamanho_global))

// Teste 2: Função simples para testar length
func test_length(arr: int[]) -> int
    return length(arr)
end

let tamanho_func: int = test_length(notas)
print("2. Tamanho via função: " + to_str(tamanho_func))

// Teste 3: Soma manual
let soma: int = notas[0] + notas[1] + notas[2] + notas[3] + notas[4]
print("3. Soma manual: " + to_str(soma))

// Teste 4: Média manual
let media_manual: int = soma / 5
print("4. Média manual: " + to_str(media_manual))

// Teste 5: Função de média corrigida
func calcula_media_simples(notas: int[]) -> int
    let soma: int = notas[0] + notas[1] + notas[2] + notas[3] + notas[4]
    return soma / 5
end

let media_func: int = calcula_media_simples(notas)
print("5. Média via função: " + to_str(media_func))

print("=== DEBUG CONCLUÍDO ===") 