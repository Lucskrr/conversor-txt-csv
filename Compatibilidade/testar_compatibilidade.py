#!/usr/bin/env python3
"""
Script para testar compatibilidade com arquivos TOTVS
Valida o parsing e conversão dos formatos suportados
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from parsers import FormatDetector, Record, GERR004Parser, CDFR054Parser
from utils.logger import get_logger

def test_compatibility():
    """Testa compatibilidade com arquivos de exemplo"""
    logger = get_logger(__name__)
    
    print("🔍 Testando Compatibilidade de Arquivos TOTVS")
    print("=" * 50)
    
    # Arquivos de teste
    test_files = [
        {
            'path': 'gerr004.P00 contagem.txt',
            'expected_format': 'gerr004',
            'expected_version': 'P00'
        },
        {
            'path': 'cdfr054.P08.txt',
            'expected_format': 'cdfr054',
            'expected_version': 'P08'
        },
        {
            'path': 'cdfr054.P06.txt',
            'expected_format': 'cdfr054',
            'expected_version': 'P06'
        }
    ]
    
    results = []
    
    for test_file in test_files:
        file_path = Path(__file__).parent / test_file['path']
        
        if not file_path.exists():
            print(f"❌ Arquivo não encontrado: {test_file['path']}")
            results.append({
                'file': test_file['path'],
                'status': 'ERROR',
                'message': 'Arquivo não encontrado'
            })
            continue
        
        try:
            print(f"\n📁 Testando: {test_file['path']}")
            print(f"   Tamanho: {file_path.stat().st_size} bytes")
            
            # Ler conteúdo
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Detectar formato
            format_info = FormatDetector.detect_format(str(file_path))
            print(f"   🎯 Formato detectado: {format_info}")
            print(f"   🔍 Tipo: {type(format_info)}")
            
            if not format_info:
                print(f"   ❌ Formato não detectado!")
                results.append({
                    'file': test_file['path'],
                    'status': 'ERROR',
                    'message': 'Formato não detectado'
                })
                continue
            
            # Validar formato esperado
            if format_info.upper() == test_file['expected_format'].upper():
                print(f"   ✅ Formato correto: {format_info}")
            else:
                print(f"   ❌ Formato incorreto. Esperado: {test_file['expected_format']}")
                print(f"   🔍 Detectado: '{format_info}' vs Esperado: '{test_file['expected_format']}'")
                results.append({
                    'file': test_file['path'],
                    'status': 'ERROR',
                    'message': f'Formato incorreto: {format_info}'
                })
                continue
            
            # Testar parsing
            if format_info.upper() == 'GERR004':
                lines = content.split('\n')
                parsed_data = GERR004Parser.parse(lines)
            elif format_info.upper() == 'CDFR054':
                lines = content.split('\n')
                parsed_data = CDFR054Parser.parse(lines)
            else:
                print(f"   ❌ Parser não implementado para: {format_info}")
                results.append({
                    'file': test_file['path'],
                    'status': 'ERROR',
                    'message': f'Parser não implementado'
                })
                continue
            
            # Validar parsing
            if parsed_data and len(parsed_data) > 0:
                print(f"   ✅ Parsing bem-sucedido")
                print(f"   📊 Registros processados: {len(parsed_data)}")
                
                # Mostrar primeiro registro como exemplo
                if len(parsed_data) > 0:
                    first_record = parsed_data[0]
                    print(f"   📋 Exemplo de dados: {list(first_record.to_dict().keys())[:3]}...")
                
                results.append({
                    'file': test_file['path'],
                    'status': 'SUCCESS',
                    'records': len(parsed_data),
                    'format': format_info
                })
            else:
                print(f"   ❌ Parsing falhou - nenhum dado extraído")
                results.append({
                    'file': test_file['path'],
                    'status': 'ERROR',
                    'message': 'Parsing falhou'
                })
                
        except Exception as e:
            print(f"   ❌ Erro no processamento: {e}")
            results.append({
                'file': test_file['path'],
                'status': 'ERROR',
                'message': str(e)
            })
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    total_count = len(results)
    
    print(f"✅ Sucesso: {success_count}/{total_count}")
    print(f"❌ Falhas: {total_count - success_count}/{total_count}")
    
    for result in results:
        status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
        print(f"{status_icon} {result['file']}")
        if result['status'] == 'SUCCESS':
            print(f"   📊 {result['records']} registros | {result['format']}")
        else:
            print(f"   ⚠️ {result['message']}")
    
    # Salvar relatório
    report_path = Path(__file__).parent / "relatorio_compatibilidade.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO DE COMPATIBILIDADE - CONVERSOR TOTVS\n")
        f.write("=" * 50 + "\n\n")
        for result in results:
            f.write(f"Arquivo: {result['file']}\n")
            f.write(f"Status: {result['status']}\n")
            if result['status'] == 'SUCCESS':
                f.write(f"Registros: {result['records']}\n")
                f.write(f"Formato: {result['format']}\n")
            else:
                f.write(f"Erro: {result['message']}\n")
            f.write("-" * 30 + "\n")
    
    print(f"\n📄 Relatório salvo em: {report_path}")
    print(f"\n🎯 Teste concluído!")

if __name__ == "__main__":
    test_compatibility()
