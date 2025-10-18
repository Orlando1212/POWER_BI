#!/usr/bin/env python3
"""
Script Simples para Gráficos Budget vs Actual por Unidade
=======================================================

Cria apenas gráficos de Budget vs Actual para cada unidade,
sem performance nem análises por item.

Autor: Assistente IA
Data: 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo
plt.style.use('default')

def load_data():
    """
    Carrega os dados do CSV
    """
    print("📊 Carregando dados do CSV...")
    df = pd.read_csv('budget_data_for_powerbi.csv')
    print(f"✅ {len(df)} registros carregados")
    return df

def create_budget_vs_actual_charts(df):
    """
    Cria gráficos simples de Budget vs Actual para cada unidade
    """
    
    # Configurar cores para cada unidade
    unit_colors = {
        'CHILE': '#FF6B6B',
        'DC': '#4ECDC4', 
        'DISTRIB': '#45B7D1',
        'PROJECTS': '#96CEB4'
    }
    
    # Obter unidades únicas
    units = df['Unidade'].unique()
    
    # Criar figura com subplots para cada unidade
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('📊 Budget vs Actual por Unidade', fontsize=24, fontweight='bold')
    
    axes = axes.flatten()
    
    for i, unit in enumerate(units):
        ax = axes[i]
        
        # Filtrar dados da unidade
        unit_data = df[df['Unidade'] == unit].copy()
        
        # Ordenar por Budget (maior para menor)
        unit_data = unit_data.sort_values('Budget_2025', ascending=True)
        
        # Preparar dados para o gráfico
        y_pos = np.arange(len(unit_data))
        
        # Criar gráfico de barras horizontais
        bars_budget = ax.barh(y_pos - 0.2, unit_data['Budget_2025'], 
                             height=0.4, label='Budget 2025', 
                             color=unit_colors[unit], alpha=0.8)
        
        bars_actual = ax.barh(y_pos + 0.2, unit_data['Actual_2025'], 
                             height=0.4, label='Actual 2025', 
                             color='#E67E22', alpha=0.8)
        
        # Configurar eixo Y
        ax.set_yticks(y_pos)
        ax.set_yticklabels([desc[:25] + '...' if len(desc) > 25 else desc 
                           for desc in unit_data['Descricao']], fontsize=9)
        
        # Configurar título e labels
        ax.set_xlabel('Valor (MUSD)', fontsize=12, fontweight='bold')
        ax.set_title(f'🏢 {unit}', fontsize=16, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='x')
        
        # Adicionar valores nas barras
        for j, (budget, actual) in enumerate(zip(unit_data['Budget_2025'], unit_data['Actual_2025'])):
            # Budget
            ax.text(budget + 0.05, y_pos[j] - 0.2, f'${budget:.2f}M', 
                   va='center', ha='left', fontsize=8, fontweight='bold')
            # Actual
            ax.text(actual + 0.05, y_pos[j] + 0.2, f'${actual:.2f}M', 
                   va='center', ha='left', fontsize=8, fontweight='bold')
        
        # Inverter eixo Y para mostrar maior budget no topo
        ax.invert_yaxis()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    
    return fig

def create_difference_percentage_charts(df):
    """
    Cria gráficos de diferença percentual entre Budget e Actual
    """
    
    # Configurar cores baseadas na performance
    def get_performance_color(value):
        if value >= 0:
            return '#2ECC71'  # Verde para positivo
        else:
            return '#E74C3C'  # Vermelho para negativo
    
    # Obter unidades únicas
    units = df['Unidade'].unique()
    
    # Criar figura com subplots para cada unidade
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('📈 Diferença Percentual por Unidade', fontsize=24, fontweight='bold')
    
    axes = axes.flatten()
    
    for i, unit in enumerate(units):
        ax = axes[i]
        
        # Filtrar dados da unidade
        unit_data = df[df['Unidade'] == unit].copy()
        
        # Ordenar por diferença percentual (pior para melhor)
        unit_data = unit_data.sort_values('Percentual_Diferenca', ascending=True)
        
        # Preparar dados para o gráfico
        y_pos = np.arange(len(unit_data))
        colors = [get_performance_color(pct) for pct in unit_data['Percentual_Diferenca']]
        
        # Criar gráfico de barras horizontais
        bars = ax.barh(y_pos, unit_data['Percentual_Diferenca'], 
                      color=colors, alpha=0.7)
        
        # Configurar eixo Y
        ax.set_yticks(y_pos)
        ax.set_yticklabels([desc[:25] + '...' if len(desc) > 25 else desc 
                           for desc in unit_data['Descricao']], fontsize=9)
        
        # Configurar título e labels
        ax.set_xlabel('Diferença Percentual (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'🏢 {unit}', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Linha de referência (0%)
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.5, linewidth=2)
        
        # Adicionar valores nas barras
        for j, (bar, pct) in enumerate(zip(bars, unit_data['Percentual_Diferenca'])):
            width = bar.get_width()
            ax.text(width + (1 if width >= 0 else -1), bar.get_y() + bar.get_height()/2,
                   f'{pct:+.1f}%', ha='left' if width >= 0 else 'right', 
                   va='center', fontsize=8, fontweight='bold')
        
        # Inverter eixo Y para mostrar maior diferença no topo
        ax.invert_yaxis()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    
    return fig

def main():
    """
    Função principal
    """
    
    print("🎯 Script Simples - Gráficos Budget vs Actual por Unidade")
    print("=" * 60)
    
    # Carregar dados
    df = load_data()
    
    print(f"\n📊 Criando gráficos...")
    
    # 1. Gráficos de Budget vs Actual por Unidade
    print("📈 Criando gráficos Budget vs Actual por unidade...")
    fig1 = create_budget_vs_actual_charts(df)
    fig1.savefig('budget_vs_actual_por_unidade.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico salvo como: budget_vs_actual_por_unidade.png")
    
    # 2. Gráficos de Diferença Percentual por Unidade
    print("📊 Criando gráficos de diferença percentual por unidade...")
    fig2 = create_difference_percentage_charts(df)
    fig2.savefig('diferenca_percentual_por_unidade.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico salvo como: diferenca_percentual_por_unidade.png")
    
    # Mostrar os gráficos
    print("\n🖼️ Exibindo gráficos...")
    plt.show()
    
    # Estatísticas simples
    print(f"\n📊 RESUMO POR UNIDADE:")
    print("=" * 50)
    
    for unit in df['Unidade'].unique():
        unit_data = df[df['Unidade'] == unit]
        total_budget = unit_data['Budget_2025'].sum()
        total_actual = unit_data['Actual_2025'].sum()
        items_count = len(unit_data)
        
        print(f"\n🏢 {unit}:")
        print(f"   📊 {items_count} itens")
        print(f"   💰 Budget Total: ${total_budget:.2f}M")
        print(f"   💵 Actual Total: ${total_actual:.2f}M")
        print(f"   📉 Diferença: ${total_actual - total_budget:+.2f}M")
    
    print(f"\n📁 Arquivos gerados:")
    print(f"   📊 budget_vs_actual_por_unidade.png")
    print(f"   📈 diferenca_percentual_por_unidade.png")

if __name__ == "__main__":
    main()
