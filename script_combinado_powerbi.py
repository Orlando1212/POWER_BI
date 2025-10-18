#!/usr/bin/env python3
"""
Script Combinado para Power BI - Geração de Scripts Python Individuais
=====================================================================

Este script combina os dados dos dois CSVs e gera scripts Python individuais
para cada gráfico que podem ser importados diretamente no Power BI.

Autor: Assistente IA
Data: 2025
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

def load_and_combine_data(excel_file):
    """
    Executa o script final que lê o Excel e gera os dados combinados
    """
    
    print(f"📊 Executando script final para processar dados do Excel: {excel_file}")
    
    # Executar script final usando subprocess com o arquivo Excel como parâmetro
    print("\n🚀 Executando script final_powerbi_script.py...")
    import subprocess
    result_final = subprocess.run(['python', 'final_powerbi_script.py', excel_file], 
                                 capture_output=True, text=True)
    if result_final.returncode != 0:
        print(f"❌ Erro ao executar final_powerbi_script.py: {result_fi.stderr}")
        return None
    else:
        print("✅ Script final executado com sucesso!")
    
    print("\n📊 Carregando dados combinados...")
    
    # Verificar se o arquivo foi criado
    if not os.path.exists('budget_data_for_powerbi.csv'):
        print("❌ Arquivo budget_data_for_powerbi.csv não foi criado!")
        return None
    
    # Carregar dados combinados (já contém dados por unidade + consolidados)
    combined_df = pd.read_csv('budget_data_for_powerbi.csv')
    
    print(f"✅ Dados carregados do arquivo: budget_data_for_powerbi.csv")
    print(f"📊 Total de registros: {len(combined_df)}")
    
    return combined_df

def create_python_script_template():
    """
    Cria template base para scripts Python do Power BI
    """
    
    return '''
# Script Python para Power BI
# Gerado automaticamente pelo script_combinado_powerbi.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configurar estilo
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# Carregar dados (Power BI irá substituir por 'dataset')
df = dataset.copy()

# Configurações do gráfico
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('white')

'''

def generate_script_1_budget_vs_actual_por_unidade():
    """
    Gera script para gráfico Budget vs Actual por Unidade COM FILTROS INTERATIVOS
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Gráfico: Budget vs Actual por Unidade - COM FILTROS INTERATIVOS
# ===============================================================

# Aplicar filtros do Power BI automaticamente (df já vem filtrado)
# O Power BI aplica os filtros automaticamente no dataset

# Filtrar apenas dados por unidade (não consolidado)
df_unidades = df[df['Tipo_Analise'] == 'Por Unidade'].copy()

# Verificar se há dados após filtro
if df_unidades.empty:
    ax.text(0.5, 0.5, 'Nenhum dado encontrado\\ncom os filtros aplicados', 
            ha='center', va='center', transform=ax.transAxes, 
            fontsize=16, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral", alpha=0.7))
    ax.set_title('📊 Budget vs Actual por Unidade - SEM DADOS', fontsize=16, fontweight='bold')
else:
    # Agrupar por unidade
    summary = df_unidades.groupby('Unidade').agg({
        'Budget_2025': 'sum',
        'Actual_2025': 'sum'
    }).reset_index()
    
    # Criar gráfico de barras agrupadas
    x = np.arange(len(summary))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, summary['Budget_2025'], width, 
                  label='Budget 2025', color='#3498DB', alpha=0.8)
    bars2 = ax.bar(x + width/2, summary['Actual_2025'], width,
                  label='Actual 2025', color='#E67E22', alpha=0.8)
    
    # Configurar eixos
    ax.set_xlabel('Unidade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valor (MUSD)', fontsize=12, fontweight='bold')
    ax.set_title('📊 Budget vs Actual por Unidade - FILTRADO', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(summary['Unidade'])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Adicionar valores nas barras
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'${height:.1f}M', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'${height:.1f}M', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
'''
    
    # Salvar script
    with open('script_1_budget_vs_actual_por_unidade.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script 1 gerado: script_1_budget_vs_actual_por_unidade.py")

def generate_script_2_performance_por_unidade():
    """
    Gera script para gráfico Performance por Unidade COM FILTROS INTERATIVOS
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Gráfico: Performance por Unidade - COM FILTROS INTERATIVOS
# ==========================================================

# Aplicar filtros do Power BI automaticamente (df já vem filtrado)
# O Power BI aplica os filtros automaticamente no dataset

# Filtrar apenas dados por unidade (não consolidado)
df_unidades = df[df['Tipo_Analise'] == 'Por Unidade'].copy()

# Verificar se há dados após filtro
if df_unidades.empty:
    ax.text(0.5, 0.5, 'Nenhum dado encontrado\\ncom os filtros aplicados', 
            ha='center', va='center', transform=ax.transAxes, 
            fontsize=16, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral", alpha=0.7))
    ax.set_title('📈 Performance por Unidade - SEM DADOS', fontsize=16, fontweight='bold')
else:
    # Agrupar por unidade e calcular performance média
    summary = df_unidades.groupby('Unidade').agg({
        'Budget_2025': 'sum',
        'Actual_2025': 'sum',
        'Percentual_Diferenca': 'mean'
    }).reset_index()
    
    # Configurar cores baseadas na performance
    colors_resumo = ['#2ECC71' if pct >= 0 else '#E74C3C' for pct in summary['Percentual_Diferenca']]
    
    # Criar gráfico de barras
    bars = ax.bar(summary['Unidade'], summary['Percentual_Diferenca'], 
                  color=colors_resumo, alpha=0.7)
    
    # Configurar eixos
    ax.set_xlabel('Unidade', fontsize=12, fontweight='bold')
    ax.set_ylabel('Performance Média (%)', fontsize=12, fontweight='bold')
    ax.set_title('📈 Performance por Unidade - FILTRADO', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    
    # Adicionar valores nas barras
    for bar, pct in zip(bars, summary['Percentual_Diferenca']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height >= 0 else -1.5),
                f'{pct:+.1f}%', ha='center', va='bottom' if height >= 0 else 'top', 
                fontsize=10, fontweight='bold')

plt.tight_layout()
'''
    
    # Salvar script
    with open('script_2_performance_por_unidade.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script 2 gerado: script_2_performance_por_unidade.py")

def generate_script_3_consolidado_budget_vs_actual():
    """
    Gera script para gráfico Consolidado Budget vs Actual COM FILTROS INTERATIVOS
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Gráfico: Consolidado Budget vs Actual - COM FILTROS INTERATIVOS
# ==============================================================

# Aplicar filtros do Power BI automaticamente (df já vem filtrado)
# O Power BI aplica os filtros automaticamente no dataset

# Filtrar apenas dados consolidados
df_consolidado = df[df['Tipo_Analise'] == 'Consolidado'].copy()

# Verificar se há dados após filtro
if df_consolidado.empty:
    ax.text(0.5, 0.5, 'Nenhum dado consolidado\\nencontrado com os filtros aplicados', 
            ha='center', va='center', transform=ax.transAxes, 
            fontsize=16, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral", alpha=0.7))
    ax.set_title('💰 Top Budgets Consolidados - SEM DADOS', fontsize=16, fontweight='bold')
else:
    # Pegar os top 10 maiores budgets
    top_10 = df_consolidado.nlargest(10, 'Budget_2025')
    
    # Criar gráfico de barras horizontais
    bars = ax.barh(range(len(top_10)), top_10['Budget_2025'], 
                   color='#3498DB', alpha=0.8)
    
    # Configurar eixos
    ax.set_yticks(range(len(top_10)))
    ax.set_yticklabels([desc[:25] + '...' if len(desc) > 25 else desc 
                       for desc in top_10['Descricao']], fontsize=10)
    ax.set_xlabel('Budget Total (MUSD)', fontsize=12, fontweight='bold')
    ax.set_title('💰 Top 10 Budgets Consolidados - FILTRADO', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                f'${width:.1f}M', ha='left', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
'''
    
    # Salvar script
    with open('script_3_consolidado_budget_vs_actual.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script 3 gerado: script_3_consolidado_budget_vs_actual.py")

def generate_script_4_consolidado_performance():
    """
    Gera script para gráfico Performance Consolidado COM FILTROS INTERATIVOS
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Gráfico: Performance Consolidado - COM FILTROS INTERATIVOS
# =========================================================

# Aplicar filtros do Power BI automaticamente (df já vem filtrado)
# O Power BI aplica os filtros automaticamente no dataset

# Filtrar apenas dados consolidados
df_consolidado = df[df['Tipo_Analise'] == 'Consolidado'].copy()

# Verificar se há dados após filtro
if df_consolidado.empty:
    ax.text(0.5, 0.5, 'Nenhum dado consolidado\\nencontrado com os filtros aplicados', 
            ha='center', va='center', transform=ax.transAxes, 
            fontsize=16, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral", alpha=0.7))
    ax.set_title('📈 Performance Consolidado - SEM DADOS', fontsize=16, fontweight='bold')
else:
    # Filtrar itens com maior variação
    significant_changes = df_consolidado[
        (df_consolidado['Percentual_Diferenca'].abs() > 50) | 
        (df_consolidado['Budget_2025'] > 5)  # Incluir itens com budget > 5M
    ].head(10)
    
    if significant_changes.empty:
        ax.text(0.5, 0.5, 'Nenhum item significativo\\nencontrado com os filtros aplicados', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.7))
        ax.set_title('📈 Performance Consolidado - SEM DADOS SIGNIFICATIVOS', fontsize=16, fontweight='bold')
    else:
        # Configurar cores baseadas na performance
        colors = ['#2ECC71' if pct >= 0 else '#E74C3C' for pct in significant_changes['Percentual_Diferenca']]
        
        # Criar gráfico de barras horizontais
        bars = ax.barh(range(len(significant_changes)), significant_changes['Percentual_Diferenca'], 
                       color=colors, alpha=0.7)
        
        # Configurar eixos
        ax.set_yticks(range(len(significant_changes)))
        ax.set_yticklabels([desc[:25] + '...' if len(desc) > 25 else desc 
                           for desc in significant_changes['Descricao']], fontsize=10)
        ax.set_xlabel('Diferença Percentual (%)', fontsize=12, fontweight='bold')
        ax.set_title('📈 Performance Consolidado - FILTRADO', fontsize=16, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
        ax.grid(True, alpha=0.3, axis='x')
        ax.invert_yaxis()
        
        # Adicionar valores nas barras
        for i, (bar, pct) in enumerate(zip(bars, significant_changes['Percentual_Diferenca'])):
            width = bar.get_width()
            ax.text(width + (1 if width >= 0 else -1), bar.get_y() + bar.get_height()/2,
                    f'{pct:+.1f}%', ha='left' if width >= 0 else 'right', 
                    va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
'''
    
    # Salvar script
    with open('script_4_consolidado_performance.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script 4 gerado: script_4_consolidado_performance.py")

def generate_script_5_dashboard_completo():
    """
    Gera script para dashboard completo COM FILTROS INTERATIVOS
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Dashboard Completo - Budget vs Actual - COM FILTROS INTERATIVOS
# ==============================================================

# Aplicar filtros do Power BI automaticamente (df já vem filtrado)
# O Power BI aplica os filtros automaticamente no dataset

# Criar figura com múltiplos subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('📊 Dashboard Completo - Budget vs Actual 2025 - FILTRADO', fontsize=18, fontweight='bold')

# Filtrar dados por tipo de análise
df_unidades = df[df['Tipo_Analise'] == 'Por Unidade'].copy()
df_consolidado = df[df['Tipo_Analise'] == 'Consolidado'].copy()

# Verificar se há dados
if df_unidades.empty and df_consolidado.empty:
    # Mostrar mensagem de erro em todos os subplots
    for ax in [ax1, ax2, ax3, ax4]:
        ax.text(0.5, 0.5, 'Nenhum dado encontrado\\ncom os filtros aplicados', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=14, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral", alpha=0.7))
        ax.set_title('SEM DADOS', fontsize=12, fontweight='bold')
else:
    # 1. Budget vs Actual por Unidade
    if not df_unidades.empty:
        summary = df_unidades.groupby('Unidade').agg({
            'Budget_2025': 'sum',
            'Actual_2025': 'sum'
        }).reset_index()
        
        x = np.arange(len(summary))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, summary['Budget_2025'], width, 
                       label='Budget 2025', color='#3498DB', alpha=0.8)
        bars2 = ax1.bar(x + width/2, summary['Actual_2025'], width,
                       label='Actual 2025', color='#E67E22', alpha=0.8)
        
        ax1.set_xlabel('Unidade', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Valor (MUSD)', fontsize=10, fontweight='bold')
        ax1.set_title('💰 Budget vs Actual por Unidade', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(summary['Unidade'])
        ax1.legend()
        ax1.grid(True, alpha=0.3)
    else:
        ax1.text(0.5, 0.5, 'Nenhum dado\\nde unidade encontrado', 
                ha='center', va='center', transform=ax1.transAxes, fontsize=12)
        ax1.set_title('💰 Budget vs Actual por Unidade - SEM DADOS', fontsize=12, fontweight='bold')
    
    # 2. Performance por Unidade
    if not df_unidades.empty:
        performance = df_unidades.groupby('Unidade')['Percentual_Diferenca'].mean()
        colors_perf = ['#2ECC71' if pct >= 0 else '#E74C3C' for pct in performance.values]
        
        bars_perf = ax2.bar(performance.index, performance.values, color=colors_perf, alpha=0.7)
        ax2.set_xlabel('Unidade', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Performance (%)', fontsize=10, fontweight='bold')
        ax2.set_title('📈 Performance por Unidade', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    else:
        ax2.text(0.5, 0.5, 'Nenhum dado\\nde unidade encontrado', 
                ha='center', va='center', transform=ax2.transAxes, fontsize=12)
        ax2.set_title('📈 Performance por Unidade - SEM DADOS', fontsize=12, fontweight='bold')
    
    # 3. Top Budgets Consolidados
    if not df_consolidado.empty:
        top_5 = df_consolidado.nlargest(5, 'Budget_2025')
        
        bars3 = ax3.barh(range(len(top_5)), top_5['Budget_2025'], color='#9B59B6', alpha=0.8)
        ax3.set_yticks(range(len(top_5)))
        ax3.set_yticklabels([desc[:20] + '...' if len(desc) > 20 else desc 
                            for desc in top_5['Descricao']], fontsize=9)
        ax3.set_xlabel('Budget (MUSD)', fontsize=10, fontweight='bold')
        ax3.set_title('🏆 Top 5 Budgets Consolidados', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')
        ax3.invert_yaxis()
    else:
        ax3.text(0.5, 0.5, 'Nenhum dado\\nconsolidado encontrado', 
                ha='center', va='center', transform=ax3.transAxes, fontsize=12)
        ax3.set_title('🏆 Top 5 Budgets Consolidados - SEM DADOS', fontsize=12, fontweight='bold')
    
    # 4. Resumo Executivo
    ax4.axis('off')
    
    if not df_consolidado.empty and not df_unidades.empty:
        # Calcular totais
        total_budget = df_consolidado['Budget_2025'].sum()
        total_actual = df_consolidado['Actual_2025'].sum()
        total_percentage = ((total_actual / total_budget) - 1) * 100 if total_budget != 0 else 0
        
        summary_data = [
            ['Budget Total', f'${total_budget:,.1f}M'],
            ['Actual Total', f'${total_actual:,.1f}M'],
            ['Diferença', f'{total_percentage:+.1f}%'],
            ['Unidades', f'{len(df_unidades["Unidade"].unique())}'],
            ['Itens', f'{len(df_consolidado)}']
        ]
        
        table = ax4.table(cellText=summary_data,
                         colLabels=['Métrica', 'Valor'],
                         cellLoc='center',
                         loc='center',
                         colWidths=[0.4, 0.4])
        
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1, 1.5)
        
        ax4.set_title('📋 Resumo Executivo - FILTRADO', fontsize=12, fontweight='bold', pad=20)
    else:
        ax4.text(0.5, 0.5, 'Dados insuficientes\\npara resumo', 
                ha='center', va='center', transform=ax4.transAxes, fontsize=12)
        ax4.set_title('📋 Resumo Executivo - SEM DADOS', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
'''
    
    # Salvar script
    with open('script_5_dashboard_completo.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script 5 gerado: script_5_dashboard_completo.py")

def generate_script_6_menu_interativo():
    """
    Gera script para menu interativo com filtros no Power BI
    """
    
    script_content = '''
# Script Python para Power BI - Menu Interativo com Filtros
# Gerado automaticamente pelo script_combinado_powerbi.py
# =========================================================

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configurar Convite
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

# Carregar dados (Power BI irá substituir por 'dataset')
df = dataset.copy()

# =========================================================
# CONFIGURAÇÃO DO MENU INTERATIVO
# =========================================================

# Definir opções do menu (baseado nos dados disponíveis)
def get_menu_options():
    """
    Retorna as opções disponíveis para o menu
    """
    
    # Unidades disponíveis
    unidades = df[df['Tipo_Analise'] == 'Por Unidade']['Unidade'].unique()
    
    # Linhas consolidadas disponíveis
    linhas_consolidadas = df[df['Tipo_Analise'] == 'Consolidado']['Descricao'].unique()
    
    return {
        'unidades': sorted(unidades),
        'linhas_consolidadas': sorted(linhas_consolidadas)
    }

# =========================================================
# FUNÇÃO PRINCIPAL - MENU INTERATIVO
# =========================================================

def create_interactive_menu():
    """
    Cria menu interativo baseado nos filtros do Power BI
    """
    
    # Configurar figura com 3 subplots (menu + 2 gráficos)
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('🎯 Menu Interativo - Análise Budget vs Actual', 
                 fontsize=20, fontweight='bold')
    
    # Criar layout com gridspec para melhor controle
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 3], width_ratios=[1, 1, 1])
    
    # 1. Menu de Opções (topo, ocupando toda a largura)
    ax_menu = fig.add_subplot(gs[0, :])
    ax_menu.axis('off')
    
    # Obter opções do menu
    menu_options = get_menu_options()
    
    # Criar texto do menu
    menu_text = "🎯 MENU INTERATIVO - Selecione uma opção nos filtros do Power BI:\\n\\n"
    menu_text += "📊 ANÁLISE POR UNIDADE:\\n"
    for i, unidade in enumerate(menu_options['unidades'], 1):
        menu_text += f"   {i}. {unidade}\\n"
    
    menu_text += "\\n📈 ANÁLISE CONSOLIDADA:\\n"
    for i, linha in enumerate(menu_options['linhas_consolidadas'][:10], 1):  # Top 10
        menu_text += f"   {i}. {linha}\\n"
    if len(menu_options['linhas_consolidadas']) > 10:
        menu_text += f"   ... e mais {len(menu_options['linhas_consolidadas'])-10} opções\\n"
    
    menu_text += "\\n💡 INSTRUÇÕES:\\n"
    menu_text += "   1. Use os filtros do Power BI para selecionar Unidade e/ou Descrição\\n"
    menu_text += "   2. O gráfico se atualizará automaticamente\\n"
    menu_text += "   3. Para análise consolidada, filtre apenas por Descrição\\n"
    menu_text += "   4. Para análise por unidade, filtre por Unidade + Descrição"
    
    ax_menu.text(0.02, 0.98, menu_text, transform=ax_menu.transAxes, 
                fontsize=12, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    # 2. Gráfico Principal (esquerda)
    ax_main = fig.add_subplot(gs[1, 0])
    
    # 3. Gráfico de Performance (direita)
    ax_perf = fig.add_subplot(gs[1, 1])
    
    # 4. Informações Adicionais (centro)
    ax_info = fig.add_subplot(gs[1, 2])
    ax_info.axis('off')
    
    # =========================================================
    # DETERMINAR TIPO DE ANÁLISE BASEADO NOS FILTROS
    # =========================================================
    
    # Verificar se há filtros aplicados
    df_filtered = df.copy()
    
    # Determinar tipo de análise
    has_unidade_filter = len(df_filtered['Unidade'].unique()) < len(df['Unidade'].unique())
    has_descricao_filter = len(df_filtered['Descricao'].unique()) < len(df['Descricao'].unique())
    
    if has_unidade_filter and has_descricao_filter:
        # Análise específica por unidade + linha
        analysis_type = "ESPECÍFICA"
        selected_unidade = df_filtered['Unidade'].iloc[0]
        selected_descricao = df_filtered['Descricao'].iloc[0]
        
        # Filtrar dados específicos
        df_analysis = df_filtered[
            (df_filtered['Tipo_Analise'] == 'Por Unidade') & 
            (df_filtered['Unidade'] == selected_unidade) & 
            (df_filtered['Descricao'] == selected_descricao)
        ]
        
        if not df_analysis.empty:
            row = df_analysis.iloc[0]
            budget = row['Budget_2025']
            actual = row['Actual_2025']
            percentage = row['Percentual_Diferenca']
            
            # Gráfico Principal - Budget vs Actual
            categories = ['Budget 2025', 'Actual 2025']
            values = [budget, actual]
            colors = ['#3498DB', '#E67E22']
            
            bars = ax_main.bar(categories, values, color=colors, alpha=0.8)
            ax_main.set_ylabel('Valor (MUSD)', fontsize=12, fontweight='bold')
            ax_main.set_title(f'💰 {selected_unidade} - {selected_descricao}', 
                            fontsize=14, fontweight='bold')
            ax_main.grid(True, alpha=0.3, axis='y')
            
            # Adicionar valores nas barras
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax_main.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                           f'${value:.2f}M', ha='center', va='bottom', 
                           fontsize=12, fontweight='bold')
            
            # Gráfico de Performance
            color = '#2ECC71' if percentage >= 0 else '#E74C3C'
            bar_perf = ax_perf.bar(['Performance'], [percentage], color=color, alpha=0.8)
            ax_perf.set_ylabel('Diferença Percentual (%)', fontsize=12, fontweight='bold')
            ax_perf.set_title('📈 Performance', fontsize=14, fontweight='bold')
            ax_perf.grid(True, alpha=0.3, axis='y')
            ax_perf.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=2)
            
            # Adicionar valor na barra
            ax_perf.text(0, percentage + (2 if percentage >= 0 else -2),
                        f'{percentage:+.1f}%', ha='center', 
                        va='bottom' if percentage >= 0 else 'top',
                        fontsize=14, fontweight='bold')
            
            # Informações
            difference = actual - budget
            status = "Acima do Budget" if difference >= 0 else "Abaixo do Budget"
            
            info_text = f"📊 ANÁLISE ESPECÍFICA\\n\\n"
            info_text += f"🏢 Unidade: {selected_unidade}\\n"
            info_text += f"📋 Linha: {selected_descricao}\\n\\n"
            info_text += f"💰 Budget: ${budget:.2f}M\\n"
            info_text += f"💵 Actual: ${actual:.2f}M\\n"
            info_text += f"📈 Diferença: {percentage:+.1f}%\\n"
            info_text += f"📋 Status: {status}"
            
            ax_info.text(0.05, 0.95, info_text, transform=ax_info.transAxes, 
                        fontsize=12, verticalalignment='top',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8))
    
    elif has_descricao_filter and not has_unidade_filter:
        # Análise consolidada por linha
        analysis_type = "CONSOLIDADA"
        selected_descricao = df_filtered['Descricao'].iloc[0]
        
        # Filtrar dados consolidados
        df_analysis = df_filtered[
            (df_filtered['Tipo_Analise'] == 'Consolidado') & 
            (df_filtered['Descricao'] == selected_descricao)
        ]
        
        if not df_analysis.empty:
            row = df_analysis.iloc[0]
            budget = row['Budget_2025']
            actual = row['Actual_2025']
            percentage = row['Percentual_Diferenca']
            
            # Gráfico Principal - Budget vs Actual Consolidado
            categories = ['Budget Total', 'Actual Total']
            values = [budget, actual]
            colors = ['#9B59B6', '#F39C12']
            
            bars = ax_main.bar(categories, values, color=colors, alpha=0.8)
            ax_main.set_ylabel('Valor (MUSD)', fontsize=12, fontweight='bold')
            ax_main.set_title(f'💰 Consolidado - {selected_descricao}', 
                            fontsize=14, fontweight='bold')
            ax_main.grid(True, alpha=0.3, axis='y')
            
            # Adicionar valores nas barras
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax_main.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                           f'${value:.2f}M', ha='center', va='bottom', 
                           fontsize=12, fontweight='bold')
            
            # Gráfico de Performance
            color = '#2ECC71' if percentage >= 0 else '#E74C3C'
            bar_perf = ax_perf.bar(['Performance'], [percentage], color=color, alpha=0.8)
            ax_perf.set_ylabel('Diferença Percentual (%)', fontsize=12, fontweight='bold')
            ax_perf.set_title('📈 Performance Consolidada', fontsize=14, fontweight='bold')
            ax_perf.grid(True, alpha=0.3, axis='y')
            ax_perf.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=2)
            
            # Adicionar valor na barra
            ax_perf.text(0, percentage + (2 if percentage >= 0 else -2),
                        f'{percentage:+.1f}%', ha='center', 
                        va='bottom' if percentage >= 0 else 'top',
                        fontsize=14, fontweight='bold')
            
            # Informações
            difference = actual - budget
            status = "Acima do Budget" if difference >= 0 else "Abaixo do Budget"
            
            info_text = f"📊 ANÁLISE CONSOLIDADA\\n\\n"
            info_text += f"📋 Linha: {selected_descricao}\\n"
            info_text += f"🏢 Todas as Unidades\\n\\n"
            info_text += f"💰 Budget Total: ${budget:.2f}M\\n"
            info_text += f"💵 Actual Total: ${actual:.2f}M\\n"
            info_text += f"📈 Diferença: {percentage:+.1f}%\\n"
            info_text += f"📋 Status: {status}"
            
            ax_info.text(0.05, 0.95, info_text, transform=ax_info.transAxes, 
                        fontsize=12, verticalalignment='top',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    else:
        # Nenhum filtro específico - mostrar resumo geral
        analysis_type = "GERAL"
        
        # Gráfico Principal - Resumo por Unidade
        df_unidades = df[df['Tipo_Analise'] == 'Por Unidade'].copy()
        summary = df_unidades.groupby('Unidade').agg({
            'Budget_2025': 'sum',
            'Actual_2025': 'sum'
        }).reset_index()
        
        x = np.arange(len(summary))
        width = 0.35
        
        bars1 = ax_main.bar(x - width/2, summary['Budget_2025'], width, 
                           label='Budget 2025', color='#3498DB', alpha=0.8)
        bars2 = ax_main.bar(x + width/2, summary['Actual_2025'], width,
                           label='Actual 2025', color='#E67E22', alpha=0.8)
        
        ax_main.set_xlabel('Unidade', fontsize=12, fontweight='bold')
        ax_main.set_ylabel('Valor (MUSD)', fontsize=12, fontweight='bold')
        ax_main.set_title('💰 Budget vs Actual por Unidade', fontsize=14, fontweight='bold')
        ax_main.set_xticks(x)
        ax_main.set_xticklabels(summary['Unidade'])
        ax_main.legend()
        ax_main.grid(True, alpha=0.3)
        
        # Gráfico de Performance
        performance = df_unidades.groupby('Unidade')['Percentual_Diferenca'].mean()
        colors_perf = ['#2ECC71' if pct >= 0 else '#E74C3C' for pct in performance.values]
        
        bars_perf = ax_perf.bar(performance.index, performance.values, color=colors_perf, alpha=0.7)
        ax_perf.set_xlabel('Unidade', fontsize=12, fontweight='bold')
        ax_perf.set_ylabel('Performance (%)', fontsize=12, fontweight='bold')
        ax_perf.set_title('📈 Performance por Unidade', fontsize=14, fontweight='bold')
        ax_perf.grid(True, alpha=0.3)
        ax_perf.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # Informações Gerais
        df_consolidado = df[df['Tipo_Analise'] == 'Consolidado'].copy()
        total_budget = df_consolidado['Budget_2025'].sum()
        total_actual = df_consolidado['Actual_2025'].sum()
        total_percentage = ((total_actual / total_budget) - 1) * 100 if total_budget != 0 else 0
        
        info_text = f"📊 VISÃO GERAL\\n\\n"
        info_text += f"🏢 Unidades: {len(summary)}\\n"
        info_text += f"📋 Linhas: {len(df_consolidado)}\\n\\n"
        info_text += f"💰 Budget Total: ${total_budget:.1f}M\\n"
        info_text += f"💵 Actual Total: ${total_actual:.1f}M\\n"
        info_text += f"📈 Diferença: {total_percentage:+.1f}%\\n\\n"
        info_text += f"💡 Use os filtros para análise específica"
        
        ax_info.text(0.05, 0.95, info_text, transform=ax_info.transAxes, 
                    fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    plt.tight_layout()

# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

# Executar o menu interativo
create_interactive_menu()
'''
    
    # Salvar script
    with open('script_6_menu_interativo.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script 6 gerado: script_6_menu_interativo.py")

def generate_instructions():
    """
    Gera instruções de uso dos scripts
    """
    
    instructions = '''
# 📊 Guia para Usar Scripts Python no Power BI
=============================================

## 🚀 Como Importar os Scripts no Power BI

### 1. Preparação dos Dados
1. Abra o Power BI Desktop
2. Vá em "Obter Dados" > "Texto/CSV"
3. Importe o arquivo: dados_combinados_powerbi.csv
4. Clique em "Carregar"

### 2. Criar Visualizações com Scripts Python

#### Método 1: Visual Python
1. No painel "Visualizações", clique no ícone Python (🐍)
2. Selecione as colunas necessárias:
   - Unidade, Budget_2025, Actual_2025, Percentual_Diferenca, Tipo_Analise
3. Copie e cole o código do script desejado
4. Clique em "Executar"

#### Método 2: R Script (Alternativo)
1. No painel "Visualizações", clique no ícone R (📊)
2. Siga os mesmos passos do Python

### 3. Scripts Disponíveis

#### 📊 Script 1: Budget vs Actual por Unidade
- Arquivo: script_1_budget_vs_actual_por_unidade.py
- Mostra: Comparação Budget vs Actual para cada unidade
- Uso: Análise por unidade individual

#### 📈 Script 2: Performance por Unidade  
- Arquivo: script_2_performance_por_unidade.py
- Mostra: Performance média de cada unidade
- Uso: Identificar unidades com melhor/pior performance

#### 💰 Script 3: Consolidado Budget vs Actual
- Arquivo: script_3_consolidado_budget_vs_actual.py
- Mostra: Top 10 maiores budgets consolidados
- Uso: Visão consolidada dos maiores orçamentos

#### 📊 Script 4: Performance Consolidado
- Arquivo: script_4_consolidado_performance.py
- Mostra: Performance dos principais itens consolidados
- Uso: Identificar itens com maior variação

#### 🎯 Script 5: Dashboard Completo
- Arquivo: script_5_dashboard_completo.py
- Mostra: Dashboard com 4 visualizações em uma
- Uso: Visão geral completa

#### 🎯 Script 6: Menu Interativo com Filtros (NOVO!)
- Arquivo: script_6_menu_interativo.py
- Mostra: Menu interativo que se adapta aos filtros do Power BI
- Uso: Análise dinâmica com filtros automáticos
- Funcionalidades:
  * Detecta filtros aplicados automaticamente
  * Mostra análise específica por unidade + linha
  * Mostra análise consolidada por linha
  * Mostra visão geral quando nenhum filtro está aplicado
  * Budget vs Actual + Diferença Percentual em tempo real

### 4. Dicas de Uso

#### Configurações Recomendadas:
- Tamanho do visual: 800x600 pixels
- Formato: PNG ou SVG
- Resolução: 300 DPI

#### Filtros Interativos:
- **Scripts 1-5**: Todos os scripts agora suportam filtros automáticos do Power BI
- **Script 6**: Menu interativo que detecta filtros e adapta a visualização automaticamente
- **Filtros por Unidade**: Selecione uma ou mais unidades nos filtros do Power BI
- **Filtros por Linha**: Selecione uma ou mais linhas (Descrição) nos filtros do Power BI
- **Análise Combinada**: Combine filtros de Unidade + Linha para análise específica
- **Análise Consolidada**: Use apenas filtro de Linha para ver dados consolidados
- **Atualização Automática**: Todos os gráficos se atualizam automaticamente quando você muda os filtros

#### Customização:
- Modifique cores alterando os códigos hex (#3498DB, #E67E22, etc.)
- Ajuste tamanhos alterando figsize=(12, 8)
- Personalize títulos e labels conforme necessário

### 5. Solução de Problemas

#### Erro: "Python não encontrado"
1. Instale Python 3.7+ no seu computador
2. Instale as bibliotecas: matplotlib, pandas, numpy
3. Configure o caminho do Python no Power BI

#### Erro: "Biblioteca não encontrada"
```bash
pip install matplotlib pandas numpy
```

#### Erro: "Dados não carregados"
1. Verifique se o arquivo CSV está correto
2. Confirme se as colunas estão com os nomes corretos
3. Teste com dados de exemplo primeiro

### 6. Estrutura dos Dados

O arquivo dados_combinados_powerbi.csv contém:
- Dados por unidade (CHILE, DC, DISTRIB, PROJECTS)
- Dados consolidados (soma de todas as unidades)
- Colunas: Unidade, Descricao, Budget_2025, Actual_2025, Percentual_Diferenca, Status, Tipo_Analise

### 7. Próximos Passos

1. ✅ Importe o CSV no Power BI
2. ✅ Teste cada script individualmente
3. ✅ Customize cores e tamanhos conforme necessário
4. ✅ Adicione filtros e interatividade
5. ✅ Publique o dashboard

## 📞 Suporte

Para dúvidas:
1. Verifique se todas as bibliotecas estão instaladas
2. Confirme se o Python está configurado no Power BI
3. Teste com dados menores primeiro
4. Verifique os logs de erro no Power BI
'''
    
    # Salvar instruções
    with open('GUIA_SCRIPTS_POWERBI.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Instruções geradas: GUIA_SCRIPTS_POWERBI.txt")

def main():
    """
    Função principal
    """
    
    import sys
    
    print("🎯 Script Combinado - Geração de Scripts Python para Power BI")
    print("=" * 70)
    
    # Verificar se o arquivo Excel foi fornecido
    if len(sys.argv) != 2:
        print("❌ Uso: python script_combinado_powerbi.py <arquivo_excel.xlsx>")
        print("📝 Exemplo: python script_combinado_powerbi.py Consolidado_Actual_x_Forecast_2025.xlsx")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    
    # Verificar se o arquivo Excel existe
    if not os.path.exists(excel_file):
        print(f"❌ Arquivo Excel não encontrado: {excel_file}")
        sys.exit(1)
    
    print(f"📁 Arquivo Excel: {excel_file}")
    
    # Carregar e combinar dados
    combined_df = load_and_combine_data(excel_file)
    
    if combined_df is None:
        print("❌ Erro ao carregar dados!")
        sys.exit(1)
    
    print(f"\n📊 Gerando scripts Python individuais...")
    
    # Gerar scripts individuais
    generate_script_1_budget_vs_actual_por_unidade()
    generate_script_2_performance_por_unidade()
    generate_script_3_consolidado_budget_vs_actual()
    generate_script_4_consolidado_performance()
    generate_script_5_dashboard_completo()
    generate_script_6_menu_interativo()
    
    # Gerar instruções
    generate_instructions()
    
    print(f"\n" + "=" * 70)
    print("✅ TODOS OS SCRIPTS GERADOS COM SUCESSO!")
    print("=" * 70)
    
    print(f"\n📁 Arquivos gerados:")
    print(f"   📊 budget_data_for_powerbi.csv (dados combinados)")
    print(f"   🐍 script_1_budget_vs_actual_por_unidade.py (COM FILTROS)")
    print(f"   🐍 script_2_performance_por_unidade.py (COM FILTROS)")
    print(f"   🐍 script_3_consolidado_budget_vs_actual.py (COM FILTROS)")
    print(f"   🐍 script_4_consolidado_performance.py (COM FILTROS)")
    print(f"   🐍 script_5_dashboard_completo.py (COM FILTROS)")
    print(f"   🎯 script_6_menu_interativo.py (MENU INTERATIVO)")
    print(f"   📋 GUIA_SCRIPTS_POWERBI.txt (instruções completas)")
    
    print(f"\n🎯 Como usar:")
    print(f"   1. 📥 Importe 'budget_data_for_powerbi.csv' no Power BI")
    print(f"   2. 🐍 Use os scripts Python nos visuais")
    print(f"   3. 📖 Siga o guia GUIA_SCRIPTS_POWERBI.txt")
    print(f"   4. 🎨 Customize cores e tamanhos conforme necessário")
    print(f"   5. 🚀 Publique seu dashboard!")

if __name__ == "__main__":
    main()
