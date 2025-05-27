import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



st.set_page_config(
    page_title="Desafio 5 – Dados Educacionais",
    layout="wide",
)
df = pd.read_csv('aula_5/desafio_5/dados_alunos_escola.csv', sep=',', encoding='utf-8')

st.title("🎓 Desafio 5 – Análise de Dados Educacionais")

st.divider()

st.header("📈 Estatísticas Descritivas")

tab1, tab2, tab3 = st.tabs([
    "📐 Matemática",
    "📖 Português",
    "🔬 Ciências"
])

with tab1:
    st.subheader("Métricas de Matemática")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Média Matemática",        f"{df['nota_matematica'].mean():.2f}")
    col2.metric("Mediana Matemática",      f"{df['nota_matematica'].median():.2f}")
    col3.metric("Moda Matemática",         f"{int(df['nota_matematica'].mode()[0])}")
    col4.metric("Variância Matemática",    f"{df['nota_matematica'].var():.2f}")
    col5.metric("Amplitude Matemática",    f"{df['nota_matematica'].max() - df['nota_matematica'].min():.2f}")
    col6.metric("Desvio Padrão Matemática",f"{df['nota_matematica'].std():.2f}")

with tab2:
    st.subheader("Métricas de Português")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Média Português",         f"{df['nota_portugues'].mean():.2f}")
    col2.metric("Mediana Português",       f"{df['nota_portugues'].median():.2f}")
    col3.metric("Moda Português",          f"{int(df['nota_portugues'].mode()[0])}")
    col4.metric("Variância Português",     f"{df['nota_portugues'].var():.2f}")
    col5.metric("Amplitude Português",     f"{df['nota_portugues'].max() - df['nota_portugues'].min():.2f}")
    col6.metric("Desvio Padrão Português", f"{df['nota_portugues'].std():.2f}")

with tab3:
    st.subheader("Métricas de Ciências")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Média Ciências",          f"{df['nota_ciencias'].mean():.2f}")
    col2.metric("Mediana Ciências",        f"{df['nota_ciencias'].median():.2f}")
    col3.metric("Moda Ciências",           f"{int(df['nota_ciencias'].mode()[0])}")
    col4.metric("Variância Ciências",      f"{df['nota_ciencias'].var():.2f}")
    col5.metric("Amplitude Ciências",      f"{df['nota_ciencias'].max() - df['nota_ciencias'].min():.2f}")
    col6.metric("Desvio Padrão Ciências",  f"{df['nota_ciencias'].std():.2f}")

#2. Qual é a frequência média dos alunos por série?
st.header("📊 Frequência Média por Série")
st.subheader("Frequência Média dos Alunos por Série")

# calcula e formata
frequencia_media = (
    df
    .groupby('serie')['frequencia_%']
    .mean()
    .round(2)
    .reset_index()
    .rename(columns={'frequencia_%': 'Média Frequência (%)'})
    .rename(columns={'serie': 'Série'})
)

st.table(
    frequencia_media.style.format({
        'Média Frequência (%)': '{:.2f}'
    })
)

st.divider()


#Filtre os alunos com frequência abaixo de 75% e calcule a média geral deles.
st.header("🔎 Filtros e Agrupamentos")
st.subheader("Alunos com Frequência Abaixo de 75%")

frequencia_baixa = df[df['frequencia_%'] < 75]

total_alunos = len(frequencia_baixa)
media_individual = frequencia_baixa[['nota_matematica','nota_portugues','nota_ciencias']].mean(axis=1)
media_geral = media_individual.mean()
col1, col2 = st.columns(2)
col1.metric("Total de alunos", f"{total_alunos}")
col2.metric("Média geral das notas", f"{media_geral:.2f}")

st.subheader("Média de Notas por Cidade e Matéria")
media_por_cidade = (
    df
    .groupby('cidade')[['nota_matematica', 'nota_portugues', 'nota_ciencias']]
    .mean()
    .reset_index()
)
media_por_cidade.columns = ['Cidade', 'Média Matemática', 'Média Português', 'Média Ciências']
st.table(
    media_por_cidade.style.format({
        'Média Matemática': '{:.2f}',
        'Média Português': '{:.2f}',
        'Média Ciências': '{:.2f}'
    })
)

# 6. Quantos alunos possuem a nota menor que 3,0?
# 7. Quantos alunos possuem a nota menor que 5,0?
# 8. Quantos alunos possuem a nota menor que 7,0?
# 9. Quantos alunos possuem a nota menor que 9,0?
# 10. Quantos alunos possuem a nota igual a 10,0?
def classificar_aluno(nota):
    if nota < 3.0:
        return "Reprovado"
    elif nota < 6.0:
        return "Exame"
    else:
        return "Aprovado"

st.subheader("Classificação dos Alunos por Nota")

alunos_menor_3  = (df['nota_matematica'] < 3.0).sum()
alunos_menor_5  = (df['nota_matematica'] < 5.0).sum()
alunos_menor_7  = (df['nota_matematica'] < 7.0).sum()
alunos_menor_9  = (df['nota_matematica'] < 9.0).sum()
alunos_igual_10 = (df['nota_matematica'] == 10.0).sum()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Nota menor que 3",       f"{alunos_menor_3}")
col2.metric("Nota menor que 5",       f"{alunos_menor_5}")
col3.metric("Nota menor que 7",       f"{alunos_menor_7}")
col4.metric("Nota menor que 9",       f"{alunos_menor_9}")
col5.metric("Nota igual a 10",        f"{alunos_igual_10}")

#11. Qual cidade tem a melhor nota em Matemática, português e ciências? E a Pior nota?
st.subheader("Melhores e Piores Notas por Cidade")
melhor_matematica = df.loc[df['nota_matematica'].idxmax(), ['cidade', 'nota_matematica']]
melhor_portugues = df.loc[df['nota_portugues'].idxmax(), ['cidade', 'nota_portugues']] 
melhor_ciencias = df.loc[df['nota_ciencias'].idxmax(), ['cidade', 'nota_ciencias']]
pior_matematica = df.loc[df['nota_matematica'].idxmin(), ['cidade', 'nota_matematica']]
pior_portugues = df.loc[df['nota_portugues'].idxmin(), ['cidade', 'nota_portugues']]
pior_ciencias = df.loc[df['nota_ciencias'].idxmin(), ['cidade', 'nota_ciencias']]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    ### 📐 Matemática
    - 🏆 **Melhor**: {melhor_matematica['cidade']} — {melhor_matematica['nota_matematica']:.2f}
    - 📉 **Pior**:  {pior_matematica['cidade']}   — {pior_matematica['nota_matematica']:.2f}
    """)

with col2:
    st.markdown(f"""
    ### 📖 Português
    - 🏆 **Melhor**: {melhor_portugues['cidade']} — {melhor_portugues['nota_portugues']:.2f}
    - 📉 **Pior**:  {pior_portugues['cidade']}   — {pior_portugues['nota_portugues']:.2f}
    """)

with col3:
    st.markdown(f"""
    ### 🔬 Ciências
    - 🏆 **Melhor**: {melhor_ciencias['cidade']}  — {melhor_ciencias['nota_ciencias']:.2f}
    - 📉 **Pior**:  {pior_ciencias['cidade']}    — {pior_ciencias['nota_ciencias']:.2f}
    """)

st.divider()
st.header("📈 Visualizações")
#5. Crie um histograma das notas de todas as matérias.
st.subheader("Histograma das Notas por Matéria")
fig, ax = plt.subplots(1, 3, figsize=(18, 6))
df['nota_matematica'].hist(bins=20, ax=ax[0], color='green', alpha=0.7)
df['nota_portugues'].hist(bins=20, ax=ax[1], color='yellow', alpha=0.7)
df['nota_ciencias'].hist(bins=20, ax=ax[2], color='blue', alpha=0.7)
ax[0].set_title('Histograma de Matemática')
ax[0].set_xlabel('Notas')
ax[0].set_ylabel('Frequência')
ax[0].grid(False)
ax[1].set_title('Histograma de Português')
ax[1].set_xlabel('Notas')
ax[1].set_ylabel('Frequência')
ax[1].grid(False)
ax[2].set_title('Histograma de Ciências')
ax[2].set_xlabel('Notas')
ax[2].set_ylabel('Frequência')
ax[2].grid(False)
st.pyplot(fig)

# 6. Gere um boxplot comparando notas de português por série.
# 7. Gere um boxplot comparando notas de matemática por série.
# 8. Gere um boxplot comparando notas de ciências por série.
st.subheader("Notas por Série")
# Lista de colunas e títulos
materias = ['nota_portugues', 'nota_matematica', 'nota_ciencias']
titulos  = ['Português', 'Matemática', 'Ciências']

# Cria figura com 3 subplots
fig, ax = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for i, (col, titulo) in enumerate(zip(materias, titulos)):
    for s in sorted(df['serie'].unique()):
        subset = df[df['serie'] == s]
        sns.kdeplot(
            subset[col],
            ax=ax[i],
            label=f'Série {s}',
            fill=True,
            alpha=0.3
        )
    ax[i].set_title(f'Densidade de {titulo} por Série')
    ax[i].set_xlabel('Nota')
    if i == 0:
        ax[i].set_ylabel('Densidade')
    else:
        ax[i].set_ylabel('')
    ax[i].legend(title='Série')
    
plt.tight_layout()
st.pyplot(fig)

# 9. Crie um gráfico de barras com a quantidade de alunos por cidade.
st.subheader("Quantidade de Alunos por Cidade")
fig, ax = plt.subplots(figsize=(10, 4))
sns.countplot(
    data=df,
    x='cidade',
    order=df['cidade'].value_counts().index,
    palette='inferno',
    ax=ax
)
ax.set_title('Quantidade de Alunos por Cidade')
ax.set_xlabel('Cidade')
ax.set_ylabel('Quantidade de Alunos')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# 10. Faça um gráfico de dispersão entre frequencia_% e nota por matéria
st.subheader("Gráfico de Dispersão: Frequência vs Notas")
fig, ax = plt.subplots(1, 3, figsize=(18, 6))
sns.scatterplot(
    data=df,
    x='frequencia_%',
    y='nota_matematica',
    ax=ax[0],
    color='green',
    alpha=0.6
)
sns.scatterplot(
    data=df,
    x='frequencia_%',
    y='nota_portugues',
    ax=ax[1],
    color='yellow',
    alpha=0.6
)
sns.scatterplot(
    data=df,
    x='frequencia_%',
    y='nota_ciencias',
    ax=ax[2],
    color='blue',
    alpha=0.6
)
ax[0].set_title('Frequência vs Matemática')
ax[0].set_xlabel('Frequência (%)')
ax[0].set_ylabel('Nota Matemática')
ax[1].set_title('Frequência vs Português')
ax[1].set_xlabel('Frequência (%)')
ax[1].set_ylabel('Nota Português')
ax[2].set_title('Frequência vs Ciências')
ax[2].set_xlabel('Frequência (%)')
ax[2].set_ylabel('Nota Ciências')
ax[0].grid(False)
ax[1].grid(False)
ax[2].grid(False)
plt.tight_layout()
st.pyplot(fig)
