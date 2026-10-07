# Novo script de captura de dados de componentes de hardware
import os
from dotenv import load_dotenv
import sys
import psutil as ps
import mysql.connector
import time


load_dotenv() # lê o .env

conexao = mysql.connector.connect( # faz a conexão com BD
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

id_servidor = os.getenv("ID_SERVIDOR") # lê o id do servidor no .env 

if id_servidor is None:  # verifica se o id veio como none
    print("ID_SERVIDOR não configurado no .env")
    sys.exit(1) # encerra o script: sem id, não dá para gravar
id_servidor = int(id_servidor) # transforma id em número

cursor = conexao.cursor() # o cursor é quem envia os comandos SQL ao banco

if conexao.is_connected(): # verifica se foi possível fazer a conexão
    print("\nConexão com o banco de dados bem sucedida!")


def capturardados(): # função para capturar dados do hardware
    print("\n Capturas sendo realizadas...\n")

    percentual_cpu = ps.cpu_percent(interval=1)
    percentual_ram = ps.virtual_memory().percent
    disco_uso_percentual = ps.disk_usage("C:\\").percent
    disco_disponivel_percentual = 100 - disco_uso_percentual
    cpu_temperatura = None
    print("Uso da CPU (%):",percentual_cpu)
    print("Uso da RAM (%):", percentual_ram)
    print("Uso do Disco (%):",disco_uso_percentual)
    print("Disponibilizade do Disco (%):",disco_disponivel_percentual)
    print("Temperatura CPU (C° - None, se o S.O for Windows): ", cpu_temperatura)

    return percentual_cpu, percentual_ram, disco_uso_percentual, disco_disponivel_percentual, cpu_temperatura


def confirmar_servidor(id_servidor): # função para confirmar o servidor monitorado
     # procura no banco um servidor com esse id
    sql = "SELECT id_servidor FROM servidores WHERE id_servidor = %s"
    cursor.execute(sql,(id_servidor,))
    resultado = cursor.fetchone() # devolve a linha encontrada ou None se não existir

    if resultado is None:
        return False
    return True

def inserir_dados(id_servidor, dados): # função para inserir os dados no banco
    sql = "INSERT INTO componentes_hardware (" \
    "data_hora," \
    "cpu_uso_percent," \
    "cpu_temperatura," \
    "ram_percent," \
    "disco_uso_percent," \
    "disco_disponivel_percent," \
    "fk_servidor) VALUES (NOW(), %s,%s,%s,%s,%s,%s)"

    cpu, ram, disco_uso, disco_disponivel, temperatura = dados

    cursor.execute( 
        sql,
        (cpu, temperatura, ram, disco_uso, disco_disponivel, id_servidor)
    )
    conexao.commit()

    time.sleep(30)

# confere uma única vez, antes do loop, se o servidor existe no banco
if not confirmar_servidor(id_servidor):
    print("Servidor não encontrado no banco.")
    sys.exit(1) # encerra se não houver servidor 

try:
    while True:
        try:
            dados = capturardados()

            inserir_dados(id_servidor, dados)

            print("Dados gravados!")
        except Exception as erro:
            # mostra o erro mas o loop continua

            time.sleep(30)
except KeyboardInterrupt: 
    print("\nMonitoramento encerrado.")

finally: # fecha cursor e conhexão após rodar o script
    cursor.close()
    conexao.close()
