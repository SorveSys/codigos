
import psutil as p
import mysql.connector
from rich import print
import speedtest


conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sorvesys"
)

cursor = conexao.cursor()

if conexao.is_connected():
    print("Conexão bem sucedida")


def registrar_leitura(tipo, nome_metrica, valor):
    sql = """
        SELECT configuracao.id, componente_metrica.id
        FROM configuracao
        INNER JOIN componente
            ON configuracao.componente_fk = componente.id
        INNER JOIN tipo_componente
            ON componente.tipo_componente_fk = tipo_componente.id
        INNER JOIN componente_metrica
            ON componente_metrica.componente_fk = componente.id
        INNER JOIN metrica
            ON componente_metrica.metrica_fk = metrica.id
        WHERE LOWER(tipo_componente.tipo) = LOWER(%s)
        AND LOWER(metrica.nome) = LOWER(%s)
        ORDER BY configuracao.id
        LIMIT 1
    """

    cursor.execute(sql, (tipo, nome_metrica))
    resultado = cursor.fetchone()

    if resultado is None:
        print(
            f"[yellow]Não foi possível registrar: "
            f"falta configurar {tipo} / {nome_metrica} no banco.[/yellow]"
        )
        return

    configuracao_id = resultado[0]
    componente_metrica_id = resultado[1]

    sql = """
        INSERT INTO leitura
            (valor, configuracao_fk, componente_metrica_fk)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        sql,
        (valor, configuracao_id, componente_metrica_id)
    )
    conexao.commit()

    print("[green]Leitura registrada no banco de dados![/green]")


def usuario():
    while True:
        recurso = input(
            "\nDigite qual recurso você quer\n"
            "1- CPU\n"
            "2- Memória\n"
            "3- Disco\n"
            "4- Qualidade da internet\n"
            "5- Capturar todos os dados\n"
            "6- Sair\n")

        if recurso.lower() == "cpu" or recurso == "1":
            cpu()
        elif recurso.lower() in ["memória", "memoria"] or recurso == "2":
            memo()
        elif recurso.lower() == "disco" or recurso == "3":
            disco()
        elif recurso.lower() in ["qualidade da internet", "internet"] or recurso == "4":
            internet()
        elif recurso.lower() in ["capturar todos", "capturar todos os dados"] or recurso == "5":
            capturar_todos()
        elif recurso.lower() == "sair" or recurso == "6":
            return
        else:
            print("[red]Recurso inválido![/red]")
def cpu():
    while True:
        cpu_info = input(
            "\nDigite o que você quer saber da CPU\n"
            "1- CPU Times\n"
            "2- Uso da CPU\n"
            "3- CPUs lógicas\n"
            "4- Sair\n"
        )

        if cpu_info.lower() in ["cpu times", "cpu time"] or cpu_info == "1":
            times = p.cpu_times(percpu=False)
            valor = times.user + times.system

            print(f"Tempo de CPU = {valor:.2f} segundos")

            registrar_leitura("CPU", "Tempo CPU", valor)

        elif cpu_info.lower() == "uso da cpu" or cpu_info == "2":
            valor = p.cpu_percent(interval=1)

            print(f"Uso da CPU = {valor}%")
            registrar_leitura("CPU", "Porcentagem", valor)

        elif cpu_info.lower() in ["cpus logicas", "cpus lógicas"] or cpu_info == "3":
            valor = p.cpu_count(logical=True)

            print(f"CPUs lógicas = {valor}")

            registrar_leitura("CPU", "CPUs lógicas", valor)

        elif cpu_info.lower() == "sair" or cpu_info == "4":
            return

        else:
            print("[red]Opção inválida![/red]")


def disco():
    while True:
        disco_info = input(
            "\nQual informação do disco você quer acessar?\n"
            "1- Disco total\n"
            "2- Disco usado\n"
            "3- Disco livre\n"
            "4- Uso do disco\n"
            "5- Sair\n"
        )

        if disco_info.lower() == "sair" or disco_info == "5":
            return

        elif disco_info in ["1", "2", "3", "4"] or disco_info.lower() in ["disco total", "disco usado", "disco livre", "uso do disco"]:
            disk = p.disk_usage("/")

            disco_total = disk.total / (1024 ** 3)
            disco_usado = disk.used / (1024 ** 3)
            disco_livre = disk.free / (1024 ** 3)
            uso_disco = disk.percent

            if disco_info.lower() == "disco total" or disco_info == "1":
                nome_metrica = "Disco Total"
                valor = disco_total
                print(f"Disco total = {valor:.2f} GB")

            elif disco_info.lower() == "disco usado" or disco_info == "2":
                nome_metrica = "Disco Usado"
                valor = disco_usado
                print(f"Disco usado = {valor:.2f} GB")

            elif disco_info.lower() == "disco livre" or disco_info == "3":
                nome_metrica = "Disco Livre"
                valor = disco_livre
                print(f"Disco livre = {valor:.2f} GB")

            elif disco_info.lower() == "uso do disco" or disco_info == "4":
                nome_metrica = "Uso do Disco"
                valor = uso_disco
                print(f"Uso do disco = {valor}%")

            registrar_leitura("Disco", nome_metrica, valor)

        else:
            print("[red]Opção inválida![/red]")


def memo():
    while True:
        memoria_info = input(
            "\nQual informação da memória você quer acessar?\n"
            "1- RAM total\n"
            "2- RAM disponível\n"
            "3- RAM usada\n"
            "4- RAM livre\n"
            "5- Uso da RAM\n"
            "6- Sair\n"
        )

        if memoria_info.lower() == "sair" or memoria_info == "6":
            return

        elif memoria_info in ["1", "2", "3", "4", "5"] or memoria_info.lower() in ["ram total", "ram disponível", "ram disponivel", "ram usada", "ram livre", "uso da ram"]:
            memoria = p.virtual_memory()

            memoria_total = memoria.total / (1024 ** 3)
            ram_disponivel = memoria.available / (1024 ** 3)
            ram_usada = memoria.used / (1024 ** 3)
            memoria_livre = memoria.free / (1024 ** 3)
            uso_ram = memoria.percent

            if memoria_info.lower() == "ram total" or memoria_info == "1":
                nome_metrica = "RAM Total"
                valor = memoria_total
                print(f"RAM total = {valor:.2f} GB")

            elif memoria_info.lower() in [
                "ram disponível", "ram disponivel"
            ] or memoria_info == "2":
                nome_metrica = "RAM Disponível"
                valor = ram_disponivel
                print(f"RAM disponível = {valor:.2f} GB")

            elif memoria_info.lower() == "ram usada" or memoria_info == "3":
                nome_metrica = "RAM Usada"
                valor = ram_usada
                print(f"RAM usada = {valor:.2f} GB")

            elif memoria_info.lower() == "ram livre" or memoria_info == "4":
                nome_metrica = "RAM Livre"
                valor = memoria_livre
                print(f"RAM livre = {valor:.2f} GB")

            elif memoria_info.lower() == "uso da ram" or memoria_info == "5":
                nome_metrica = "Uso da RAM"
                valor = uso_ram
                print(f"Uso da RAM = {valor}%")

            registrar_leitura("Memória", nome_metrica, valor)

        else:
            print("[red]Opção inválida![/red]")


def internet():
    print("Iniciando o teste de velocidade... Aguarde um momento.")

    st = speedtest.Speedtest()
    st.get_best_server()

    print("Testando o Ping...")
    ping = round(st.results.ping, 2)

    print("Testando a velocidade de Download...")
    download_speed = round(st.download() / 1_000_000, 2)

    print("Testando a velocidade de Upload...")
    upload_speed = round(st.upload() / 1_000_000, 2)

    print(f"\nPing: {ping:.2f} ms")
    print(f"Download: {download_speed:.2f} Mbps")
    print(f"Upload: {upload_speed:.2f} Mbps\n")

    registrar_leitura("Rede", "Latencia", ping)
    registrar_leitura("Rede", "Velocidade", download_speed)
    registrar_leitura("Rede", "Velocidade", upload_speed)


def banco():
    while True:
        bank = input(
            "\nQual dado do banco você quer consultar?\n"
            "1- CPU\n"
            "2- Memória\n"
            "3- Disco\n"
            "4- Internet\n"
            "5- Sair\n"
        )

        tipos = {
            "1": "CPU",
            "2": "Memória",
            "3": "Disco",
            "4": "Rede"
        }

        if bank.lower() == "sair" or bank == "5":
            return

        if bank.lower() in ["cpu", "memória", "memoria", "disco", "internet", "rede"]:
            if bank.lower() == "cpu":
                tipo = "CPU"
            elif bank.lower() in ["memória", "memoria"]:
                tipo = "Memória"
            elif bank.lower() == "disco":
                tipo = "Disco"
            else:
                tipo = "Rede"
        elif bank in tipos:
            tipo = tipos[bank]
        else:
            print("[red]Opção inválida![/red]")
            continue

        sql = """
            SELECT leitura.id, metrica.nome, leitura.valor,
                   metrica.unidade_medida, leitura.data_hora
            FROM leitura
            INNER JOIN configuracao
                ON leitura.configuracao_fk = configuracao.id
            INNER JOIN componente
                ON configuracao.componente_fk = componente.id
            INNER JOIN tipo_componente
                ON componente.tipo_componente_fk = tipo_componente.id
            INNER JOIN componente_metrica
                ON leitura.componente_metrica_fk = componente_metrica.id
            INNER JOIN metrica
                ON componente_metrica.metrica_fk = metrica.id
            WHERE LOWER(tipo_componente.tipo) = LOWER(%s)
            ORDER BY leitura.data_hora DESC
        """

        cursor.execute(sql, (tipo,))
        resultados = cursor.fetchall()

        if not resultados:
            print("[yellow]Nenhuma leitura encontrada.[/yellow]")

        for registro in resultados:
            print(f"\nID: {registro[0]}")
            print(f"Métrica: {registro[1]}")
            print(f"Valor: {registro[2]} {registro[3]}")
            print(f"Data/Hora: {registro[4]}")


def deletar():
    while True:
        delt = input(
            "\nQual registro você quer apagar?\n"
            "1- CPU\n"
            "2- Memória\n"
            "3- Disco\n"
            "4- Internet\n"
            "5- Sair\n"
        )

        tipos = {
            "1": "CPU",
            "2": "Memória",
            "3": "Disco",
            "4": "Rede"
        }

        if delt.lower() == "sair" or delt == "5":
            return

        if delt.lower() in ["cpu", "memória", "memoria", "disco", "internet", "rede"]:
            if delt.lower() == "cpu":
                tipo = "CPU"
            elif delt.lower() in ["memória", "memoria"]:
                tipo = "Memória"
            elif delt.lower() == "disco":
                tipo = "Disco"
            else:
                tipo = "Rede"
        elif delt in tipos:
            tipo = tipos[delt]
        else:
            print("[red]Opção inválida![/red]")
            continue

        sql = """
            DELETE FROM leitura
            WHERE id IN (
                SELECT id FROM (
                    SELECT leitura.id
                    FROM leitura
                    INNER JOIN configuracao
                        ON leitura.configuracao_fk = configuracao.id
                    INNER JOIN componente
                        ON configuracao.componente_fk = componente.id
                    INNER JOIN tipo_componente
                        ON componente.tipo_componente_fk = tipo_componente.id
                    WHERE LOWER(tipo_componente.tipo) = LOWER(%s)
                    ORDER BY leitura.id DESC
                    LIMIT 5
                ) AS ultimos
            )
        """

        cursor.execute(sql, (tipo,))
        conexao.commit()

        print(f"[green]{cursor.rowcount} registros apagados.[/green]")

def atualizar():
    while True:
        atual = input(
            "\nQual registro você quer atualizar?\n"
            "1- CPU\n"
            "2- Memória\n"
            "3- Disco\n"
            "4- Internet\n"
            "5- Sair\n"
        )

        tipos = {
            "1": "CPU",
            "2": "Memória",
            "3": "Disco",
            "4": "Rede"
        }

        if atual.lower() == "sair" or atual == "5":
            return

        if atual.lower() in ["cpu", "memória", "memoria", "disco", "internet", "rede"]:
            if atual.lower() == "cpu":
                tipo = "CPU"
            elif atual.lower() in ["memória", "memoria"]:
                tipo = "Memória"
            elif atual.lower() == "disco":
                tipo = "Disco"
            else:
                tipo = "Rede"
        elif atual in tipos:
            tipo = tipos[atual]
        else:
            print("[red]Opção inválida![/red]")
            continue

        sql = """
            UPDATE leitura
            SET data_hora = NOW()
            WHERE id IN (
                SELECT id FROM (
                    SELECT leitura.id
                    FROM leitura
                    INNER JOIN configuracao
                        ON leitura.configuracao_fk = configuracao.id
                    INNER JOIN componente
                        ON configuracao.componente_fk = componente.id
                    INNER JOIN tipo_componente
                        ON componente.tipo_componente_fk = tipo_componente.id
                    WHERE LOWER(tipo_componente.tipo) = LOWER(%s)
                    ORDER BY leitura.id DESC
                    LIMIT 3
                ) AS ultimos
            )
        """

        cursor.execute(sql, (tipo,))
        conexao.commit()

        print(f"[green]{cursor.rowcount} registros atualizados.[/green]")


def decisao():
    while True:
        dec = input(
            "\nQuais dados você quer?\n"
            "1- Informações do PC\n"
            "2- Banco de Dados\n"
            "3- Deletar Registros\n"
            "4- Atualizar Registros\n"
            "5- Sair\n"
        )

        if dec.lower() == "banco de dados" or dec == "2":
            banco()

        elif dec.lower() in ["informações do pc", "informaçoes do pc", "informacoes do pc", "1"]:
            usuario()

        elif dec.lower() in ["deletar registros", "deletar registro", "3"]:
            deletar()

        elif dec.lower() in ["atualizar registros", "atualizar registro", "4"]:
            atualizar()

        elif dec.lower() == "sair" or dec == "5":
            print("[green]Programa encerrado![/green]")
            break

        else:
            print("[red]Opção inválida![/red]")

def capturar_todos():
    while True:
        quantidade = input(
            "\nQuantas capturas completas você deseja fazer? "
        )

        if quantidade.isdigit() and int(quantidade) > 0:
            quantidade = int(quantidade)
            break

        print("[red]Digite um número inteiro maior que zero![/red]")

    for i in range(quantidade):
        print(f"\n[bold cyan]CAPTURA {i + 1} DE {quantidade}[/bold cyan]")

        # CPU
        print("\n[bold]Capturando CPU...[/bold]")

        uso_cpu = p.cpu_percent(interval=1)
        times = p.cpu_times(percpu=False)
        cpus_logicas = p.cpu_count(logical=True)

        print(f"Uso da CPU: {uso_cpu}%")
        print(f"CPU Times: {times.user + times.system:.2f} segundos")
        print(f"CPUs lógicas: {cpus_logicas}")

        registrar_leitura("CPU", "Porcentagem", uso_cpu)
        registrar_leitura(
            "CPU", "Tempo CPU", times.user + times.system
        )
        registrar_leitura("CPU", "CPUs lógicas", cpus_logicas)

        # MEMÓRIA
        print("\n[bold]Capturando memória...[/bold]")

        memoria = p.virtual_memory()

        memoria_total = memoria.total / (1024 ** 3)
        ram_disponivel = memoria.available / (1024 ** 3)
        ram_usada = memoria.used / (1024 ** 3)
        memoria_livre = memoria.free / (1024 ** 3)
        uso_ram = memoria.percent

        print(f"RAM total: {memoria_total:.2f} GB")
        print(f"RAM disponível: {ram_disponivel:.2f} GB")
        print(f"RAM usada: {ram_usada:.2f} GB")
        print(f"RAM livre: {memoria_livre:.2f} GB")
        print(f"Uso da RAM: {uso_ram}%")

        registrar_leitura("Memória", "RAM Total", memoria_total)
        registrar_leitura(
            "Memória", "RAM Disponível", ram_disponivel
        )
        registrar_leitura("Memória", "RAM Usada", ram_usada)
        registrar_leitura("Memória", "RAM Livre", memoria_livre)
        registrar_leitura("Memória", "Uso da RAM", uso_ram)
        print("\n[bold]Capturando disco...[/bold]")

        disk = p.disk_usage("/")
        disco_total = disk.total / (1024 ** 3)
        disco_usado = disk.used / (1024 ** 3)
        disco_livre = disk.free / (1024 ** 3)
        uso_disco = disk.percent

        print(f"Disco total: {disco_total:.2f} GB")
        print(f"Disco usado: {disco_usado:.2f} GB")
        print(f"Disco livre: {disco_livre:.2f} GB")
        print(f"Uso do disco: {uso_disco}%")

        registrar_leitura("Disco", "Disco Total", disco_total)
        registrar_leitura("Disco", "Disco Usado", disco_usado)
        registrar_leitura("Disco", "Disco Livre", disco_livre)
        registrar_leitura("Disco", "Uso do Disco", uso_disco)
        print("\n[bold]Testando a internet...[/bold]")
        print("Aguarde, essa etapa pode demorar.")
        st = speedtest.Speedtest()
        st.get_best_server()
        ping = round(st.results.ping, 2)
        download_speed = round(
            st.download() / 1_000_000, 2
        )
        upload_speed = round(
            st.upload() / 1_000_000, 2
        )
        print(f"Ping: {ping:.2f} ms")
        print(f"Download: {download_speed:.2f} Mbps")
        print(f"Upload: {upload_speed:.2f} Mbps")
        registrar_leitura("Rede", "Latencia", ping)
        registrar_leitura(
            "Rede", "Velocidade", download_speed
        )
        registrar_leitura(
            "Rede", "Velocidade", upload_speed
        )
        print(
            f"\n[green]Captura {i + 1} concluída![/green]"
        )
    print(
        f"\n[bold green]Todas as {quantidade} "
        "capturas foram finalizadas![/bold green]"
    )
decisao()
cursor.close()
conexao.close()