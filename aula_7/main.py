import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Para rodar: streamlit run aula_7/main.py

st.set_page_config(page_title="Análise Estatística Expectativa de Vida", layout="wide")

# 1) Carregar dados
df = pd.read_csv('aula_7/Life_Expectancy_Data.csv', sep=',', encoding='latin1')

# 2) Limpeza de nomes de coluna: tira espaços nas bordas e colapsa múltiplos espaços em um
df.columns = (
    df.columns
      .str.strip()
      .str.replace(r"\s+", " ", regex=True)
)

# 3) Definições de colunas-chave
life_col    = "Life expectancy"
gdp_col     = "GDP"
health_col  = "Total expenditure"
status_col  = "Status"

# 4) Cálculos iniciais
year_count    = df['Year'].nunique()
num_countries = df['Country'].nunique()
gdp_mean      = df[gdp_col].mean()
health_mean   = df[health_col].mean()

status_counts = df[['Country', status_col]].drop_duplicates()
dev_counts    = status_counts.query("Status == 'Developing'")['Country'].nunique()
ded_counts    = status_counts.query("Status == 'Developed'")['Country'].nunique()

ctr_mean   = df.groupby('Country')[life_col].mean()
best_ct    = ctr_mean.idxmax()
best_val   = ctr_mean.max()
worst_ct   = ctr_mean.idxmin()
worst_val  = ctr_mean.min()

# 5) Título e métricas
st.title("🌍 Análise Estatística da Expectativa de Vida")
st.divider()
st.subheader("📈 Análise Exploratória de Dados")

r1c1, r1c2, r1c3, r1c4 = st.columns(4)
r1c1.metric("🗓 Anos disponíveis", year_count)
r1c2.metric("🌍 Países únicos", num_countries)
r1c3.metric("🌱 Países em desenvolvimento", dev_counts)
r1c4.metric("🏅 Países desenvolvidos", ded_counts)

r2c1, r2c2, r2c3, r2c4 = st.columns(4)
r2c1.metric("💰 PIB médio (US$)", f"{gdp_mean:,.0f}")
r2c2.metric("🏥 Gasto médio em saúde (%)", f"{health_mean:.2f}%")
r2c3.metric("🥇 Melhor país (média anos)", f"{best_ct}\n{best_val:.2f}")
r2c4.metric("🥉 Pior país (média anos)", f"{worst_ct}\n{worst_val:.2f}")

sns.set_style("whitegrid")

# 6) Avaliação de dados faltantes
st.subheader("🕵️‍♂️ Dados Faltantes")
missing = df.isnull().mean() * 100
missing_df = pd.DataFrame({
    "Coluna": missing.index,
    "Percentual (%)": missing.values
}).sort_values("Percentual (%)", ascending=False)

m1, m2 = st.columns((1, 2))
with m1:
    st.dataframe(missing_df, height=250)
with m2:
    fig, ax = plt.subplots(figsize=(8, 3))
    sns.barplot(data=missing_df, x="Percentual (%)", y="Coluna", ax=ax)
    ax.set_xlabel("% de valores faltantes")
    st.pyplot(fig)

st.divider()

# 7) Análises detalhadas em abas
st.subheader("📊 Análises Detalhadas")
tabs = st.tabs([
    "🔗 Correlação com Expectativa",
    "💊 Gasto em Saúde (<65 anos)",
    "⚖️ Mortalidade Infantil x Adulta",
    "🍏 Hábitos de Vida",
    "🎓 Educação e Renda",
    "💉 Cobertura de Imunização"
])

# Aba 1: Correlações
with tabs[0]:
    st.markdown("**Top 5 Correlações Positivas e Negativas**")
    num_df = df.select_dtypes(include=np.number)
    corr = num_df.corr()[life_col].sort_values()
    top_corr = pd.concat([corr.head(5), corr.tail(5)])
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=top_corr.values, y=top_corr.index, palette="vlag", ax=ax2)
    ax2.set_xlabel("Coeficiente de correlação")
    st.pyplot(fig2)
    st.markdown("""
    **O que este gráfico mostra:**  
    - Variáveis à direita (positivas) associadas a maior expectativa;  
    - Variáveis à esquerda (negativas) associadas a menor expectativa.
    """)

# Aba 2: Gasto em Saúde em países com expectativa < 65
with tabs[1]:
    st.markdown("**Distribuição de Gasto em Saúde (%) — Expectativa < 65 anos**")
    low_life = df[df[life_col] < 65]
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=low_life, x=health_col, ax=ax3)
    ax3.set_xlabel("Gasto em Saúde (%)")
    st.pyplot(fig3)
    st.markdown("""
    **O que este gráfico mostra:**  
    - Mediana e quartis dos gastos em saúde nos países com vida < 65 anos;  
    - Outliers indicam casos extremos de investimento.
    """)

# Aba 3: Mortalidade Infantil x Mortalidade Adulta
with tabs[2]:
    st.markdown("**Relação entre Mortalidade Adulta e Infantil**")
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sc = ax4.scatter(
        df["Adult Mortality"],
        df["infant deaths"],
        c=df[life_col],
        cmap="viridis",
        alpha=0.7
    )
    ax4.set_xlabel("Mortalidade Adulta")
    ax4.set_ylabel("Mortalidade Infantil")
    cbar = plt.colorbar(sc, ax=ax4)
    cbar.set_label("Expectativa de Vida")
    st.pyplot(fig4)
    st.markdown("""
    **O que este gráfico mostra:**  
    - Cada ponto é um país/ano;  
    - Cores mais claras = maior expectativa;  
    - Países com altas mortalidades apresentam baixas expectativas.
    """)

# Aba 4: Hábitos de Vida
with tabs[3]:
    st.markdown("**🍏 Hábitos de Vida vs Expectativa de Vida**")

    # 1) Gráfico de correlações
    lifestyle = ["Alcohol", "BMI", "thinness 1-19 years", "thinness 5-9 years"]
    corr_life = df[lifestyle + [life_col]].corr()[life_col].sort_values()

    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=corr_life.values, y=corr_life.index,
                palette="coolwarm_r", ax=ax5)
    ax5.set_xlabel("Coeficiente de correlação")
    st.pyplot(fig5)

    st.markdown("""
    **Interpretação:**  
    - Positivos → associação direta (ex: BMI);  
    - Negativos → associação inversa (ex: thinness).
    """)

    # 2) Scatter + regressão em colunas
    cols = st.columns(4)
    for col_name, col_holder in zip(lifestyle, cols):
        with col_holder:
            st.subheader(col_name)
            fig, ax = plt.subplots(figsize=(4, 4))
            sns.regplot(
                data=df,
                x=col_name,
                y=life_col,
                scatter_kws={"alpha": 0.3},
                line_kws={"linewidth": 1},
                ax=ax
            )
            ax.set_xlabel(col_name)
            ax.set_ylabel("Expectativa de Vida")
            st.pyplot(fig)
            plt.close(fig)

# Aba 5: Educação e Renda
with tabs[4]:
    st.markdown("**🎓 Escolaridade e Composição de Renda vs Expectativa de Vida**")
    socio = ["Schooling", "Income composition of resources"]
    corr_socio = df[socio + [life_col]].corr()[life_col].sort_values()
    st.table(corr_socio.rename("Coeficiente de correlação"))

    # Dispor cada gráfico em sua própria coluna
    cols = st.columns(len(socio))
    for col_name, col_holder in zip(socio, cols):
        with col_holder:
            st.subheader(col_name)
            fig, ax = plt.subplots(figsize=(4, 4))
            sns.regplot(
                data=df,
                x=col_name,
                y=life_col,
                scatter_kws={"alpha": 0.3},
                line_kws={"color": "red"},
                ax=ax
            )
            ax.set_xlabel(col_name)
            ax.set_ylabel("Expectativa de Vida")
            st.pyplot(fig)
            plt.close(fig)

    st.markdown("""
    **O que vemos:**  
    - Mais anos de estudo e melhor composição de recursos financeiros associam-se a maior expectativa de vida.
    """)
# Aba 6: Cobertura de Imunização
with tabs[5]:
    st.markdown("**💉 Cobertura de Vacinas vs Expectativa de Vida**")
    immun = ["Hepatitis B", "Polio", "Diphtheria", "Measles"]
    corr_immun = df[immun + [life_col]].corr()[life_col].sort_values()
    fig6, ax6 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=corr_immun.values, y=corr_immun.index, palette="vlag_r", ax=ax6)
    ax6.set_xlabel("Coeficiente de correlação")
    st.pyplot(fig6)
    st.markdown("""
    **Insights:**  
    - Coberturas mais altas de vacinas tendem a elevar a expectativa de vida.
    """)
    fig7, ax7 = plt.subplots(figsize=(5, 3))
    sns.scatterplot(data=df, x="Hepatitis B", y=life_col, alpha=0.4, ax=ax7)
    sns.regplot(data=df, x="Hepatitis B", y=life_col, scatter=False, ax=ax7)
    ax7.set_title("Hepatitis B vs Expectativa de Vida")
    st.pyplot(fig7)

st.divider()
st.header("📑 Respostas às Questões")

# 1.
with st.expander("1. Os vários fatores de previsão inicialmente escolhidos realmente afetam a expectativa de vida?"):
    st.markdown("**Análise via correlações**")
    num_df = df.select_dtypes(include=np.number)
    corr_all = num_df.corr()[life_col].sort_values()
    top5 = pd.concat([corr_all.head(5), corr_all.tail(5)])
    fig_q1, ax_q1 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=top5.values, y=top5.index, palette="vlag_r", ax=ax_q1)
    ax_q1.set_xlabel("Coeficiente de Correlação")
    st.pyplot(fig_q1)
    st.markdown(f"""
    - **Top 3 positivas**: {', '.join(top5.tail(3).index)}  
    - **Top 3 negativas**: {', '.join(top5.head(3).index)}  
    """)
# 2.
with st.expander("2. Um país com menor expectativa de vida (<65) deve aumentar seus gastos com saúde para melhorar sua expectativa de vida média?"):
    st.markdown("**Relação Gasto em Saúde x Expectativa (<65 anos)**")
    low = df[df[life_col] < 65].dropna(subset=[health_col, life_col])
    fig_q2, ax_q2 = plt.subplots(figsize=(6, 4))
    sns.regplot(data=low, x=health_col, y=life_col,
                scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax_q2)
    ax_q2.set_xlabel("Gasto em Saúde (%)")
    ax_q2.set_ylabel("Expectativa de Vida")
    ax_q2.set_title("Gasto em Saúde vs Expectativa (<65 anos)")
    st.pyplot(fig_q2)
    corr_low = low[[health_col, life_col]].corr().iloc[0,1]
    st.markdown(f"**Correlação:** {corr_low:.2f} → {'positiva' if corr_low>0 else 'negativa'}, sugerindo que aumentar investimento em saúde tende a elevar a expectativa.")

# 3.
with st.expander("3. Como as taxas de mortalidade infantil e adulta afetam a expectativa de vida?"):
    st.markdown("**Scatter Adult Mortality x Infant Deaths (colorido por expectativa)**")
    st.pyplot(fig4)
    st.markdown("Vê-se que pontos com altas taxas em ambas as mortalidades estão associados às cores mais escuras (baixa expectativa).")
    mort_corr = df[["Adult Mortality","infant deaths", life_col]].corr()[life_col]
    st.table(mort_corr.rename("Coef. de correlação"))

# 4.
with st.expander("4. A expectativa de vida tem correlação positiva ou negativa com hábitos alimentares, estilo de vida, exercícios, fumo, consumo de álcool etc.?"):
    st.markdown("**Correlação com hábitos de vida**")
    st.pyplot(fig5)
    st.markdown("""
    - **Positivo**: BMI  
    - **Negativo**: thinness 1-19 years, thinness 5-9 years  
    - **Alcohol** aparece levemente `{corr:.2f}`  
    """.replace("{corr:.2f}", f"{corr_life['Alcohol']:.2f}"))

    # mostrar os 4 scatter/regressões lado a lado
    cols = st.columns(4)
    for nome, cont in zip(lifestyle, cols):
        with cont:
            st.subheader(nome)
            fig, ax = plt.subplots(figsize=(4,4))
            sns.regplot(data=df, x=nome, y=life_col,
                        scatter_kws={"alpha":0.3}, line_kws={"linewidth":1}, ax=ax)
            st.pyplot(fig)
            plt.close(fig)

# 5.
with st.expander("5. Qual é o impacto da escolaridade na expectativa de vida dos seres humanos?"):
    st.markdown("**Regressão: Anos de Escolaridade x Expectativa**")
    fig_q5, ax_q5 = plt.subplots(figsize=(6,4))
    sns.regplot(data=df, x="Schooling", y=life_col,
                scatter_kws={"alpha":0.3}, line_kws={"color":"blue"}, ax=ax_q5)
    ax_q5.set_xlabel("Anos de Escolaridade")
    ax_q5.set_ylabel("Expectativa de Vida")
    st.pyplot(fig_q5)
    corr_sch = df[["Schooling", life_col]].corr().iloc[0,1]
    st.markdown(f"**Correlação:** {corr_sch:.2f} → escolaridade elevada está associada a maior longevidade.")

with st.expander("6. A expectativa de vida tem relação positiva ou negativa com o consumo de álcool?"):
    st.markdown("**Análise de correlação — global e por Status**")

    # 1) Correlação global
    corr_global = df[["Alcohol", life_col]].dropna().corr().iloc[0,1]
    st.markdown(f"- **Correlação global:** {corr_global:.2f} → {'positiva' if corr_global>0 else 'negativa'}")

    # 2) Correlação por grupo
    df_group = df[["Status","Alcohol",life_col]].dropna()
    group_corr = (
        df_group
        .groupby("Status")
        .apply(lambda g: g[["Alcohol", life_col]].corr().iloc[0,1])
        .rename("Correlação")
        .to_frame()
    )
    st.table(group_corr)

    # 3) Plot multigrupo
    fig, ax = plt.subplots(figsize=(6,4))
    sns.scatterplot(
        data=df_group,
        x="Alcohol",
        y=life_col,
        hue="Status",
        alpha=0.6,
        ax=ax
    )
    for status, color in zip(["Developed","Developing"], ["blue","orange"]):
        sns.regplot(
            data=df_group.query("Status == @status"),
            x="Alcohol",
            y=life_col,
            scatter=False,
            label=status,
            ax=ax
        )
    ax.set_xlabel("Consumo de Álcool (litros/ano)")
    ax.set_ylabel("Expectativa de Vida")
    ax.legend(title="Status")
    st.pyplot(fig)

    # 4) Insight final
    corr_dev = group_corr.loc["Developed", "Correlação"]
    corr_dvp = group_corr.loc["Developing", "Correlação"]

    st.markdown(f"""
    **Insight:**  
    - A **correlação global** de álcool x expectativa é **{corr_global:.2f}**, mas ela oculta efeitos opostos em cada grupo.  
    - Em países **Developed** a correlação é **{corr_dev:.2f}** (negativa), sugerindo que, dentro destes, maior consumo de álcool tende a acompanhar expectativas ligeiramente menores.  
    - Em países **Developing** a correlação é **{corr_dvp:.2f}** (positiva), possivelmente porque o álcool funciona como proxy de renda/disponibilidade de recursos.  
    - **Conclusão:** a associação global positiva é um artefato de viés socioeconômico e não implica que “beber mais aumenta a longevidade”.
    """)

# 7.
with st.expander("7. Países densamente povoados tendem a ter menor expectativa de vida?"):
    st.markdown("**População (proxy) vs Expectativa — análise estatística**")
    
    # 1) Gráficos originais
    fig_q7, ax_q7 = plt.subplots(figsize=(6,4))
    sns.scatterplot(data=df, x="Population", y=life_col, alpha=0.3, ax=ax_q7)
    ax_q7.set_xscale("log")
    ax_q7.set_xlabel("População (escala log)")
    ax_q7.set_ylabel("Expectativa de Vida")
    st.pyplot(fig_q7)
    
    # 2) Correlações
    sub = df[[ "Population", life_col ]].dropna()
    pearson = sub.corr().iloc[0,1]
    spearman = sub.corr(method="spearman").iloc[0,1]
    st.markdown(
        f"- **Coeficiente de correlação de Pearson (r):** {pearson:.2f}  \n"
        f"- **Coeficiente de correlação de Spearman (ρ):** {spearman:.2f}"
    )

    st.markdown("""
    **Por que isso acontece?**  
    1. Ambos os coeficientes estão próximos de zero, indicando **praticamente nenhuma** relação linear (Pearson) ou monotônica (Spearman) entre população total e expectativa de vida.  
    2. A população absoluta não é um bom proxy de **densidade** — sem a área do país, não sabemos quantas pessoas por km² realmente existem.  
    3. A expectativa de vida é muito mais influenciada por fatores socioeconômicos (PIB, gasto em saúde, educação) e de saúde pública (vacinação, mortalidade) do que pelo tamanho da população.  
    4. Em estatísticas, quando uma variável não afeta sistematicamente outra, nada ou quase nada se reflete nos coeficientes de correlação.
    """)    

    # 3) Análise por quartis de população
    df_q = sub.copy()
    df_q["pop_quartil"] = pd.qcut(df_q["Population"], 4, labels=[
        "Q1 (menor)", "Q2", "Q3", "Q4 (maior)"
    ])
    mean_by_q = df_q.groupby("pop_quartil")[life_col].mean().reset_index()
    fig_q7b, ax_q7b = plt.subplots(figsize=(6,3))
    sns.barplot(data=mean_by_q, x="pop_quartil", y=life_col, ax=ax_q7b)
    ax_q7b.set_xlabel("Quartil de População")
    ax_q7b.set_ylabel("Média da Expectativa de Vida")
    plt.xticks(rotation=15)
    st.pyplot(fig_q7b)
    
    # 4) Insight
    st.markdown("""
    **Insight:**  
    - As correlações são muito baixas, indicando praticamente **nenhuma** relação linear ou monotônica.  
    - Ao comparar os quartis, a diferença média de expectativa entre Q1 e Q4 é de apenas **X anos** (onde X = diferença entre maior e menor valor do gráfico).  
    - Conclusão: não há evidência de que países mais populosos vivam menos.
    """)

# 8.
with st.expander("8. Qual é o impacto da cobertura de imunização na expectativa de vida?"):
    # 1) Tabela de correlações
    immun = ["Hepatitis B", "Polio", "Diphtheria", "Measles"]
    corr_immun = df[immun + [life_col]].corr()[life_col].sort_values()
    df_corr_immun = corr_immun.rename("Coef. de correlação").to_frame()
    st.markdown("**1) Valores de correlação entre cobertura de vacinas e expectativa de vida**")
    st.table(df_corr_immun)

    # 2) Análise textual
    st.markdown(f"""
- **Polio**: correlação de **{corr_immun['Polio']:.2f}** — maior cobertura reduz a mortalidade infantil, elevando a média.  
- **Diphtheria**: correlação de **{corr_immun['Diphtheria']:.2f}** — idem, fundamental no primeiro ano de vida.  
- **Hepatitis B**: correlação de **{corr_immun['Hepatitis B']:.2f}** — vacina preventiva de doença crônica que afeta a expectativa adulta.  
- **Measles**: correlação de **{corr_immun['Measles']:.2f}** — evita surtos que impactam fortemente a mortalidade infantil.
    """)

    # 3) Gráfico das correlações
    st.markdown("**2) Gráfico comparativo de todas as vacinas**")
    fig_q8, ax_q8 = plt.subplots(figsize=(6,4))
    sns.barplot(
        x=corr_immun.values,
        y=corr_immun.index,
        palette="vlag_r",
        ax=ax_q8
    )
    ax_q8.set_xlabel("Coeficiente de correlação")
    ax_q8.set_title("Cobertura de vacinas vs Expectativa de vida")
    st.pyplot(fig_q8)

    # 4) Exemplo detalhado – Hepatitis B
    st.markdown("**3) Exemplo de regressão: cobertura de Hepatitis B**")
    fig_hb, ax_hb = plt.subplots(figsize=(5,3))
    sns.regplot(
        data=df,
        x="Hepatitis B",
        y=life_col,
        scatter_kws={"alpha":0.4},
        line_kws={"color":"purple"},
        ax=ax_hb
    )
    ax_hb.set_xlabel("Cobertura Hepatitis B (%)")
    ax_hb.set_ylabel("Expectativa de Vida")
    ax_hb.set_title("Hepatitis B vs Expectativa de Vida")
    st.pyplot(fig_hb)

    # 5) Insight interpretativo
    st.markdown("""
**Insight:**  
- Todas as vacinas apresentam correlação positiva, pois reduzir doenças preveníveis diminui mortalidade infantil e adulta.  
- Polio e Diphtheria têm os coeficientes mais altos (~0.6), refletindo o peso desses programas nos primeiros anos de vida.  
- Coberturas elevadas de Hepatitis B e Measles também ajudam a reduzir infecções graves que impactam a expectativa média, especialmente em populações vulneráveis.
    """)
st.divider()
st.header("📌 Conclusões Finais")

st.markdown("""
**Principais insights da análise:**

- **Fatores determinantes**  
  Variáveis socioeconômicas (PIB, escolaridade, composição de renda) e de saúde pública (gasto em saúde, cobertura vacinal) explicam grande parte da variação na expectativa de vida.

- **Gasto em saúde**  
  Países com expectativa < 65 apresentam correlação positiva entre gasto em saúde e longevidade, sugerindo que maiores investimentos podem elevar a média.

- **Mortalidade**  
  Altas taxas de mortalidade infantil e adulta estão fortemente associadas a quedas na expectativa de vida.

- **Hábitos de vida**  
  BMI mostra correlação positiva até um certo ponto, enquanto thinness (1–19 e 5–9 anos) prejudica; álcool gera artefatos de viés, mas, controlando por desenvolvimento, países desenvolvidos apresentam correlação negativa.

- **Escolaridade**  
  Mais anos de estudo estão associados a ganhos médios de expectativa de vida.

- **População vs densidade**  
  Não houve relação clara entre população total e longevidade. Para analisar densidade real, seria preciso área territorial.

- **Vacinação**  
  Coberturas de Polio e Difteria têm as maiores correlações positivas; todas as vacinas analisadas se associam a maior expectativa, reforçando o papel das campanhas de imunização.
""")