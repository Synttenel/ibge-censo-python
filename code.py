import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# ETAPA 1: EXTRACT & TRANSFORM (ETL)
# ==========================================

# 1. Leitura do ficheiro bruto
with open('Analfabetismo_data.csv', 'r', encoding='utf-8', errors='ignore') as f:
    all_lines = f.readlines()

# Função para preenchimento sequencial (forward-fill) em listas de cabeçalho
def ffill_list(l):
    res, curr = [], ''
    for item in l:
        if item != '': 
            curr = item
        res.append(curr)
    return res

# 2. Reconstrução dos níveis de cabeçalho
sexo_list = ffill_list(all_lines[4].strip().split(';'))
raca_list = ffill_list(all_lines[5].strip().split(';'))
idade_list = ffill_list(all_lines[6].strip().split(';'))
status_list = all_lines[7].strip().split(';')

col_tuples = [
    (sexo_list[i], raca_list[i], idade_list[i], status_list[i]) 
    for i in range(1, len(status_list))
]

# 3. Leitura dos dados numéricos
data_rows = [line.strip().split(';')[1:] for line in all_lines[8:41]]
locations = [line.strip().split(';')[0] for line in all_lines[8:41]]

columns = pd.MultiIndex.from_tuples(
    col_tuples, 
    names=['Sexo', 'Cor_Raca', 'Grupo_Idade', 'Status_Alfabetizacao']
)

df_raw = pd.DataFrame(data_rows, index=locations, columns=columns).apply(pd.to_numeric, errors='coerce')
df_raw.index.name = 'Localizacao'

# 4. Despivotagem (Melt) para estrutura Tidy
df_long = pd.melt(
    df_raw.reset_index(), 
    id_vars=['Localizacao'], 
    var_name=['Sexo', 'Cor_Raca', 'Grupo_Idade', 'Status_Alfabetizacao'], 
    value_name='Pessoas'
)

df_tidy = df_long.pivot_table(
    index=['Localizacao', 'Sexo', 'Cor_Raca', 'Grupo_Idade'], 
    columns='Status_Alfabetizacao', 
    values='Pessoas', 
    aggfunc='first'
).reset_index()

# 5. Tratamento de nulos e cálculo da taxa de analfabetismo (%)
df_tidy[['Alfabetizadas', 'Não alfabetizadas', 'Total']] = df_tidy[['Alfabetizadas', 'Não alfabetizadas', 'Total']].fillna(0)
df_tidy['Taxa_Analfabetismo_Pct'] = np.where(
    df_tidy['Total'] > 0, 
    (df_tidy['Não alfabetizadas'] / df_tidy['Total']) * 100, 
    0.0
)

# Salvar o dataset transformado
df_tidy.to_csv('Analfabetismo_data_ETL_Completo.csv', index=False, encoding='utf-8-sig')


# ==========================================
# ETAPA 2: VISUALIZAÇÃO COM MATPLOTLIB PURO
# ==========================================

plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# ------------------------------------------
# Gráfico 1: Taxa de Analfabetismo por Idade
# ------------------------------------------
df_idade = df_tidy[
    (df_tidy['Localizacao'] == 'Brasil') & 
    (df_tidy['Sexo'] == 'Total') & 
    (df_tidy['Cor_Raca'] == 'Total') & 
    (df_tidy['Grupo_Idade'] != 'Total')
].sort_values(by='Taxa_Analfabetismo_Pct', ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor('#f8f9fa')
bars = ax.barh(df_idade['Grupo_Idade'], df_idade['Taxa_Analfabetismo_Pct'], color='#2b5c8f', edgecolor='#1a3654', alpha=0.9, height=0.7)
ax.set_title('Taxa de Analfabetismo por Faixa Etária - Brasil (Censo 2022)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Taxa de Analfabetismo (%)', fontsize=11, fontweight='bold')
ax.set_ylabel('Grupo de Idade', fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6, axis='x')

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.3, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', ha='left', fontsize=9, fontweight='bold')

ax.set_xlim(0, max(df_idade['Taxa_Analfabetismo_Pct']) * 1.15)
plt.tight_layout()
plt.savefig('grafico_analfabetismo_idade_pure_mpl.png', dpi=300)
plt.show()

# ------------------------------------------
# Gráfico 2: Taxa de Analfabetismo por Cor/Raça
# ------------------------------------------
df_raca = df_tidy[
    (df_tidy['Localizacao'] == 'Brasil') & 
    (df_tidy['Sexo'] == 'Total') & 
    (df_tidy['Cor_Raca'] != 'Total') & 
    (df_tidy['Grupo_Idade'] == 'Total')
].sort_values(by='Taxa_Analfabetismo_Pct', ascending=False)

fig, ax = plt.subplots(figsize=(9, 5))
ax.set_facecolor('#f8f9fa')
colors_raca = ['#2e8b57', '#e96a42', '#4682b4', '#d6709a', '#8a2be2']
bars = ax.bar(df_raca['Cor_Raca'], df_raca['Taxa_Analfabetismo_Pct'], color=colors_raca, edgecolor='black', alpha=0.85, width=0.6)
ax.set_title('Taxa de Analfabetismo por Cor ou Raça - Brasil (2022)', fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Taxa de Analfabetismo (%)', fontsize=11, fontweight='bold')
ax.set_xlabel('Cor ou Raça', fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6, axis='y')

for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.2, f'{h:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylim(0, max(df_raca['Taxa_Analfabetismo_Pct']) * 1.18)
plt.tight_layout()
plt.savefig('grafico_analfabetismo_raca_pure_mpl.png', dpi=300)
plt.show()

# ------------------------------------------
# Gráfico 3: Taxa de Analfabetismo por Região
# ------------------------------------------
regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
df_regioes = df_tidy[
    (df_tidy['Localizacao'].isin(regioes)) & 
    (df_tidy['Sexo'] == 'Total') & 
    (df_tidy['Cor_Raca'] == 'Total') & 
    (df_tidy['Grupo_Idade'] == 'Total')
].sort_values(by='Taxa_Analfabetismo_Pct', ascending=False)

fig, ax = plt.subplots(figsize=(9, 5))
ax.set_facecolor('#f8f9fa')
colors_reg = ['#d95f02', '#e7298a', '#7570b3', '#1b9e77', '#e6ab02']
bars = ax.bar(df_regioes['Localizacao'], df_regioes['Taxa_Analfabetismo_Pct'], color=colors_reg, edgecolor='black', alpha=0.85, width=0.6)
ax.set_title('Taxa de Analfabetismo por Região do Brasil (2022)', fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Taxa de Analfabetismo (%)', fontsize=11, fontweight='bold')
ax.set_xlabel('Grande Região', fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6, axis='y')

for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.2, f'{h:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylim(0, max(df_regioes['Taxa_Analfabetismo_Pct']) * 1.18)
plt.tight_layout()
plt.savefig('grafico_analfabetismo_regioes_pure_mpl.png', dpi=300)
plt.show()