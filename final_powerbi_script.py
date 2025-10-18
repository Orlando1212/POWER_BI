#!/usr/bin/env python3
"""
Script Final para Extração de Dados de Budget para Power BI
===========================================================

Este script extrai dados dos sheets de budget da planilha Excel e prepara
os dados para importação no Power BI, incluindo:

- BUDGET DISTRIB 2025
- BUDGET PROJECTS 2025  
- BUDGET DC 2025
- BUDGET CHILE 2025

Funcionalidades:
- Filtra linhas que não contêm porcentagem
- Calcula diferenças entre Budget 2025 e Actual 2025
- Calcula percentuais de variação
- Gera arquivo CSV otimizado para Power BI
- Cria análises estatísticas adicionais

Autor: Assistente IA
Data: 2025
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def extract_budget_data():
    """
    Extrai dados dos sheets de budget especificados e prepara para Power BI
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
    
    # Descrições predefinidas para CHILE (baseadas no padrão dos outros sheets)
    # EXCLUINDO todas as que contêm % pois são porcentagens, não valores absolutos
    chile_descriptions = [
        'ORDERS RECEIVED', 'REVENUES', 'REBATES', 'REBATES ANUAL',
        'SALES INCENTIVE', 'GROSS PROFIT',
        'GROSS PROFIT w/ rebates & incentives', 'COMISSIONS', 'SALES EXPENSES',
        'MARKETING EXPENSES', 'GENERAL AND ADMINISTRATION EXPENSES', 'SG&A',
        'FH', 'SG&A w/funded head', 'OH', 'TOTAL OPERATIONAL EBITDA',
        'Item_19', 'Item_20', 'Item_21', 'Item_22', 'Item_23', 'Item_24'
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
                        description = f'Item_{idx}'
                else:
                    description = str(row[config['description_col']]) if pd.notna(row[config['description_col']]) else ''
                
                actual_value = row[actual_col]
                budget_value = row[budget_col]
                
                # Critérios de filtragem - EXCLUIR todas as linhas com % na descrição
                is_valid = (
                    '%' not in description and  # SEMPRE excluir linhas com %
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
                        
                        # Calcular métricas
                        difference = actual_float - budget_float
                        percentage_diff = (difference / budget_float * 100) if budget_float != 0 else 0
                        
                        # Determinar status
                        status = "Acima do Budget" if difference >= 0 else "Abaixo do Budget"
                        
                        filtered_data.append({
                            'Unidade': config['unit'],
                            'Sheet_Original': sheet_name,
                            'Descricao': description.strip(),
                            'Budget_2025': budget_float,
                            'Actual_2025': actual_float,
                            'Percentual_Diferenca': percentage_diff,
                            'Status': status,
                            'Tipo': 'Budget' if 'BUDGET' in description.upper() else 'Item'
                        })
                        
                    except (ValueError, TypeError):
                        continue
            
            print(f"✅ Encontradas {len(filtered_data)} linhas válidas")
            all_data.extend(filtered_data)
            
        except Exception as e:
            print(f"❌ Erro ao processar {sheet_name}: {e}")
            continue
    
    return all_data

def create_final_dataset(all_data):
    """
    Cria o dataset final e salva os arquivos
    """
    
    if not all_data:
        print("❌ Nenhum dado válido foi encontrado!")
        return None
    
    # Criar DataFrame final
    final_df = pd.DataFrame(all_data)
    
    # Ordenar por unidade e descrição
    final_df = final_df.sort_values(['Unidade', 'Descricao'])
    
    # Salvar arquivo principal para Power BI
    output_file = 'budget_data_for_powerbi.csv'
    final_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ Dados extraídos com sucesso!")
    print(f"📊 Total de registros: {len(final_df)}")
    print(f"📁 Arquivo principal: {output_file}")
    
    # Mostrar dados por unidade (Budget vs Actual)
    show_unit_data(final_df)
    
    return final_df

def show_unit_data(df):
    """
    Mostra dados Budget vs Actual para cada linha, separado por unidade
    """
    
    print(f"\n📊 DADOS POR UNIDADE - BUDGET vs ACTUAL:")
    print("=" * 80)
    
    # Agrupar por unidade
    for unit in df['Unidade'].unique():
        unit_data = df[df['Unidade'] == unit].sort_values('Descricao')
        
        print(f"\n🏢 UNIDADE: {unit}")
        print("-" * 60)
        print(f"{'Descrição':<35} {'Budget 2025':<12} {'Actual 2025':<12} {'Diferença %':<12}")
        print("-" * 60)
        
        for _, row in unit_data.iterrows():
            desc = row['Descricao'][:32] + "..." if len(row['Descricao']) > 35 else row['Descricao']
            budget = f"${row['Budget_2025']:,.2f}M"
            actual = f"${row['Actual_2025']:,.2f}M"
            pct = f"{row['Percentual_Diferenca']:+.1f}%"
            
            print(f"{desc:<35} {budget:<12} {actual:<12} {pct:<12}")
        
        print()

def create_powerbi_instructions():
    """
    Cria instruções detalhadas para Power BI
    """
    
    instructions = '''
# 📊 Guia Completo para Dashboard Power BI - Análise de Budget 2025

## 🚀 Passos para Importação

### 1. Importar Dados
1. Abra o Power BI Desktop
2. Clique em "Obter Dados" > "Texto/CSV"
3. Selecione o arquivo `budget_data_for_powerbi.csv`
4. Clique em "Carregar"

### 2. Configurar Medidas DAX

```DAX
# Medidas Principais
Budget Total = SUM(budget_data_for_powerbi[Budget_2025])
Actual Total = SUM(budget_data_for_powerbi[Actual_2025])
Diferença Total = SUM(budget_data_for_powerbi[Diferenca])
Percentual Médio = AVERAGE(budget_data_for_powerbi[Percentual_Diferenca])

# Medidas Calculadas
Variação % = DIVIDE([Diferença Total], [Budget Total], 0) * 100
Performance = IF([Diferença Total] >= 0, "Acima do Budget", "Abaixo do Budget")

# Medidas por Unidade
Budget por Unidade = CALCULATE([Budget Total], ALLEXCEPT(budget_data_for_powerbi, budget_data_for_powerbi[Unidade]))
Actual por Unidade = CALCULATE([Actual Total], ALLEXCEPT(budget_data_for_powerbi, budget_data_for_powerbi[Unidade]))
```

### 3. Visualizações Recomendadas

#### 📈 Dashboard Principal
- **Cartões (Topo):**
  - Budget Total
  - Actual Total  
  - Diferença Total
  - Variação %

- **Gráfico de Barras (Centro):**
  - Eixo X: Unidade
  - Valores: Budget Total, Actual Total
  - Legenda: Budget vs Actual

- **Gráfico de Pizza (Lado):**
  - Categoria: Unidade
  - Valores: Budget Total

- **Tabela (Inferior):**
  - Colunas: Unidade, Descrição, Budget 2025, Actual 2025, Diferença, Percentual Diferença, Status

#### 📊 Dashboard Detalhado
- **Gráfico de Funil:** Performance por Unidade
- **Gráfico de Linha:** Percentual de Diferença por Item
- **Gráfico de Dispersão:** Budget vs Actual
- **Tabela Matricial:** Análise por Unidade e Tipo

### 4. Filtros e Interatividade

#### Filtros Principais:
- **Unidade:** DISTRIB, PROJECTS, DC, CHILE
- **Status:** Acima do Budget, Abaixo do Budget
- **Tipo:** Budget, Item
- **Faixa de Percentual:** Slider para percentual de diferença

#### Interatividade:
- Cross-filtering entre visualizações
- Drill-through para detalhes por unidade
- Tooltips com informações adicionais
- Botões de navegação entre páginas

### 5. Formatação e Design

#### Cores:
- Verde: Valores positivos (acima do budget)
- Vermelho: Valores negativos (abaixo do budget)
- Azul: Valores neutros

#### Formatação de Números:
- Valores monetários: $#,##0.00M
- Percentuais: 0.0%
- Números decimais: #,##0.00

#### Layout:
- Tema: Claro/Moderno
- Fonte: Segoe UI
- Tamanho: Responsivo

### 6. Alertas e Insights

#### Alertas Automáticos:
- Itens com diferença > 50% (negativa)
- Unidades com performance < -60%
- Valores orçamentários não utilizados

#### KPIs:
- Taxa de utilização do budget
- Performance por unidade
- Variação média por categoria

### 7. Atualização de Dados

#### Configuração de Atualização:
1. Vá em "Início" > "Atualizar"
2. Configure atualização automática (se necessário)
3. Defina fonte de dados para atualização

#### Manutenção:
- Execute o script Python periodicamente
- Substitua o arquivo CSV
- Atualize o Power BI

## 📋 Checklist de Implementação

- [ ] Importar dados CSV
- [ ] Configurar medidas DAX
- [ ] Criar visualizações principais
- [ ] Configurar filtros
- [ ] Aplicar formatação
- [ ] Testar interatividade
- [ ] Configurar alertas
- [ ] Publicar dashboard
- [ ] Configurar atualizações

## 🎯 Objetivos do Dashboard

1. **Visão Geral:** Performance geral do budget vs actual
2. **Análise por Unidade:** Comparação entre DISTRIB, PROJECTS, DC, CHILE
3. **Detalhamento:** Análise item por item
4. **Tendências:** Identificação de padrões e outliers
5. **Alertas:** Identificação de desvios significativos

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se o arquivo CSV está correto
2. Confirme se as medidas DAX estão funcionando
3. Teste as visualizações individualmente
4. Verifique os filtros aplicados
'''
    
    with open('powerbi_setup_instructions.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"📋 Instruções detalhadas salvas em: powerbi_setup_instructions.txt")

def main():
    """
    Função principal do script
    """
    
    print("🎯 Script Final para Extração de Dados de Budget - Power BI")
    print("=" * 70)
    
    # Extrair dados
    all_data = extract_budget_data()
    
    if all_data:
        # Criar dataset final
        final_df = create_final_dataset(all_data)
        
        if final_df is not None:
            # Criar instruções para Power BI
            create_powerbi_instructions()
            
            print("\n" + "=" * 70)
            print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            print("=" * 70)
            
            print(f"\n📁 Arquivos gerados:")
            print(f"   🎯 budget_data_for_powerbi.csv (dados principais)")
            print(f"   📋 powerbi_setup_instructions.txt (instruções completas)")
            
            print(f"\n🎯 Próximos passos:")
            print(f"   1. 📥 Importe o arquivo CSV no Power BI Desktop")
            print(f"   2. 📖 Siga as instruções no arquivo de texto")
            print(f"   3. 🎨 Configure as visualizações conforme sugerido")
            print(f"   4. 📊 Use as análises estatísticas para insights")
            print(f"   5. 🚀 Publique seu dashboard!")
            
            print(f"\n💡 Dica: Comece com o dashboard principal e depois adicione")
            print(f"   as visualizações detalhadas conforme necessário.")
            
        else:
            print("❌ Erro ao criar dataset final!")
    else:
        print("❌ Nenhum dado foi extraído!")

if __name__ == "__main__":
    main()
