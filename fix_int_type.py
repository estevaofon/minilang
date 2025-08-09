#!/usr/bin/env python3

def fix_int_type():
    with open('compiler.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir todas as ocorrências de ir.IntType(32) por self.int_type na função de concatenação
    # Apenas nas linhas específicas da função de concatenação
    lines = content.split('\n')
    
    # Linhas que precisam ser corrigidas na função de concatenação
    target_lines = [3207, 3226, 3248, 3267]
    
    for i, line in enumerate(lines, 1):
        if i in target_lines and 'ir.IntType(32)' in line:
            lines[i-1] = line.replace('ir.IntType(32)', 'self.int_type')
            print(f"Corrigindo linha {i}: {line.strip()}")
    
    # Salvar o arquivo corrigido
    with open('compiler.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print("Arquivo corrigido!")

if __name__ == "__main__":
    fix_int_type()
