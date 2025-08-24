#!/usr/bin/env python3
"""
Script para executar todos os arquivos de exemplo Noxy
Executa cada arquivo sequencialmente com um intervalo de 3 segundos entre execuções
"""

import os
import subprocess
import time
import sys
from pathlib import Path

def run_noxy_file(file_path):
    """
    Executa um arquivo Noxy usando o pipeline completo:
    1. Compila com o compilador Noxy
    2. Link com as funções de casting em C
    3. Executa o programa resultante
    """
    file_name = os.path.basename(file_path)
    print(f"\n{'='*60}")
    print(f"🚀 Executando: {file_name}")
    print(f"{'='*60}")
    
    try:
        # Comando completo para compilar e executar
        cmd = f'uv run python compiler.py --compile ".\\noxy_examples\\{file_name}" && gcc -mcmodel=large casting_functions.c output.obj -o programa.exe && .\\programa.exe'
        
        print(f"📝 Comando: {cmd}")
        print(f"⏳ Executando...")
        
        # Executar o comando usando shell=True para Windows
        # Configurar encoding para UTF-8 para evitar problemas de unicode
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Substituir caracteres problemáticos
            timeout=30  # Timeout de 30 segundos por arquivo
        )
        
        if result.returncode == 0:
            print(f"✅ {file_name} executado com sucesso!")
            if result.stdout.strip():
                print(f"📤 Saída:")
                print(result.stdout)
        else:
            print(f"❌ Erro ao executar {file_name}")
            if result.stderr.strip():
                print(f"🚨 Erro:")
                print(result.stderr)
            if result.stdout.strip():
                print(f"📤 Saída:")
                print(result.stdout)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {file_name} demorou mais de 30 segundos")
        return False
    except Exception as e:
        print(f"💥 Exceção ao executar {file_name}: {e}")
        return False

def main():
    """Função principal"""
    print("🎯 Script de Execução de Exemplos Noxy")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("noxy_examples"):
        print("❌ Diretório 'noxy_examples' não encontrado!")
        print("   Certifique-se de executar este script na raiz do projeto Noxy")
        sys.exit(1)
    
    # Verificar se os arquivos necessários existem
    required_files = ["compiler.py", "casting_functions.c"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Arquivo necessário '{file}' não encontrado!")
            sys.exit(1)
    
    # Obter lista de arquivos .nx na pasta noxy_examples
    examples_dir = Path("noxy_examples")
    nx_files = sorted(examples_dir.glob("*.nx"))
    
    if not nx_files:
        print("❌ Nenhum arquivo .nx encontrado em noxy_examples/")
        sys.exit(1)
    
    print(f"📁 Encontrados {len(nx_files)} arquivos de exemplo:")
    for i, file in enumerate(nx_files, 1):
        print(f"   {i:2d}. {file.name}")
    
    print(f"\n🕐 Intervalo entre execuções: 3 segundos")
    print(f"⏱️  Timeout por arquivo: 30 segundos")
    print(f"\n{'='*60}")
    
    # Confirmar execução
    try:
        response = input("Deseja continuar? (y/N): ").lower().strip()
        if response not in ['y', 'yes', 's', 'sim']:
            print("❌ Execução cancelada pelo usuário")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n❌ Execução cancelada")
        sys.exit(0)
    
    # Executar cada arquivo
    successful = 0
    failed = 0
    
    start_time = time.time()
    
    for i, file_path in enumerate(nx_files, 1):
        print(f"\n📊 Progresso: {i}/{len(nx_files)}")
        
        if run_noxy_file(file_path):
            successful += 1
        else:
            failed += 1
        
        # Aguardar 3 segundos antes do próximo arquivo (exceto no último)
        if i < len(nx_files):
            print(f"\n⏳ Aguardando 1 segundos antes do próximo arquivo...")
            time.sleep(1)
    
    # Relatório final
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n{'='*60}")
    print(f"📋 RELATÓRIO FINAL")
    print(f"{'='*60}")
    print(f"✅ Arquivos executados com sucesso: {successful}")
    print(f"❌ Arquivos com erro: {failed}")
    print(f"📁 Total de arquivos: {len(nx_files)}")
    print(f"⏱️  Tempo total de execução: {total_time:.2f} segundos")
    print(f"📈 Taxa de sucesso: {(successful/len(nx_files)*100):.1f}%")
    
    if failed > 0:
        print(f"\n⚠️  {failed} arquivo(s) falharam na execução")
        sys.exit(1)
    else:
        print(f"\n🎉 Todos os arquivos foram executados com sucesso!")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Execução interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        sys.exit(1)
