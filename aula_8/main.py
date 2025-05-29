import streamlit as st
import pandas as pd
import sqlite3
#streamlit run aula_8/main.py
conn = sqlite3.connect('aula_8/biblioteca.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    quantidade_disponivel INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES autores(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
)
''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    devolvido boolean NOT NULL,
    FOREIGN KEY (livro_id) REFERENCES livros(id)
)
''')
conn.commit()

# Insere dados fictícios nas tabelas

# Exemplo para inserção dos autores
cursor.execute("SELECT COUNT(*) FROM autores")
if cursor.fetchone()[0] == 0:
    autores = [
        ("J.K. Rowling",),
        ("George R. R. Martin",),
        ("J.R.R. Tolkien",),
        ("Agatha Christie",),
        ("Stephen King",)
    ]
    cursor.executemany("INSERT INTO autores (nome) VALUES (?)", autores)
    conn.commit()

# Exemplo para inserção das categorias
cursor.execute("SELECT COUNT(*) FROM categorias")
if cursor.fetchone()[0] == 0:
    categorias = [
        ("Fantasia",),
        ("Mistério",),
        ("Terror",),
        ("Ficção Científica",),
        ("Romance",)
    ]
    cursor.executemany("INSERT INTO categorias (nome) VALUES (?)", categorias)
    conn.commit()

# Exemplo para inserção dos livros (pelo menos 10)
cursor.execute("SELECT COUNT(*) FROM livros")
if cursor.fetchone()[0] == 0:
    livros = [
        ("Harry Potter and the Sorcerer's Stone", 1, 1, 1997, 5),
        ("Harry Potter and the Chamber of Secrets", 1, 1, 1998, 4),
        ("A Game of Thrones", 2, 1, 1996, 3),
        ("A Clash of Kings", 2, 1, 1998, 3),
        ("The Hobbit", 3, 1, 1937, 6),
        ("The Lord of the Rings", 3, 1, 1954, 5),
        ("Murder on the Orient Express", 4, 2, 1934, 4),
        ("And Then There Were None", 4, 2, 1939, 4),
        ("The Shining", 5, 3, 1977, 5),
        ("It", 5, 3, 1986, 4),
        ("Carrie", 5, 3, 1974, 3),
        ("Misery", 5, 3, 1987, 2)
    ]
    cursor.executemany("""
        INSERT INTO livros (titulo, autor_id, categoria_id, ano, quantidade_disponivel)
        VALUES (?, ?, ?, ?, ?)
    """, livros)
    conn.commit()

# Exemplo para inserção dos empréstimos
cursor.execute("SELECT COUNT(*) FROM emprestimos")
if cursor.fetchone()[0] == 0:
    emprestimos = [
        (1, "2025-05-27", 0),
        (2, "2025-05-26", 1),
        (3, "2025-05-25", 0),
        (4, "2025-05-24", 1),
        (5, "2025-05-23", 0),
        (6, "2025-05-22", 1),
        (7, "2025-05-21", 0),
        (8, "2025-05-20", 1),
        (9, "2025-05-19", 0),
        (10, "2025-05-18", 1)
    ]
    cursor.executemany("""
        INSERT INTO emprestimos (livro_id, data_emprestimo, devolvido)
        VALUES (?, ?, ?)
    """, emprestimos)
    conn.commit()

st.set_page_config(page_title="Biblioteca", layout="wide")
st.title("🌍 Biblioteca Senai")
st.divider()

# ===== Atividade 1 =====
st.subheader("Todos os livros com nome do autor e da categoria.")

# Busca todos os livros com autor e categoria
query = """
SELECT 
    l.id,
    l.titulo,
    a.nome      AS Autor,
    c.nome      AS Categoria
    FROM livros l
    INNER JOIN autores a
  ON l.autor_id = a.id
    INNER JOIN categorias c
  ON l.categoria_id = c.id;
"""
df_livros = pd.read_sql_query(query, conn)

# Exibe em uma tabela interativa
st.dataframe(df_livros)

# ===== Atividade 2 =====
#Filtro de livros por ano de publicação, utilize o slider do streamlit.
years = pd.read_sql_query("SELECT MIN(ano) AS min_year, MAX(ano) AS max_year FROM livros", conn)
min_year = int(years.loc[0, 'min_year'])
max_year = int(years.loc[0, 'max_year'])
st.divider()
st.subheader("Livros publicados entre um intervalo de anos.")
ano_inicio, ano_fim = st.slider(
    "Selecione o intervalo de ano de publicação:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 3) Leitura e filtro dos dados
query = """
SELECT 
  l.id,
  l.titulo,
  a.nome      AS Autor,
  c.nome      AS Categoria,
  l.ano,
  l.quantidade_disponivel AS Disponíveis
FROM livros l
JOIN autores a ON l.autor_id = a.id
JOIN categorias c ON l.categoria_id = c.id
WHERE l.ano BETWEEN ? AND ?
ORDER BY l.ano
"""
df = pd.read_sql_query(query, conn, params=(ano_inicio, ano_fim))

# 4) Exibe o resultado filtrado
st.text(f"Livros publicados de {ano_inicio} até {ano_fim}")
st.dataframe(df)

st.divider()

# ===== Atividade 3 =====
# Quantidade total de livros, de empréstimos e devolvidos.
st.subheader("Quantidade total de livros, de empréstimos e devolvidos.")

# Total de livros é a soma da coluna "quantidade_disponivel"
query_total_livros = "SELECT SUM(quantidade_disponivel) AS total_livros FROM livros"
total_livros = pd.read_sql_query(query_total_livros, conn).iloc[0]['total_livros']

query_total_emprestimos = "SELECT COUNT(*) AS total_emprestimos FROM emprestimos"
total_emprestimos = pd.read_sql_query(query_total_emprestimos, conn).iloc[0]['total_emprestimos']

query_total_devolvidos = """
SELECT COUNT(*) AS total_devolvidos
FROM emprestimos
WHERE devolvido = 1
"""
total_devolvidos = pd.read_sql_query(query_total_devolvidos, conn).iloc[0]['total_devolvidos']

col1, col2, col3 = st.columns(3)
col1.metric("Total de livros", f"{total_livros}")
col2.metric("Total de empréstimos", f"{total_emprestimos}")
col3.metric("Total de livros devolvidos", f"{total_devolvidos}")

st.divider()
# ===== Atividade 4 =====
# Número de livros por categoria (agrupado).
st.subheader("Número de livros por categoria (agrupado).")
query_categoria = """
SELECT 
    c.nome AS Categoria,
    COUNT(l.id) AS Total_Livros
FROM categorias c
LEFT JOIN livros l ON c.id = l.categoria_id
GROUP BY c.id
"""
df_categoria = pd.read_sql_query(query_categoria, conn)
st.dataframe(df_categoria)

st.divider()

# ===== Atividade 5 =====
# Formulário para inserir um novo Livro
st.subheader("➕ Inserir novo Livro")
with st.form("form_novo_livro"):
    titulo = st.text_input("Título do Livro")
    
    # Busca autores disponíveis
    autores_df = pd.read_sql_query("SELECT id, nome FROM autores", conn)
    autor_option = st.selectbox("Autor", [""] + autores_df["nome"].tolist())
    if autor_option:
        autor_id = int(autores_df[autores_df["nome"] == autor_option]["id"].values[0])
    else:
        autor_id = None

    # Busca categorias disponíveis
    categorias_df = pd.read_sql_query("SELECT id, nome FROM categorias", conn)
    categoria_option = st.selectbox("Categoria", [""] + categorias_df["nome"].tolist())
    if categoria_option:
        categoria_id = int(categorias_df[categorias_df["nome"] == categoria_option]["id"].values[0])
    else:
        categoria_id = None

    ano = st.number_input("Ano de publicação", min_value=1, step=1)
    quantidade = st.number_input("Quantidade disponível", min_value=0, step=1)
    
    submit_livro = st.form_submit_button("Registrar Livro")
    
    if submit_livro:
        if titulo and autor_id and categoria_id and ano > 0 and quantidade >= 0:
            cursor.execute("""
                INSERT INTO livros (titulo, autor_id, categoria_id, ano, quantidade_disponivel)
                VALUES (?, ?, ?, ?, ?)
            """, (titulo, autor_id, categoria_id, int(ano), int(quantidade)))
            conn.commit()
            st.success(f"Livro '{titulo}' inserido com sucesso!")
            st.rerun()
        else:
            st.error("Preencha todos os campos corretamente para o livro.")


# Formulário para inserir um novo Empréstimo
st.subheader("➕ Inserir novo Empréstimo")
with st.form("form_novo_emprestimo"):
    # Busca livros disponíveis
    livros_df = pd.read_sql_query("SELECT id, titulo FROM livros", conn)
    if not livros_df.empty:
        livro_option = st.selectbox("Selecione o Livro", livros_df["titulo"].tolist())
        livro_id = int(livros_df[livros_df["titulo"] == livro_option]["id"].values[0])
    else:
        st.error("Nenhum livro disponível para empréstimo.")
        livro_id = None

    data_emprestimo = st.date_input("Data do Empréstimo")
    devolvido = st.checkbox("Já devolvido?", value=False)
    
    submit_emprestimo = st.form_submit_button("Registrar Empréstimo")
    
    if submit_emprestimo:
        if livro_id is not None:
            data_str = data_emprestimo.strftime("%Y-%m-%d")
            devolvido_int = 1 if devolvido else 0
            cursor.execute("""
                INSERT INTO emprestimos (livro_id, data_emprestimo, devolvido)
                VALUES (?, ?, ?)
            """, (livro_id, data_str, devolvido_int))
            conn.commit()
            st.success("Empréstimo registrado com sucesso!")
            st.rerun()
        else:
            st.error("Selecione um livro válido para registrar o empréstimo.")

st.divider()

# ===== Atividade 6 =====
# Formulário para editar um autor (alterar o nome)
st.subheader("✏️ Editar Autor")
with st.form("form_editar_autor"):
    # Busca autores disponíveis
    autores_df = pd.read_sql_query("SELECT id, nome FROM autores", conn)
    if not autores_df.empty:
        autor_option = st.selectbox("Selecione o Autor", autores_df["nome"].tolist())
        novo_nome = st.text_input("Novo Nome do Autor")
        submit_editar = st.form_submit_button("Atualizar Autor")
        if submit_editar:
            if novo_nome.strip():
                autor_id = int(autores_df[autores_df["nome"] == autor_option]["id"].values[0])
                cursor.execute("UPDATE autores SET nome = ? WHERE id = ?", (novo_nome.strip(), autor_id))
                conn.commit()
                st.success(f"Autor atualizado para '{novo_nome}' com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, insira um nome válido.")
    else:
        st.error("Nenhum autor disponível para editar.")

st.divider()
# ===== Atividade 7 =====
# Formulário para editar um livro (alterar titulo, nome, categoria,
# quantidade disponivel)
st.subheader("✏️ Editar Livro")
with st.form("form_editar_livro"):
    livros_df = pd.read_sql_query("SELECT id, titulo FROM livros", conn)
    if not livros_df.empty:
        livro_option = st.selectbox("Selecione o Livro", livros_df["titulo"].tolist())
        novo_titulo = st.text_input("Novo Título do Livro")
        
        autores_df = pd.read_sql_query("SELECT id, nome FROM autores", conn)
        autor_option = st.selectbox("Autor", [""] + autores_df["nome"].tolist())
        if autor_option:
            autor_id = int(autores_df[autores_df["nome"] == autor_option]["id"].values[0])
        else:
            autor_id = None

        categorias_df = pd.read_sql_query("SELECT id, nome FROM categorias", conn)
        categoria_option = st.selectbox("Categoria", [""] + categorias_df["nome"].tolist())
        if categoria_option:
            categoria_id = int(categorias_df[categorias_df["nome"] == categoria_option]["id"].values[0])
        else:
            categoria_id = None

        nova_quantidade = st.number_input("Nova Quantidade Disponível", min_value=0, step=1)
        
        submit_editar = st.form_submit_button("Atualizar Livro")
        
        if submit_editar:
            if novo_titulo.strip() and autor_id and categoria_id and nova_quantidade >= 0:
                livro_id = int(livros_df[livros_df["titulo"] == livro_option]["id"].values[0])
                cursor.execute("""
                    UPDATE livros 
                    SET titulo = ?, autor_id = ?, categoria_id = ?, quantidade_disponivel = ?
                    WHERE id = ?
                """, (novo_titulo.strip(), autor_id, categoria_id, int(nova_quantidade), livro_id))
                conn.commit()
                st.success(f"Livro '{novo_titulo}' atualizado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha todos os campos corretamente para o livro.")
    else:
        st.error("Nenhum livro disponível para editar.")

st.divider()
# ===== Atividade 8 =====

# Formulário para deletar um Livro
st.subheader("🗑️ Deletar Livro")
with st.form("form_deletar_livro"):
    livros_df = pd.read_sql_query("SELECT id, titulo FROM livros", conn)
    if not livros_df.empty:
        livro_option = st.selectbox("Selecione o Livro", livros_df["titulo"].tolist())
        submit_deletar_livro = st.form_submit_button("Deletar Livro")
        if submit_deletar_livro:
            livro_id = int(livros_df[livros_df["titulo"] == livro_option]["id"].values[0])
            cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
            conn.commit()
            st.success(f"Livro '{livro_option}' deletado com sucesso!")
            st.rerun()
    else:
        st.error("Nenhum livro disponível para deletar.")

st.divider()

# Formulário para deletar um Autor
st.subheader("🗑️ Deletar Autor")
with st.form("form_deletar_autor"):
    autores_df = pd.read_sql_query("SELECT id, nome FROM autores", conn)
    if not autores_df.empty:
        autor_option = st.selectbox("Selecione o Autor", autores_df["nome"].tolist())
        submit_deletar_autor = st.form_submit_button("Deletar Autor")
        if submit_deletar_autor:
            autor_id = int(autores_df[autores_df["nome"] == autor_option]["id"].values[0])
            cursor.execute("DELETE FROM autores WHERE id = ?", (autor_id,))
            conn.commit()
            st.success(f"Autor '{autor_option}' deletado com sucesso!")
            st.rerun()
    else:
        st.error("Nenhum autor disponível para deletar.")
