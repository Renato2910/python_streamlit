import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Análise de Fatores de Cancelamento – Cartões", layout="wide")
df = pd.read_csv('aula_6/analise_de_dados/clientes.csv', sep=',', encoding='latin1')

st.title("📊 Dashboard de Cancelamento – Cartões de Crédito")
tot = len(df)
ativo = (df['Categoria']=='Cliente').sum()
cancel = (df['Categoria']=='Cancelado').sum()
cols = st.columns(6)
cols[0].metric("Total de Clientes",            tot)
cols[1].metric("Clientes Ativos",              ativo)
cols[2].metric("Clientes Cancelados",          cancel)
cols[3].metric("Percentual de Ativos",         f"{ativo/tot:.2%}")
cols[4].metric("Percentual de Cancelamentos",   f"{cancel/tot:.2%}")
cols[5].metric("Taxa de Cancelamento",         f"{cancel/tot:.2%}")

st.divider()

salary_order = [
    'Less than $40K',
    '$40K - $60K',
    '$60K - $80K',
    '$80K - $120K',
    '$120K +',
    'Não informado'
]
df['Faixa Salarial Anual'] = pd.Categorical(
    df['Faixa Salarial Anual'],
    categories=salary_order,
    ordered=True
)

bins = [18,25,35,45,55,65,100]
labels = ['18–24','25–34','35–44','45–54','55–64','65+']
df['Faixa Etária'] = pd.cut(df['Idade'], bins=bins, labels=labels, right=False)

salary_map = {
    'Less than $40K': 30000,
    '$40K - $60K':   50000,
    '$60K - $80K':   70000,
    '$80K - $120K': 100000,
    '$120K +':      140000
}
df['Salario_Aprox'] = df['Faixa Salarial Anual'].map(salary_map)
df_lim = df.dropna(subset=['Salario_Aprox']).copy()
df_lim['Razao_Limite_Salario'] = df_lim['Limite'] / df_lim['Salario_Aprox']

df['churn_flag'] = df['Categoria'].map({'Cliente':0, 'Cancelado':1})

st.header("🔎 Análises Segmentadas por Dimensão")
tabs = st.tabs([
    "🔹 Sexo",
    "💳 Categoria do Cartão",
    "🎂 Faixa Etária",
    "💰 Faixa Salarial"
])

with tabs[0]:
    st.subheader("Taxa de Cancelamento por Sexo")
    churn = df.groupby('Sexo')['Categoria'].apply(lambda x: (x=='Cancelado').mean())

    l, m, r = st.columns([1, 6, 1])
    with m:
        fig, ax = plt.subplots(figsize=(8,4))
        sns.barplot(x=churn.index, y=churn.values, ax=ax)
        ax.set_ylabel("Taxa de Cancelamento")
        ax.set_ylim(0, churn.max()*1.1)
        for bar in ax.patches:
            ax.text(bar.get_x()+bar.get_width()/2,
                    bar.get_height()+0.005,
                    f"{bar.get_height():.1%}",
                    ha='center')
        st.pyplot(fig, use_container_width=True)
        st.markdown(f"- **Feminino:** {churn.get('F',0):.1%}  \n- **Masculino:** {churn.get('M',0):.1%}")

with tabs[1]:
    st.subheader("Taxa de Cancelamento por Categoria do Cartão")
    churn = df.groupby('Categoria Cartão')['Categoria'].apply(lambda x: (x=='Cancelado').mean())

    l, m, r = st.columns([1, 6, 1])
    with m:
        fig, ax = plt.subplots(figsize=(10,4))
        sns.barplot(x=churn.index, y=churn.values, ax=ax)
        ax.set_ylabel("Taxa de Cancelamento")
        ax.set_ylim(0, churn.max()*1.1)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
        for bar in ax.patches:
            ax.text(bar.get_x()+bar.get_width()/2,
                    bar.get_height()+0.005,
                    f"{bar.get_height():.1%}",
                    ha='center')
        st.pyplot(fig, use_container_width=True)
        worst, best = churn.idxmax(), churn.idxmin()
        st.markdown(f"- **Maior:** {worst} ({churn[worst]:.1%})  \n- **Menor:** {best} ({churn[best]:.1%})")

with tabs[2]:
    st.subheader("Taxa de Cancelamento por Faixa Etária")
    churn = df.groupby('Faixa Etária')['Categoria'].apply(lambda x: (x=='Cancelado').mean())

    l, m, r = st.columns([1, 6, 1])
    with m:
        fig, ax = plt.subplots(figsize=(10,4))
        sns.barplot(x=churn.index, y=churn.values, ax=ax, order=labels)
        ax.set_ylabel("Taxa de Cancelamento")
        ax.set_ylim(0, churn.max()*1.1)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
        for bar in ax.patches:
            ax.text(bar.get_x()+bar.get_width()/2,
                    bar.get_height()+0.005,
                    f"{bar.get_height():.1%}",
                    ha='center')
        st.pyplot(fig, use_container_width=True)
        peak_age = churn.idxmax()
        st.markdown(f"- **Faixa com maior cancelamento:** {peak_age} ({churn[peak_age]:.1%})")

with tabs[3]:
    st.subheader("Taxa de Cancelamentopor Faixa Salarial Anual")
    churn = df.groupby('Faixa Salarial Anual')['Categoria'].apply(lambda x: (x=='Cancelado').mean())

    l, m, r = st.columns([1, 6, 1])
    with m:
        fig, ax = plt.subplots(figsize=(10,4))
        sns.barplot(x=churn.index, y=churn.values, order=salary_order, ax=ax)
        ax.set_ylabel("Taxa de Cancelamento")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
        ax.set_ylim(0, churn.max()*1.1)
        for bar in ax.patches:
            ax.text(bar.get_x()+bar.get_width()/2,
                    bar.get_height()+0.005,
                    f"{bar.get_height():.1%}",
                    ha='center')
        st.pyplot(fig, use_container_width=True)
        st.markdown(f"- **Cancelamento mais alto em:** {churn.idxmax()} ({churn.max():.1%})")
st.divider()

st.header("🚀 Principais Fatores de Cancelamento")
driver_feats = {
    'Contatos 12m':            'Número de Contatos (12m)',
    'Inatividade 12m':         'Meses Inativos (12m)',
    'Taxa de Utilização Cartão':'Utilização do Limite',
    'Produtos Contratados':    'Qtd. de Produtos'
}
feats = list(driver_feats.keys())
for i in range(0, len(feats), 2):
    f1, f2 = feats[i], feats[i+1] if i+1<len(feats) else None
    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6,3))
        sns.barplot(x='Categoria', y=f1, data=df, estimator='mean', ci=None, ax=ax)
        ax.set_title(driver_feats[f1])
        st.pyplot(fig, use_container_width=True)
    if f2:
        with c2:
            fig, ax = plt.subplots(figsize=(6,3))
            sns.barplot(x='Categoria', y=f2, data=df, estimator='mean', ci=None, ax=ax)
            ax.set_title(driver_feats[f2])
            st.pyplot(fig, use_container_width=True)
st.divider()

st.subheader("Correlação com Indicadores de Cancelamento")

fatores = list(driver_feats.keys())
corr_with_churn = (
    df[fatores + ['churn_flag']]
      .corr()['churn_flag']
      .drop('churn_flag')
      .sort_values()
)

fig, ax = plt.subplots(figsize=(6,4))
colors = corr_with_churn.apply(lambda v: 'salmon' if v<0 else 'seagreen')
bars = ax.barh(corr_with_churn.index, corr_with_churn.values, color=colors)

ax.axvline(0, color='gray', linewidth=1)            
ax.set_xlabel("Coeficiente de Correlação")          
ax.set_xlim(corr_with_churn.min()*1.1, corr_with_churn.max()*1.1)


for bar in bars:
    w = bar.get_width()
    ax.text(
        w + (0.01 if w>=0 else -0.01),
        bar.get_y() + bar.get_height()/2,
        f"{w:.2f}",
        va='center',
        ha='left' if w>=0 else 'right'
    )

st.pyplot(fig, use_container_width=True)
st.markdown("""
> **Insight:**  
> - +0.19 entre Contatos12m e churn_flag → muitos contatos indicam insatisfação.  
> - +0.12 entre Inatividade12m e churn_flag → longos períodos sem uso levam ao cancelamento.  
> - –0.08 entre Utilização e churn_flag → baixa utilização está associada a abandono.  
> - –0.05 entre Produtos e churn_flag → mais produtos = menor churn.
""")

st.divider()

st.header("📋 Plano de Ação Recomendada")
st.markdown("""
1. **Reengajamento automático** para quem acumular mais de 2 meses de inatividade (cashback, ofertas personalizadas).  
2. **Melhoria contínua do suporte**: monitorar contagens de contato e aplicar NPS pós-atendimento.  
3. **Cross-sell de Produtos**: incentivar contratação de seguros e benefícios para reduzir churn.  
4. **Revisão de limites**: política de “limite progressivo” alinhada ao uso e faixa salarial.  
""")
