#!/usr/bin/env python3
"""
Script para testar todas as mensagens de erro do compilador Nox
Executa cada arquivo de teste e captura a saída para análise
"""

import os
import subprocess
import sys
from pathlib import Path

def run_test(test_file):
    """Executa um teste específico e captura a saída"""
    print(f"\n{'='*60}")
    print(f"TESTANDO: {test_file}")
    print('='*60)
    
    try:
        # Executar o compilador com o arquivo de teste
        result = subprocess.run(
            ["uv", "run", "python", "../compiler.py", "--compile", test_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("✅ COMPILAÇÃO BEM-SUCEDIDA (não esperado para arquivo de teste de erro)")
            print("STDOUT:", result.stdout)
        else:
            print("❌ ERRO DETECTADO (esperado):")
            print("STDERR:", result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout)
                
    except Exception as e:
        print(f"💥 ERRO NA EXECUÇÃO: {e}")

def main():
    """Executa todos os testes de erro"""
    print("🧪 INICIANDO TESTES DE MENSAGENS DE ERRO DO COMPILADOR NOX")
    print("=" * 70)
    
    # Diretório atual do script
    test_dir = Path(__file__).parent
    
    # Encontrar todos os arquivos .nx no diretório
    test_files = sorted(test_dir.glob("*.nx"))
    
    if not test_files:
        print("❌ Nenhum arquivo de teste (.nx) encontrado!")
        return
    
    print(f"📁 Encontrados {len(test_files)} arquivos de teste:")
    for f in test_files:
        print(f"  - {f.name}")
    
    print("\n🚀 Executando testes...")
    
    # Executar cada teste
    for test_file in test_files:
        run_test(test_file.name)
    
    print(f"\n{'='*70}")
    print("🏁 TESTES CONCLUÍDOS")
    print("="*70)

if __name__ == "__main__":
    main()
