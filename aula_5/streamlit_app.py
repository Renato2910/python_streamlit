import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações gerais da página
st.set_page_config(
    page_title="Dashboard Estatístico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e descrição
st.title("📊 Dashboard de Estatística e Visualização")
st.markdown(
    """
    Neste dashboard você pode explorar:
    - Estatísticas descritivas (média, mediana, moda, variância, amplitude)
    - Distribuição por estado
    - Boxplot de salário por departamento
    - Dispersão entre idade e salário
    """
)

# Carregamento de dados (com cache para performance)
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=",", encoding="utf-8")
    # Cria coluna de faixa etária
    def faixa_etaria(idade):
        if idade <= 25:
            return "Jovem"
        elif idade <= 45:
            return "Adulto"
        else:
            return "Sênior"
    df["faixa_etaria"] = df["idade"].apply(faixa_etaria)
    return df

df = load_data("aula_5/dados_estatistica_visualizacao.csv")

# Estatísticas descritivas rápidas
st.subheader("📈 Estatísticas Descritivas")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Média Idade", f"{df['idade'].mean():.2f}")
col2.metric("Mediana Idade", f"{df['idade'].median():.2f}")
col3.metric("Moda Idade", f"{int(df['idade'].mode()[0])}")
col4.metric("Variância Idade", f"{df['idade'].var():.2f}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Média Salário", f"{df['salario'].mean():.2f}")
col6.metric("Mediana Salário", f"{df['salario'].median():.2f}")
col7.metric("Moda Salário", f"{int(df['salario'].mode()[0])}")
col8.metric("Amplitude Salário", f"{df['salario'].max() - df['salario'].min():.2f}")

# Mostrar dados brutos (expansível)
with st.expander("🗄️ Ver dados brutos"):
    st.dataframe(df, use_container_width=True)

# Separar gráficos em abas
tab1, tab2, tab3 = st.tabs([
    "📊 Distribuição por Estado",
    "📦 Boxplot por Departamento",
    "🔎 Dispersão Idade × Salário"
])

with tab1:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(
        data=df,
        x="estado",
        order=df["estado"].value_counts().index,
        ax=ax
    )
    ax.set_title("Distribuição por Estado")
    ax.set_xlabel("Estado")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(
        data=df,
        x="departamento",
        y="salario",
        ax=ax
    )
    ax.set_title("Salário por Departamento")
    ax.set_xlabel("Departamento")
    ax.set_ylabel("Salário")
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.scatterplot(
        data=df,
        x="idade",
        y="salario",
        hue="departamento",
        palette="tab10",
        ax=ax
    )
    ax.set_title("Dispersão: Idade vs. Salário")
    ax.set_xlabel("Idade")
    ax.set_ylabel("Salário")
    st.pyplot(fig)
