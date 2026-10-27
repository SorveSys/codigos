import os
import csv
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

cursor = conexao.cursor()

sql = """
SELECT
    r.dt_hora,
    s.id   AS id_servidor,
    s.tipo AS tipo_servidor,
    e.id   AS id_empresa,
    e.nome_fantasia AS empresa,
    c.nome AS componente,
    m.tipo AS metrica,
    r.valor,
    a.categoria AS alerta
FROM registro_monitoramento AS r
JOIN config      AS cfg ON cfg.id = r.fk_config
JOIN servidor    AS s   ON s.id   = cfg.fk_servidor
JOIN empresa     AS e   ON e.id   = s.fk_empresa
JOIN componente  AS c   ON c.id   = cfg.fk_componente
JOIN metrica     AS m   ON m.id   = r.fk_metrica
LEFT JOIN alerta AS a   ON a.fk_registro = r.id
ORDER BY r.dt_hora
"""

cursor.execute(sql)

pasta = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(pasta, "dados_monitoramento.csv")

with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow([col[0] for col in cursor.description])
    escritor.writerows(cursor.fetchall())

cursor.close()
conexao.close()
print("CSV gerado em:", caminho)