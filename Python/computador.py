import psutil as p
import mysql.connector
from rich import print
import speedtest
from datetime import datetime


conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pedro2302",
    database="SorveSys"
)

cursor = conexao.cursor()

if conexao.is_connected():
    print("Conexão bem sucedida")

def usuario(): 
    while True:
        recurso = input("Digite qual recurso você quer \n"
        "1- CPU \n"
        "2- Memória \n"
        "3- Disco \n"
        "4- Qualidade da internet\n"
        "5- Sair\n"
        )
        if recurso.lower() == "cpu" or recurso == "1":
            cpu()

        elif recurso.lower() == "disco" or recurso == "3":
            disco()

        elif recurso.lower() == "memória" or recurso.lower() == "memoria" or recurso == "2":
            memo()

        elif recurso.lower() == "qualidade da internet" or recurso.lower() == "internet" or recurso == "4":
            internet()

        elif recurso.lower() == "sair" or recurso == "5":
            return

        else:
            print("[bold red]Recurso inválido![/bold red]")


def cpu():
    while True:

        cpuInfo = input(
            "Digite o que você quer saber da CPU \n"
            "1- CPU Times \n"
            "2- Uso da CPU \n"
            "3- CPUs lógicas \n"
            "4- sair\n"
        )

        if cpuInfo.lower() == "cpu times" or cpuInfo.lower() == "cpu time" or cpuInfo == "1":

            times = p.cpu_times(percpu=False)
            uso_cpu = p.cpu_percent(interval=1)
            cpus_logicas = p.cpu_count(logical=True)

            print(times)

            sql = """
                INSERT INTO leitura 
                (valor, data_hora, configuracao_maquina_fk, configuracao_componente_fk, configuracao_status_monitor_fk, metrica_fk)
                VALUES (%s, NOW(), 1, 1, 1, 1)
            """

            valores = (times.user + times.system,)
            cursor.execute(sql, valores)
            conexao.commit()

        elif cpuInfo.lower() == "uso da cpu" or cpuInfo == "2":

            times = p.cpu_times(percpu=False)
            uso_cpu = p.cpu_percent(interval=1)
            cpus_logicas = p.cpu_count(logical=True)

            print(f"[bold blue] CPU = {uso_cpu}% [/bold blue]")

            sql = """
                INSERT INTO leitura 
                (valor, data_hora, configuracao_maquina_fk, configuracao_componente_fk, configuracao_status_monitor_fk, metrica_fk)
                VALUES (%s, NOW(), 1, 1, 1, 1)
            """

            valores = (uso_cpu,)
            cursor.execute(sql, valores)
            conexao.commit()

        elif (cpuInfo.lower() == "cpus logicas" or cpuInfo.lower() == "cpus lógicas" or cpuInfo == "3"):

            times = p.cpu_times(percpu=False)
            uso_cpu = p.cpu_percent(interval=1)
            cpus_logicas = p.cpu_count(logical=True)

            print(f"[bold blue] CPUs Lógicas = {cpus_logicas} [/bold blue]")

            sql = """
                INSERT INTO leitura 
                (valor, data_hora, configuracao_maquina_fk, configuracao_componente_fk, configuracao_status_monitor_fk, metrica_fk)
                VALUES (%s, NOW(), 1, 1, 1, 1)
            """

            valores = (cpus_logicas,)

            cursor.execute(sql, valores)
            conexao.commit()

        elif cpuInfo.lower() == "sair" or cpuInfo == "4":
            return

        else:
            print("[bold red]Opção inválida![/bold red]")


def disco():

    while True:

        discoInfo = input("Qual informação do disco você quer acessar \n"
        "1- Disco Total \n"
        "2- Disco Usado \n"
        "3- Disco Livre \n"
        "4- Uso do disco \n"
        " 5- sair \n")

        if discoInfo.lower() == "sair" or discoInfo == "5":
            return

        elif (
            discoInfo.lower() == "disco total" or discoInfo.lower() == "disco usado"
            or discoInfo.lower() == "disco livre" or discoInfo.lower() == "uso do disco" or discoInfo 
        ):

            disk = p.disk_usage("C:\\")

            disco_total = disk.total / (1024 ** 3)
            disco_usado = disk.used / (1024 ** 3)
            disco_livre = disk.free / (1024 ** 3)
            uso_disco = disk.percent

            if discoInfo.lower() == "disco total" or discoInfo == "1":
                print(f"[bold blue]Disco Total = {disco_total:.2f} GB [/bold blue]")
                valor_inserir = disco_total

            elif discoInfo.lower() == "disco usado" or discoInfo == "2":
                print(f"[bold blue]Disco Usado = {disco_usado:.2f} GB [/bold blue]")
                valor_inserir = disco_usado

            elif discoInfo.lower() == "disco livre" or discoInfo == "3":
                print(f"[bold blue]Disco Livre = {disco_livre:.2f} GB [/bold blue]")
                valor_inserir = disco_livre

            elif discoInfo.lower() == "uso do disco" or discoInfo == "4":
                print(f"[bold blue]Uso do Disco = {uso_disco}%[/bold blue]")
                valor_inserir = uso_disco

            sql = """
                INSERT INTO leitura 
                (valor, data_hora, configuracao_maquina_fk, configuracao_componente_fk, configuracao_status_monitor_fk, metrica_fk)
                VALUES (%s, NOW(), 1, 3, 1, 2)
            """

            valores = (valor_inserir,)

            cursor.execute(sql, valores)
            conexao.commit()

        else:
            print("[bold red]Opção inválida![bold red]")


def memo():

    while True:

        memoriaInfo = input("Qual informação da memória você quer acessar \n"
        "1- RAM Total \n"
        "2- RAM Disponível \n"
        "3- RAM Usada \n"
        "4- RAM Livre \n"
        "5- Uso da RAM \n"
        "6- sair\n")

        if memoriaInfo.lower() == "sair" or memoriaInfo == "6":
            return

        elif (
            memoriaInfo.lower() == "ram total" or memoriaInfo.lower() == "ram disponivel"
            or memoriaInfo.lower() == "ram disponível" or memoriaInfo.lower() == "ram usada"
            or memoriaInfo.lower() == "ram livre" or memoriaInfo.lower() == "uso da ram" or memoriaInfo == "1"
            or memoriaInfo == "2" or memoriaInfo == "3" or memoriaInfo == "4" or memoriaInfo == "5" or memoriaInfo == "6"
        ):

            memoria = p.virtual_memory()

            memoria_total = memoria.total / (1024 ** 3)
            ram_disponivel = memoria.available / (1024 ** 3)
            ram_usada = memoria.used / (1024 ** 3)
            memoria_livre = memoria.free / (1024 ** 3)
            uso_ram = memoria.percent

            if memoriaInfo.lower() == "ram total" or memoriaInfo == "1":
                print(f"[bold blue]RAM Total = {memoria_total:.2f} GB[/bold blue]")
                valor_inserir = memoria_total

            elif (
                memoriaInfo.lower() == "ram disponivel"
                or memoriaInfo.lower() == "ram disponível" or memoriaInfo == "2"
            ):
                print(f"[bold blue]RAM Disponível = {ram_disponivel:.2f} GB[/bold blue]")
                valor_inserir = ram_disponivel

            elif memoriaInfo.lower() == "ram usada" or memoriaInfo == "3":
                print(f"[bold blue]RAM Usada = {ram_usada:.2f} GB[/bold blue]")
                valor_inserir = ram_usada

            elif memoriaInfo.lower() == "ram livre" or memoriaInfo == "4":
                print(f"[bold blue]RAM Livre = {memoria_livre:.2f} GB[/bold blue]")
                valor_inserir = memoria_livre

            elif memoriaInfo.lower() == "uso da ram" or memoriaInfo == "5":
                print(f"[bold blue]Uso da RAM = {uso_ram}%[/bold blue]")
                valor_inserir = uso_ram

            sql = """
                INSERT INTO leitura 
                (valor, data_hora, configuracao_maquina_fk, configuracao_componente_fk, configuracao_status_monitor_fk, metrica_fk)
                VALUES (%s, NOW(), 1, 2, 1, 2)
            """

            valores = (valor_inserir,)

            cursor.execute(sql, valores)
            conexao.commit()

        else:
            print("[bold red]Opção inválida![/bold red]")

def internet():
    print("Iniciando o teste de velocidade... Aguarde um momento.")

    st = speedtest.Speedtest()
    st.get_best_server()

    print("Testando o Ping...")
    ping = st.results.ping

    print("Testando a velocidade de Download...")
    download_speed = st.download() / 1_000_000

    print("Testando a velocidade de Upload...")
    upload_speed = st.upload() / 1_000_000

    print(f"")
    print(f"[bold green]Ping: {ping:.2f} ms[/bold green]")
    print(f"[bold green]Download: {download_speed:.2f} Mbps[/bold green]")
    print(f"[bold green]Upload: {upload_speed:.2f} Mbps[/bold green]")
    print(f"")

    sql = """
        INSERT INTO leitura 
        (valor, data_hora, configuracao_maquina_fk, configuracao_componente_fk, configuracao_status_monitor_fk, metrica_fk)
        VALUES (%s, NOW(), 1, 4, 1, 3)
    """

    valores = (download_speed,)

    cursor.execute(sql, valores)
    conexao.commit()


def banco():
    bank = input("Qual dado do banco você quer \n"
    "1- CPU \n"
    "2- Memória \n"
    "3- Disco \n"
    "4- Internet \n"
    "5- sair\n")
    if bank.lower() == "cpu" or bank == "1":
        cursor.execute("SELECT id, valor, data_hora FROM leitura WHERE configuracao_componente_fk = 1")
        resultados = cursor.fetchall()

        for produto in resultados:
            print(f"\nID: {produto[0]}")
            print(f"Valor registrado: {produto[1]}")
            print(f"Data/Hora: {produto[2]}")

    elif bank.lower() == "memoria" or bank.lower() == "memória" or bank == "2":
        cursor.execute("SELECT id, valor, data_hora FROM leitura WHERE configuracao_componente_fk = 2")
        resultados = cursor.fetchall()

        for produto in resultados:
            print(f"\nID: {produto[0]}")
            print(f"Valor registrado: {produto[1]}")
            print(f"Data/Hora: {produto[2]}")

    elif bank.lower() == "disco" or bank == "3":
        cursor.execute("SELECT id, valor, data_hora FROM leitura WHERE configuracao_componente_fk = 3")
        resultados = cursor.fetchall()

        for produto in resultados:
            print(f"\nID: {produto[0]}")
            print(f"Valor registrado: {produto[1]}")
            print(f"Data/Hora: {produto[2]}")

    elif bank.lower() == "internet" or bank == "4":
            cursor.execute("SELECT id, valor, data_hora FROM leitura WHERE configuracao_componente_fk = 4")
            resultados = cursor.fetchall()

            for produto in resultados:
                print(f"\nID: {produto[0]}")
                print(f"Valor registrado: {produto[1]}")
                print(f"Data/Hora: {produto[2]}")

    elif bank.lower() == "sair" or bank == "5":
        return
    else:
        banco()

def deletar():
    delt = input("Qual registro você quer apagar? \n "
    "1- CPU \n "
    "2- Memória \n"
    "3- Disco \n"
    "4- sair\n")

    if delt.lower() == "memoria" or delt.lower() == "memória " or delt == "2":
        cursor.execute("DELETE FROM leitura WHERE configuracao_componente_fk = 2 ORDER BY id DESC LIMIT 5;")
        conexao.commit()

        print("[bold green]Registros apagados com sucesso![/bold green]")
        cursor.execute("SELECT * FROM leitura WHERE configuracao_componente_fk = 2")
        resultados = cursor.fetchall()
        for registro in resultados:
            print(registro)    


    elif delt.lower() == "cpu" or delt == "1":
        cursor.execute("DELETE FROM leitura WHERE configuracao_componente_fk = 1 ORDER BY id DESC LIMIT 5;")
        conexao.commit()

        print("[bold green]Registros apagados com sucesso![/bold green]")

        cursor.execute("SELECT * FROM leitura WHERE configuracao_componente_fk = 1")
        resultados = cursor.fetchall()
        for registro in resultados:
            print(registro)       

    elif delt.lower() == "disco" or delt == "3":
        cursor.execute("DELETE FROM leitura WHERE configuracao_componente_fk = 3 ORDER BY id DESC LIMIT 5;")
        conexao.commit()

        print("Registros apagados com sucesso!")   
        cursor.execute("SELECT * FROM leitura WHERE configuracao_componente_fk = 3")
        resultados = cursor.fetchall()
        for registro in resultados:
            print(registro) 

    elif delt.lower() == "sair" or delt == "4":
        return

    deletar()

def atualizar():
    atual = input("Qual registro você quer atualizar? \n"
    "1- CPU \n"
    "2- Memória \n"
    "3- Disco \n"
    "4- sair \n")

    if atual.lower() == "memoria" or atual.lower() == "memória " or atual == "1":
        cursor.execute("UPDATE leitura SET data_hora = NOW() WHERE id IN (SELECT id FROM (SELECT id FROM leitura WHERE configuracao_componente_fk = 2 ORDER BY id DESC LIMIT 3) AS ultimos);")
        conexao.commit()
        cursor.execute("SELECT * FROM leitura WHERE configuracao_componente_fk = 2")
        resultados = cursor.fetchall()
        for registro in resultados:
            print(registro)

        print("[bold green]Registros atualizados com sucesso![/bold green]")

    elif atual.lower() == "cpu" or atual == "2":
        cursor.execute("UPDATE leitura SET data_hora = NOW() WHERE id IN (SELECT id FROM (SELECT id FROM leitura WHERE configuracao_componente_fk = 1 ORDER BY id DESC LIMIT 3) AS ultimos);")
        conexao.commit()

        print("[bold green]Registros atualizados com sucesso![/bold green]")
        cursor.execute("SELECT * FROM leitura WHERE configuracao_componente_fk = 1")
        resultados = cursor.fetchall()
        for registro in resultados:
            print(registro)

    elif atual.lower() == "disco" or atual == "3":
        cursor.execute("UPDATE leitura SET data_hora = NOW() WHERE id IN (SELECT id FROM (SELECT id FROM leitura WHERE configuracao_componente_fk = 3 ORDER BY id DESC LIMIT 3) AS ultimos);")
        conexao.commit()
        print("[bold green]Registros atualizados com sucesso![/bold green]")   

        cursor.execute("SELECT * FROM leitura WHERE configuracao_componente_fk = 3")
        resultados = cursor.fetchall()
        for registro in resultados:
            print(registro)


    elif atual.lower() == "sair" or atual == "4":
        return    
    atualizar()

def decisao():
    while True:
        dec = input(
            "Quais dados você quer \n"
            "1- Informações do PC \n"
            "2- Banco de Dados \n"
            "3- Deletar Registros \n"
            "4- Atualizar Registros \n"
            "5- sair\n" 
        )

        if dec.lower() == "banco de dados" or dec == "2":
            banco()

        elif dec.lower() in [
            "informações do pc",
            "informaçoes do pc",
            "informacoes do pc",
            "1"
        ]:
            usuario()
        elif dec.lower() in [
            "deletar registros",
            "daletar registro",
            "deleta resgistro",
            "3"
        ]:
            deletar() 
        elif dec.lower() in [
            "atualiza registro",
            "atualizar registros",
            "atualiza registros",
            "atualizar registro",
            "4"
        ]:
            atualizar()

        elif dec.lower() == "sair" or dec == "5":
            print(" Programa encerrado!")
            break

        else:
            print("Opção inválida!")


decisao()

cursor.close()
conexao.close()