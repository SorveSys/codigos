# Script de captura de dados de componentes de hardware

import os
import sys
import time
from datetime import datetime

import psutil as ps
import mysql.connector
from dotenv import load_dotenv


# Lê as variáveis do arquivo .env
load_dotenv()

conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

# Lê e valida o ID do servidor
id_servidor = os.getenv("ID_SERVIDOR")

if id_servidor is None:
    print("ID_SERVIDOR não configurado no .env")
    conexao.close()
    sys.exit(1)

try:
    id_servidor = int(id_servidor)
except ValueError:
    print("ID_SERVIDOR deve ser um número inteiro.")
    conexao.close()
    sys.exit(1)

cursor = conexao.cursor()

if conexao.is_connected():
    print("\nConexão com o banco de dados bem-sucedida!")


def confirmar_servidor(id_servidor):
    # Verifica se o servidor existe no banco
    sql = "SELECT id FROM servidor WHERE id = %s"
    cursor.execute(sql, (id_servidor,))
    resultado = cursor.fetchone()

    return resultado is not None


def capturar_temperatura():
    # Verifica se o psutil disponibiliza a função
    if not hasattr(ps, "sensors_temperatures"):
        return None

    try:
        temperaturas = ps.sensors_temperatures()

        for sensores in temperaturas.values():
            for sensor in sensores:
                if sensor.current is not None:
                    return sensor.current

    except (AttributeError, OSError):
        return None

    return None


def capturardados():
    print("\nCapturas sendo realizadas...\n")

    percentual_cpu = ps.cpu_percent(interval=1)
    percentual_ram = ps.virtual_memory().percent

    # Usa o caminho adequado para o sistema operacional
    caminho_disco = "C:\\" if os.name == "nt" else "/"

    disco_uso_percentual = ps.disk_usage(caminho_disco).percent
    disco_disponivel_percentual = 100 - disco_uso_percentual

    cpu_temperatura = capturar_temperatura()

    print("Uso da CPU (%):", percentual_cpu)
    print("Uso da RAM (%):", percentual_ram)
    print("Uso do Disco (%):", disco_uso_percentual)
    print("Disponibilidade do Disco (%):", disco_disponivel_percentual)
    print("Temperatura da CPU (°C):", cpu_temperatura)

    return (
        percentual_cpu,
        percentual_ram,
        disco_uso_percentual,
        disco_disponivel_percentual,
        cpu_temperatura,
    )


def buscar_configuracao(id_servidor, nome_componente):
    # Busca a configuração do componente para o servidor
    sql = """
        SELECT cfg.id
        FROM config AS cfg
        JOIN servidor AS s
            ON s.id = cfg.fk_servidor
        JOIN componente AS c
            ON c.id = cfg.fk_componente
        WHERE s.id = %s
          AND c.nome = %s
    """

    cursor.execute(sql, (id_servidor, nome_componente))
    resultado = cursor.fetchone()

    if resultado is None:
        return None

    return resultado[0]


def buscar_metrica(tipo_metrica, nome_componente):
    # Busca o ID da métrica
    sql = """
        SELECT m.id
        FROM metrica AS m
        JOIN componente AS c
            ON c.id = m.fk_componente
        WHERE m.tipo = %s
          AND c.nome = %s
    """

    cursor.execute(sql, (tipo_metrica, nome_componente))
    resultado = cursor.fetchone()

    if resultado is None:
        return None

    return resultado[0]


def definir_limite(id_registro, tipo_metrica, valor):
    categoria = None
    descricao = None

    # Alertas de uso da CPU
    if tipo_metrica == "Porcentagem de Uso (%)":
        if valor > 85:
            categoria = "Critico"
            descricao = "Alerta: Uso da CPU Critico"
        elif valor > 70:
            categoria = "Moderado"
            descricao = "Alerta: Uso da CPU Moderado"

    # Alertas de uso da RAM
    elif tipo_metrica == "Uso da Memoria (%)":
        if valor > 90:
            categoria = "Critico"
            descricao = "Alerta: Uso da Memoria RAM Critico"
        elif valor > 75:
            categoria = "Moderado"
            descricao = "Alerta: Uso da Memoria RAM Moderado"

    # Alertas de espaço em uso no disco
    elif tipo_metrica == "Espaco em uso (%)":
        if valor > 90:
            categoria = "Critico"
            descricao = "Alerta: Uso do Disco Critico"
        elif valor > 75:
            categoria = "Moderado"
            descricao = "Alerta: Uso do Disco Moderado"

    # Alertas de espaço disponível no disco
    elif tipo_metrica == "Espaco disponivel (%)":
        if valor < 10:
            categoria = "Critico"
            descricao = "Alerta: Espaco livre do Disco Critico"
        elif valor < 25:
            categoria = "Moderado"
            descricao = "Alerta: Espaco livre do Disco Moderado"

    # Alertas de temperatura da CPU
    elif tipo_metrica == "Temperatura (Celsius)":
        if valor > 80:
            categoria = "Critico"
            descricao = "Alerta: Temperatura da CPU Critico"
        elif valor > 70:
            categoria = "Moderado"
            descricao = "Alerta: Temperatura da CPU Moderado"

    # Insere e exibe somente alertas moderados ou críticos
    if categoria is not None:
        sql = """
            INSERT INTO alerta (categoria, descricao, fk_registro)
            VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (categoria, descricao, id_registro))

        print(f"[{categoria}] {descricao} | Valor: {valor}")


def inserir_dados(id_servidor, dados):
    (
        percentual_cpu,
        percentual_ram,
        disco_uso_percentual,
        disco_disponivel_percentual,
        cpu_temperatura,
    ) = dados

    sql = """
        INSERT INTO registro_monitoramento
            (fk_config, fk_metrica, valor, dt_hora)
        VALUES (%s, %s, %s, %s)
    """

    # Dados da CPU - uso percentual
    id_config = buscar_configuracao(id_servidor, "CPU")
    tipo_metrica = "Porcentagem de Uso (%)"
    id_metrica = buscar_metrica(tipo_metrica, "CPU")

    if id_config is not None and id_metrica is not None:
        cursor.execute(
            sql, (id_config, id_metrica, percentual_cpu, datetime.now())
        )
        id_registro = cursor.lastrowid
        definir_limite(id_registro, tipo_metrica, percentual_cpu)

    # Dados da RAM - uso percentual
    id_config = buscar_configuracao(id_servidor, "Memoria RAM")
    tipo_metrica = "Uso da Memoria (%)"
    id_metrica = buscar_metrica(tipo_metrica, "Memoria RAM")

    if id_config is not None and id_metrica is not None:
        cursor.execute(
            sql, (id_config, id_metrica, percentual_ram, datetime.now())
        )
        id_registro = cursor.lastrowid
        definir_limite(id_registro, tipo_metrica, percentual_ram)

    # Dados do disco - espaço em uso
    id_config = buscar_configuracao(id_servidor, "Disco Rigido")
    tipo_metrica = "Espaco em uso (%)"
    id_metrica = buscar_metrica(tipo_metrica, "Disco Rigido")

    if id_config is not None and id_metrica is not None:
        cursor.execute(
            sql, (id_config, id_metrica, disco_uso_percentual, datetime.now())
        )
        id_registro = cursor.lastrowid
        definir_limite(id_registro, tipo_metrica, disco_uso_percentual)

    # Dados do disco - espaço disponível
    id_config = buscar_configuracao(id_servidor, "Disco Rigido")
    tipo_metrica = "Espaco disponivel (%)"
    id_metrica = buscar_metrica(tipo_metrica, "Disco Rigido")

    if id_config is not None and id_metrica is not None:
        cursor.execute(
            sql,
            (id_config, id_metrica, disco_disponivel_percentual, datetime.now()),
        )
        id_registro = cursor.lastrowid
        definir_limite(id_registro, tipo_metrica, disco_disponivel_percentual)

    # Temperatura: insere somente se houver leitura disponível
    if cpu_temperatura is not None:
        id_config = buscar_configuracao(id_servidor, "CPU")
        tipo_metrica = "Temperatura (Celsius)"
        id_metrica = buscar_metrica(tipo_metrica, "CPU")

        if id_config is not None and id_metrica is not None:
            cursor.execute(
                sql, (id_config, id_metrica, cpu_temperatura, datetime.now())
            )
            id_registro = cursor.lastrowid
            definir_limite(id_registro, tipo_metrica, cpu_temperatura)

    # Confirma registros e alertas juntos
    conexao.commit()
    print("Dados inseridos com sucesso!")


# Confere uma única vez se o servidor existe no banco
try:
    if not confirmar_servidor(id_servidor):
        print("Servidor não encontrado no banco.")
        sys.exit(1)

    while True:
        try:
            dados = capturardados()
            inserir_dados(id_servidor, dados)
            print("Dados gravados!")

        except Exception as erro:
            print("Erro durante o monitoramento:", erro)
            conexao.rollback()

        time.sleep(30)

except KeyboardInterrupt:
    print("\nMonitoramento encerrado.")

finally:
    cursor.close()
    conexao.close()