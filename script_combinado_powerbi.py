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

def load_and_combine_data():
    """
    Gera os CSVs chamando os scripts e combina os dados
    """
    
    print("📊 Gerando dados dos scripts...")
    
    # Executar script final usando subprocess
    print("\n🚀 Executando script final_powerbi_script.py...")
    import subprocess
    result_final = subprocess.run(['python', 'final_powerbi_script.py'], 
                                 capture_output=True, text=True)
    if result_final.returncode != 0:
        print(f"❌ Erro ao executar final_powerbi_script.py: {result_final.stderr}")
        return None
    else:
        print("✅ Script final executado com sucesso!")
    
    # Executar script consolidado usando subprocess
    print("\n🚀 Executando script_consolidado.py...")
    result_consolidado = subprocess.run(['python', 'script_consolidado.py'], 
                                       capture_output=True, text=True)
    if result_consolidado.returncode != 0:
        print(f"❌ Erro ao executar script_consolidado.py: {result_consolidado.stderr}")
        return None
    else:
        print("✅ Script consolidado executado com sucesso!")
    
    print("\n📊 Carregando e combinando dados...")
    
    # Verificar se os arquivos foram criados
    if not os.path.exists('budget_data_for_powerbi.csv'):
        print("❌ Arquivo budget_data_for_powerbi.csv não foi criado!")
        return None
    
    if not os.path.exists('dados_consolidados_budget.csv'):
        print("❌ Arquivo dados_consolidados_budget.csv não foi criado!")
        return None
    
    # Carregar dados individuais por unidade
    df_individual = pd.read_csv('budget_data_for_powerbi.csv')
    
    # Carregar dados consolidados
    df_consolidado = pd.read_csv('dados_consolidados_budget.csv')
    
    # Adicionar identificador de tipo
    df_individual['Tipo_Analise'] = 'Por Unidade'
    df_consolidado['Tipo_Analise'] = 'Consolidado'
    
    # Adicionar coluna de unidade para consolidado
    df_consolidado['Unidade'] = 'CONSOLIDADO'
    
    # Adicionar colunas que faltam no consolidado
    df_consolidado['Sheet_Original'] = 'CONSOLIDADO'
    df_consolidado['Tipo'] = 'Item'
    
    # Combinar os dados
    combined_df = pd.concat([df_individual, df_consolidado], ignore_index=True)
    
    # Salvar CSV combinado
    combined_df.to_csv('dados_combinados_powerbi.csv', index=False, encoding='utf-8')
    
    print(f"✅ Dados combinados salvos em: dados_combinados_powerbi.csv")
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
    Gera script para gráfico Budget vs Actual por Unidade
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Gráfico: Budget vs Actual por Unidade
# ======================================

# Filtrar apenas dados por unidade (não consolidado)
df_unidades = df[df['Tipo_Analise'] == 'Por Unidade'].copy()

# Agrupar por unidade
summary = df_unidades.groupby('Unidade').agg({
    'Budget_2025': 'sum',
    'Actual_2025': 'sum'
}).reset_index()

# Configurar cores para cada unidade
colors = {
    'CHILE': '#FF6B6B',
    'DC': '#4ECDC4', 
    'DISTRIB': '#45B7D1',
    'PROJECTS': '#96CEB4'
}

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
ax.set_title('📊 Budget vs Actual por Unidade', fontsize=16, fontweight='bold')
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
    Gera script para gráfico Performance por Unidade
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Gráfico: Performance por Unidade
# ================================

# Filtrar apenas dados por unidade (não consolidado)
df_unidades = df[df['Tipo_Analise'] == 'Por Unidade'].copy()

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
ax.set_title('📈 Performance Média por Unidade', fontsize=16, fontweight='bold')
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
    Gera script para gráfico Consolidado Budget vs Actual
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Gráfico: Consolidado Budget vs Actual
# ====================================

# Filtrar apenas dados consolidados
df_consolidado = df[df['Tipo_Analise'] == 'Consolidado'].copy()

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
ax.set_title('💰 Top 10 Maiores Budgets Consolidados', fontsize=16, fontweight='bold')
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
    Gera script para gráfico Performance Consolidado
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Gráfico: Performance Consolidado
# ================================

# Filtrar apenas dados consolidados
df_consolidado = df[df['Tipo_Analise'] == 'Consolidado'].copy()

# Filtrar itens com maior variação
significant_changes = df_consolidado[
    (df_consolidado['Percentual_Diferenca'].abs() > 50) | 
    (df_consolidado['Budget_2025'] > 5)  # Incluir itens com budget > 5M
].head(10)

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
ax.set_title('📈 Performance Consolidado - Principais Itens', fontsize=16, fontweight='bold')
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
    Gera script para dashboard completo
    """
    
    script_content = create_python_script_template()
    
    script_content += '''
# Dashboard Completo - Budget vs Actual
# ====================================

# Criar figura com múltiplos subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('📊 Dashboard Completo - Budget vs Actual 2025', fontsize=18, fontweight='bold')

# 1. Budget vs Actual por Unidade
df_unidades = df[df['Tipo_Analise'] == 'Por Unidade'].copy()
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

# 2. Performance por Unidade
performance = df_unidades.groupby('Unidade')['Percentual_Diferenca'].mean()
colors_perf = ['#2ECC71' if pct >= 0 else '#E74C3C' for pct in performance.values]

bars_perf = ax2.bar(performance.index, performance.values, color=colors_perf, alpha=0.7)
ax2.set_xlabel('Unidade', fontsize=10, fontweight='bold')
ax2.set_ylabel('Performance (%)', fontsize=10, fontweight='bold')
ax2.set_title('📈 Performance por Unidade', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)

# 3. Top Budgets Consolidados
df_consolidado = df[df['Tipo_Analise'] == 'Consolidado'].copy()
top_5 = df_consolidado.nlargest(5, 'Budget_2025')

bars3 = ax3.barh(range(len(top_5)), top_5['Budget_2025'], color='#9B59B6', alpha=0.8)
ax3.set_yticks(range(len(top_5)))
ax3.set_yticklabels([desc[:20] + '...' if len(desc) > 20 else desc 
                    for desc in top_5['Descricao']], fontsize=9)
ax3.set_xlabel('Budget (MUSD)', fontsize=10, fontweight='bold')
ax3.set_title('🏆 Top 5 Budgets Consolidados', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='x')
ax3.invert_yaxis()

# 4. Resumo Executivo
ax4.axis('off')

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

ax4.set_title('📋 Resumo Executivo', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
'''
    
    # Salvar script
    with open('script_5_dashboard_completo.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script 5 gerado: script_5_dashboard_completo.py")

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

### 4. Dicas de Uso

#### Configurações Recomendadas:
- Tamanho do visual: 800x600 pixels
- Formato: PNG ou SVG
- Resolução: 300 DPI

#### Filtros:
- Use filtros de página para focar em unidades específicas
- Combine com slicers para análise interativa
- Aplique filtros de data se disponível

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
    
    print("🎯 Script Combinado - Geração de Scripts Python para Power BI")
    print("=" * 70)
    
    # Carregar e combinar dados
    combined_df = load_and_combine_data()
    
    print(f"\n📊 Gerando scripts Python individuais...")
    
    # Gerar scripts individuais
    generate_script_1_budget_vs_actual_por_unidade()
    generate_script_2_performance_por_unidade()
    generate_script_3_consolidado_budget_vs_actual()
    generate_script_4_consolidado_performance()
    generate_script_5_dashboard_completo()
    
    # Gerar instruções
    generate_instructions()
    
    print(f"\n" + "=" * 70)
    print("✅ TODOS OS SCRIPTS GERADOS COM SUCESSO!")
    print("=" * 70)
    
    print(f"\n📁 Arquivos gerados:")
    print(f"   📊 dados_combinados_powerbi.csv (dados combinados)")
    print(f"   🐍 script_1_budget_vs_actual_por_unidade.py")
    print(f"   🐍 script_2_performance_por_unidade.py")
    print(f"   🐍 script_3_consolidado_budget_vs_actual.py")
    print(f"   🐍 script_4_consolidado_performance.py")
    print(f"   🐍 script_5_dashboard_completo.py")
    print(f"   📋 GUIA_SCRIPTS_POWERBI.txt (instruções completas)")
    
    print(f"\n🎯 Como usar:")
    print(f"   1. 📥 Importe 'dados_combinados_powerbi.csv' no Power BI")
    print(f"   2. 🐍 Use os scripts Python nos visuais")
    print(f"   3. 📖 Siga o guia GUIA_SCRIPTS_POWERBI.txt")
    print(f"   4. 🎨 Customize cores e tamanhos conforme necessário")
    print(f"   5. 🚀 Publique seu dashboard!")

if __name__ == "__main__":
    main()
