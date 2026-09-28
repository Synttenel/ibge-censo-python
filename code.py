import pandas as pd
import matplotlib.pyplot as plt



# Leitura do Arquivo

df = pd.read_csv("Analfabetismo_data_ETL_Completo.csv")


# Transformação de valores do arquivo em valor numérico

df["Alfabetizadas"] = pd.to_numeric(
    df["Alfabetizadas"],
    errors="coerce"
)

df["Não alfabetizadas"] = pd.to_numeric(
    df["Não alfabetizadas"],
    errors="coerce"
)

df["Total"] = pd.to_numeric(
    df["Total"],
    errors="coerce"
)


# Taxa de Analfabetismo

df["Taxa_Analfabetismo_Pct"] = (
    df["Não alfabetizadas"] / df["Total"]
) * 100

df["Taxa_Analfabetismo_Pct"] = (
    df["Taxa_Analfabetismo_Pct"].round(2)
)



# Dataframe printado no terminal, contagem de linhas

print(df)


# Criação de um arquivo para armazenar as etapas de ETL

df.to_csv(
    "Analfabetismo_ETL_Final.csv",
    index=False,
    encoding="utf-8-sig"
)


# Gráfico de Região
regioes = [
    "Nordeste",
    "Norte",
    "Centro-Oeste",
    "Sudeste",
    "Sul"
]

dados_regiao = df[
    (df["Localizacao"].isin(regioes)) &
    (df["Sexo"] == "Total") &
    (df["Cor_Raca"] == "Total") &
    (df["Grupo_Idade"] == "Total")
]

dados_regiao = dados_regiao.set_index("Localizacao")
dados_regiao = dados_regiao.loc[regioes]


plt.figure(figsize=(10, 5))

plt.bar(
    dados_regiao.index,
    dados_regiao["Taxa_Analfabetismo_Pct"],
    color=[
        "#e67e22",
        "#e84393",
        "#8e86bd",
        "#36a987",
        "#f0b91c"
    ],
    edgecolor="black",
    linewidth=0.5
)

plt.title(
    "Taxa de Analfabetismo por Região do Brasil (2022)",
    fontsize=13,
    fontweight="bold"
)

plt.xlabel("Grande Região", fontweight="bold")
plt.ylabel("Taxa de Analfabetismo (%)", fontweight="bold")

plt.grid(axis="y", alpha=0.3)
plt.ylim(0, 16.5)

for i, valor in enumerate(
    dados_regiao["Taxa_Analfabetismo_Pct"]
):
    plt.text(
        i,
        valor + 0.2,
        f"{valor:.1f}%",
        ha="center",
        fontweight="bold"
    )

plt.tight_layout()
plt.show()


# Gráfico de Cor ou Raça

cores_raca = [
    "Indígena",
    "Preta",
    "Parda",
    "Branca",
    "Amarela"
]

dados_raca = df[
    (df["Localizacao"] == "Brasil") &
    (df["Sexo"] == "Total") &
    (df["Grupo_Idade"] == "Total") &
    (df["Cor_Raca"].isin(cores_raca))
]

dados_raca = dados_raca.set_index("Cor_Raca")
dados_raca = dados_raca.loc[cores_raca]


plt.figure(figsize=(10, 5))

plt.bar(
    dados_raca.index,
    dados_raca["Taxa_Analfabetismo_Pct"],
    color=[
        "#76c7b0",
        "#ff9470",
        "#8fa4c8",
        "#dc8abd",
        "#a9d45b"
    ],
    edgecolor="black",
    linewidth=0.5
)

plt.title(
    "Taxa de Analfabetismo por Cor ou Raça - Brasil (2022)",
    fontsize=13,
    fontweight="bold"
)

plt.xlabel("Cor ou Raça", fontweight="bold")
plt.ylabel("Taxa de Analfabetismo (%)", fontweight="bold")

plt.grid(axis="y", alpha=0.3)
plt.ylim(0, 18)

for i, valor in enumerate(
    dados_raca["Taxa_Analfabetismo_Pct"]
):
    plt.text(
        i,
        valor + 0.3,
        f"{valor:.1f}%",
        ha="center",
        fontweight="bold"
    )

plt.tight_layout()
plt.show()


# Gráfico de Idade/ faixa etária

idades = [
    "15 a 19 anos",
    "20 a 24 anos",
    "25 a 34 anos",
    "35 a 44 anos",
    "45 a 54 anos",
    "55 a 64 anos",
    "65 anos ou mais",
    "75 anos ou mais",
    "80 anos ou mais"
]

dados_idade = df[
    (df["Localizacao"] == "Brasil") &
    (df["Sexo"] == "Total") &
    (df["Cor_Raca"] == "Total") &
    (df["Grupo_Idade"].isin(idades))
]

dados_idade = dados_idade.set_index("Grupo_Idade")
dados_idade = dados_idade.loc[idades]


plt.figure(figsize=(10, 5))

plt.barh(
    dados_idade.index,
    dados_idade["Taxa_Analfabetismo_Pct"],
    color="#3d8abe",
    edgecolor="black",
    linewidth=0.5
)

plt.title(
    "Taxa de Analfabetismo por Faixa Etária - Brasil (Censo 2022)",
    fontsize=13,
    fontweight="bold"
)

plt.xlabel("Taxa de Analfabetismo (%)", fontweight="bold")
plt.ylabel("Grupo de idade", fontweight="bold")

plt.grid(axis="x", alpha=0.3)
plt.xlim(0, 32)

for i, valor in enumerate(
    dados_idade["Taxa_Analfabetismo_Pct"]
):
    plt.text(
        valor + 0.3,
        i,
        f"{valor:.1f}%",
        va="center",
        fontweight="bold"
    )

plt.tight_layout()
plt.show()


# Gráfico Sexo/Gênero

dados_sexo = df[
    (df["Localizacao"] == "Brasil") &
    (df["Cor_Raca"] == "Total") &
    (df["Grupo_Idade"] == "Total") &
    (df["Sexo"] != "Total")
]

dados_sexo = dados_sexo[
    ["Sexo", "Taxa_Analfabetismo_Pct"]
]

dados_sexo = dados_sexo.set_index("Sexo")


plt.figure(figsize=(8, 5))

plt.bar(
    dados_sexo.index,
    dados_sexo["Taxa_Analfabetismo_Pct"],
    color=["#4a90e2", "#e8759b"],
    edgecolor="black",
    linewidth=0.5
)

plt.title(
    "Taxa de Analfabetismo por Sexo - Brasil (2022)",
    fontsize=13,
    fontweight="bold"
)

plt.xlabel(
    "Sexo",
    fontweight="bold"
)

plt.ylabel(
    "Taxa de Analfabetismo (%)",
    fontweight="bold"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.ylim(
    0,
    max(dados_sexo["Taxa_Analfabetismo_Pct"]) + 2
)


# Valores acima das barras
for i, valor in enumerate(
    dados_sexo["Taxa_Analfabetismo_Pct"]
):
    plt.text(
        i,
        valor + 0.2,
        f"{valor:.1f}%",
        ha="center",
        fontweight="bold"
    )

plt.tight_layout()
plt.show()
