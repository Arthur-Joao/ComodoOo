import sqlite3

NOME_BANCO = "ranking.db"

def inicializar_banco():
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pontos INTEGER NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def salvar_pontuacao(nome, pontos):
    if not nome.strip():
        nome = "Anonimo"
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ranking (nome, pontos) VALUES (?, ?)", (nome, pontos))
    conn.commit()
    conn.close()

def obter_top_scores(limit=5):
    conn = sqlite3.connect(NOME_BANCO)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, pontos FROM ranking 
        ORDER BY pontos DESC 
        LIMIT ?
    """, (limit,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados