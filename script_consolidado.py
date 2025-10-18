#!/usr/bin/env python3
"""
Script para Gerar Consolidado de Budget vs Actual
===============================================

Este script extrai dados dos sheets de budget e gera um consolidado
somando Budget e Actual de todas as unidades para cada linha,
calculando a diferença percentual do total.

Autor: Assistente IA
Data: 2025
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def extract_budget_data():
    """
    Extrai dados dos sheets de budget especificados
    """
    
    # Configuração dos sheets a serem processados
    sheets_config = {
        'BUDGET DISTRIB 2025': {
            'unit': 'DISTRIB',
            'description_col': 'Unnamed: 1'
        },
        'BUDGET PROJECTS 2025': {
            'unit': 'PROJECTS', 
            'description_col': 'Unnamed: 1'
        },
        'BUDGET DC 2025': {
            'unit': 'DC',
            'description_col': 'Unnamed: 1'
        },
        'BUDGET CHILE 2025': {
            'unit': 'CHILE',
            'description_col': 'Unnamed: 1',
            'use_predefined_descriptions': True
        }
    }
    
    # Descrições predefinidas para CHILE (limitadas conforme solicitado)
    chile_descriptions = [
        'REVENUES', 'REBATES', 'REBATES ANUAL',
        'SALES INCENTIVE', 'GROSS PROFIT',
        'GROSS PROFIT w/ rebates & incentives', 'COMISSIONS', 'SALES EXPENSES',
        'MARKETING EXPENSES', 'GENERAL AND ADMINISTRATION EXPENSES', 'SG&A',
        'FH', 'SG&A w/funded head', 'OH', 'TOTAL OPERATIONAL EBITDA'
    ]
    
    all_data = []
    
    print("🚀 Iniciando extração de dados de budget...")
    print("=" * 60)
    
    for sheet_name, config in sheets_config.items():
        print(f"\n📊 Processando {sheet_name}...")
        
        try:
            # Ler o sheet usando a linha 2 como cabeçalho
            df = pd.read_excel('Consolidado_Actual x Forecast_2025_Versao Final_Julho_Dinho.xlsx', 
                             sheet_name=sheet_name, header=2)
            
            # Identificar as colunas necessárias
            actual_col = None
            budget_col = None
            
            for col in df.columns:
                if 'Actual 2025' in str(col):
                    actual_col = col
                elif 'Budget 2025' in str(col):
                    budget_col = col
            
            if not all([actual_col, budget_col]):
                print(f"❌ Erro: Não foi possível identificar colunas necessárias em {sheet_name}")
                continue
            
            # Processar dados
            filtered_data = []
            
            for idx, row in df.iterrows():
                # Determinar descrição
                if config.get('use_predefined_descriptions', False):
                    if idx < len(chile_descriptions):
                        description = chile_descriptions[idx]
                    else:
                        # Não processar itens além da lista predefinida para CHILE
                        continue
                else:
                    description = str(row[config['description_col']]) if pd.notna(row[config['description_col']]) else ''
                
                actual_value = row[actual_col]
                budget_value = row[budget_col]
                
                # Critérios de filtragem
                is_valid = (
                    '%' not in description and
                    'ORDERS RECEIVED' not in description and  # Remover ORDERS RECEIVED de todas as unidades
                    pd.notna(actual_value) and pd.notna(budget_value) and
                    str(actual_value) not in ['MUSD', 'nan'] and
                    str(budget_value) not in ['MUSD', 'nan'] and
                    description.strip() != '' and description != 'nan'
                )
                
                if is_valid:
                    try:
                        # Converter para float
                        actual_float = float(actual_value)
                        budget_float = float(budget_value)
                        
                        filtered_data.append({
                            'Unidade': config['unit'],
                            'Descricao': description.strip(),
                            'Budget_2025': budget_float,
                            'Actual_2025': actual_float,
                            'Index': idx  # Para manter a ordem original
                        })
                        
                    except (ValueError, TypeError):
                        continue
            
            print(f"✅ Encontradas {len(filtered_data)} linhas válidas")
            all_data.extend(filtered_data)
            
        except Exception as e:
            print(f"❌ Erro ao processar {sheet_name}: {e}")
            continue
    
    return all_data

def create_consolidated_data(all_data):
    """
    Cria dados consolidados somando Budget e Actual por descrição
    """
    
    print("\n📊 Criando dados consolidados...")
    
    # Converter para DataFrame
    df = pd.DataFrame(all_data)
    
    # Agrupar por descrição e somar Budget e Actual
    consolidated = df.groupby('Descricao').agg({
        'Budget_2025': 'sum',
        'Actual_2025': 'sum'
    }).reset_index()
    
    # Calcular diferença e percentual
    consolidated['Diferenca'] = consolidated['Actual_2025'] - consolidated['Budget_2025']
    consolidated['Percentual_Diferenca'] = ((consolidated['Actual_2025'] / consolidated['Budget_2025']) - 1) * 100
    
    # Ordenar por Budget (maior para menor)
    consolidated = consolidated.sort_values('Budget_2025', ascending=False)
    
    # Adicionar coluna de status
    consolidated['Status'] = consolidated['Diferenca'].apply(
        lambda x: "Acima do Budget" if x >= 0 else "Abaixo do Budget"
    )
    
    return consolidated

def show_consolidated_summary(consolidated_df):
    """
    Mostra resumo consolidado dos dados
    """
    
    print(f"\n📊 RESUMO CONSOLIDADO - TODAS AS UNIDADES:")
    print("=" * 80)
    
    # Calcular totais
    total_budget = consolidated_df['Budget_2025'].sum()
    total_actual = consolidated_df['Actual_2025'].sum()
    total_difference = consolidated_df['Diferenca'].sum()
    total_percentage = ((total_actual / total_budget) - 1) * 100 if total_budget != 0 else 0
    
    print(f"\n💰 TOTAIS CONSOLIDADOS:")
    print(f"   Budget Total: ${total_budget:,.2f}M")
    print(f"   Actual Total: ${total_actual:,.2f}M")
    print(f"   Diferença Total: ${total_difference:+,.2f}M")
    print(f"   Diferença Percentual: {total_percentage:+.2f}%")
    
    print(f"\n📋 DETALHAMENTO POR LINHA:")
    print("-" * 80)
    print(f"{'Descrição':<40} {'Budget Total':<15} {'Actual Total':<15} {'Diferença %':<12}")
    print("-" * 80)
    
    for _, row in consolidated_df.iterrows():
        desc = row['Descricao'][:37] + "..." if len(row['Descricao']) > 40 else row['Descricao']
        budget = f"${row['Budget_2025']:,.2f}M"
        actual = f"${row['Actual_2025']:,.2f}M"
        pct = f"{row['Percentual_Diferenca']:+.1f}%"
        
        print(f"{desc:<40} {budget:<15} {actual:<15} {pct:<12}")
    
    return total_budget, total_actual, total_difference, total_percentage

def save_consolidated_data(consolidated_df):
    """
    Salva os dados consolidados em CSV
    """
    
    output_file = 'dados_consolidados_budget.csv'
    consolidated_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ Dados consolidados salvos em: {output_file}")
    
    return output_file

def create_consolidated_visualization(consolidated_df, total_budget, total_actual, total_percentage):
    """
    Cria visualização do consolidado
    """
    
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Configurar estilo
        plt.style.use('default')
        
        # Criar figura
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('📊 Consolidado Budget vs Actual - Todas as Unidades', 
                     fontsize=20, fontweight='bold')
        
        # 1. Gráfico de Barras - Top 15 Maiores Budgets
        top_15 = consolidated_df.head(15)
        
        bars = ax1.barh(range(len(top_15)), top_15['Budget_2025'], 
                       color='#3498DB', alpha=0.8)
        
        ax1.set_yticks(range(len(top_15)))
        ax1.set_yticklabels([desc[:25] + '...' if len(desc) > 25 else desc 
                            for desc in top_15['Descricao']], fontsize=9)
        ax1.set_xlabel('Budget Total (MUSD)', fontsize=12, fontweight='bold')
        ax1.set_title('💰 Top 15 Maiores Budgets', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')
        ax1.invert_yaxis()
        
        # Adicionar valores nas barras
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                    f'${width:.1f}M', ha='left', va='center', fontsize=8, fontweight='bold')
        
        # 2. Gráfico de Barras - Top 15 Maiores Actuals
        bars2 = ax2.barh(range(len(top_15)), top_15['Actual_2025'], 
                        color='#E67E22', alpha=0.8)
        
        ax2.set_yticks(range(len(top_15)))
        ax2.set_yticklabels([desc[:25] + '...' if len(desc) > 25 else desc 
                            for desc in top_15['Descricao']], fontsize=9)
        ax2.set_xlabel('Actual Total (MUSD)', fontsize=12, fontweight='bold')
        ax2.set_title('💵 Top 15 Maiores Actuals', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        ax2.invert_yaxis()
        
        # Adicionar valores nas barras
        for i, bar in enumerate(bars2):
            width = bar.get_width()
            ax2.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                    f'${width:.1f}M', ha='left', va='center', fontsize=8, fontweight='bold')
        
        # 3. Gráfico de Diferença Percentual
        # Filtrar para mostrar apenas os com maior variação (positiva e negativa)
        significant_changes = consolidated_df[
            (consolidated_df['Percentual_Diferenca'].abs() > 10) | 
            (consolidated_df['Budget_2025'] > 1)  # Incluir itens com budget > 1M
        ].head(15)
        
        colors = ['#2ECC71' if pct >= 0 else '#E74C3C' for pct in significant_changes['Percentual_Diferenca']]
        bars3 = ax3.barh(range(len(significant_changes)), significant_changes['Percentual_Diferenca'], 
                        color=colors, alpha=0.7)
        
        ax3.set_yticks(range(len(significant_changes)))
        ax3.set_yticklabels([desc[:25] + '...' if len(desc) > 25 else desc 
                            for desc in significant_changes['Descricao']], fontsize=9)
        ax3.set_xlabel('Diferença Percentual (%)', fontsize=12, fontweight='bold')
        ax3.set_title('📈 Diferença Percentual - Principais Itens', fontsize=14, fontweight='bold')
        ax3.axvline(x=0, color='black', linestyle='-', alpha=0.5)
        ax3.grid(True, alpha=0.3, axis='x')
        ax3.invert_yaxis()
        
        # Adicionar valores nas barras
        for i, (bar, pct) in enumerate(zip(bars3, significant_changes['Percentual_Diferenca'])):
            width = bar.get_width()
            ax3.text(width + (1 if width >= 0 else -1), bar.get_y() + bar.get_height()/2,
                    f'{pct:+.1f}%', ha='left' if width >= 0 else 'right', 
                    va='center', fontsize=8, fontweight='bold')
        
        # 4. Resumo Executivo
        ax4.axis('off')
        
        # Criar tabela de resumo
        summary_data = [
            ['Budget Total', f'${total_budget:,.2f}M'],
            ['Actual Total', f'${total_actual:,.2f}M'],
            ['Diferença Total', f'${total_actual - total_budget:+,.2f}M'],
            ['Diferença Percentual', f'{total_percentage:+.2f}%'],
            ['Total de Itens', f'{len(consolidated_df)}'],
            ['Status Geral', 'Acima do Budget' if total_percentage >= 0 else 'Abaixo do Budget']
        ]
        
        table = ax4.table(cellText=summary_data,
                         colLabels=['Métrica', 'Valor'],
                         cellLoc='center',
                         loc='center',
                         colWidths=[0.4, 0.4])
        
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 2)
        
        # Colorir células baseado no status
        for i in range(1, len(summary_data) + 1):
            if i == 6:  # Status Geral
                status_cell = table[(i, 1)]
                if 'Acima' in status_cell.get_text().get_text():
                    status_cell.set_facecolor('#D5F4E6')
                else:
                    status_cell.set_facecolor('#FADBD8')
        
        ax4.set_title('📋 Resumo Executivo', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.93)
        
        # Salvar gráfico
        plt.savefig('consolidado_budget_vs_actual.png', dpi=300, bbox_inches='tight')
        print("✅ Gráfico consolidado salvo como: consolidado_budget_vs_actual.png")
        
        plt.show()
        
    except ImportError:
        print("⚠️ Matplotlib não disponível. Gráfico não foi gerado.")

def main():
    """
    Função principal do script
    """
    
    print("🎯 Script Consolidado - Budget vs Actual Todas as Unidades")
    print("=" * 70)
    
    # Extrair dados
    all_data = extract_budget_data()
    
    if all_data:
        # Criar dados consolidados
        consolidated_df = create_consolidated_data(all_data)
        
        # Mostrar resumo
        total_budget, total_actual, total_difference, total_percentage = show_consolidated_summary(consolidated_df)
        
        # Salvar dados
        output_file = save_consolidated_data(consolidated_df)
        
        # Criar visualização
        create_consolidated_visualization(consolidated_df, total_budget, total_actual, total_percentage)
        
        print("\n" + "=" * 70)
        print("✅ PROCESSAMENTO CONSOLIDADO CONCLUÍDO!")
        print("=" * 70)
        
        print(f"\n📁 Arquivos gerados:")
        print(f"   🎯 {output_file} (dados consolidados)")
        print(f"   📊 consolidado_budget_vs_actual.png (visualização)")
        
        print(f"\n🎯 Principais Insights:")
        print(f"   💰 Budget Total Consolidado: ${total_budget:,.2f}M")
        print(f"   💵 Actual Total Consolidado: ${total_actual:,.2f}M")
        print(f"   📊 Diferença Percentual: {total_percentage:+.2f}%")
        print(f"   📋 Total de Itens Analisados: {len(consolidated_df)}")
        
    else:
        print("❌ Nenhum dado foi extraído!")

if __name__ == "__main__":
    main()
