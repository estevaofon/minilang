// ===================================
// MiniLang v2.0 - Exemplo de HashMap Simples (chave string)
// ===================================

// Função strlen para MiniLang (conta até o caractere nulo)
func len(s: string) -> int
    let i: int = 0
    while s[i] != "\0" do
        i = i + 1
    end
    return i
end

print("=== MiniLang v2.0 - HashMap Simples (chave string) ===")
print("")

// Definição de um HashMap simples para chaves string
// (sem tratamento de colisão, apenas para fins didáticos)

global HASH_SIZE: int = 10
global keys: string[10] = ["", "", "", "", "", "", "", "", "", ""]
global values: int[10] = zeros(10)

// Função de hash simples para string (soma dos códigos dos caracteres)
func hash(key: string) -> int
    let soma: int = 0
    let i: int = 0
    while i < len(key) do
        soma = soma + ord(key[i])
        i = i + 1
    end
    return soma % HASH_SIZE
end

// Função para comparar strings (igualdade)
func str_eq(a: string, b: string) -> int
    if len(a) != len(b) then
        return 0
    end
    let i: int = 0
    while i < len(a) do
        if a[i] != b[i] then
            return 0
        end
        i = i + 1
    end
    return 1
end

// Inserir par chave-valor
func hashmap_put(key: string, value: int) -> void
    let idx: int = hash(key)
    keys[idx] = key
    values[idx] = value
end

// Buscar valor pela chave
func hashmap_get(key: string) -> int
    let idx: int = hash(key)
    if str_eq(keys[idx], key) == 1 then
        return values[idx]
    else
        // Retorna -1 se não encontrado
        return -1
    end
end

// Exemplo de uso
print(">> Inserindo valores no HashMap:")
hashmap_put("foo", 100)
hashmap_put("bar", 200)
hashmap_put("baz", 300)
print("Valor para chave 'foo': ")
print(hashmap_get("foo"))
print("Valor para chave 'bar': ")
print(hashmap_get("bar"))
print("Valor para chave 'baz': ")
print(hashmap_get("baz"))
print("Valor para chave 'qux' (não inserida): ")
print(hashmap_get("qux"))
print("")
print("=== Fim do exemplo de HashMap Simples (chave string) ===") 