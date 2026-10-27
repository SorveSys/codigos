# instala biblioetecas
install.packages("ggplot2")
install.packages(c("dplyr", "tidyr"))

# ----------------------------------------------------------
library(ggplot2)

# lê o CSV
dados <- read.csv("C:/Users/melis/Downloads/codigos/Python/dados_monitoramento.csv",
                  stringsAsFactors = FALSE)

dados$dt_hora <- as.POSIXct(dados$dt_hora)
dados$id_servidor <- factor(dados$id_servidor)


# Registros sem alerta vêm vazios no CSV, então vira NA
dados$alerta[dados$alerta == ""] <- NA

# Separa os dados por métrica
cpu   <- subset(dados, metrica == "Porcentagem de Uso (%)")
ram   <- subset(dados, metrica == "Uso da Memoria (%)")
disco <- subset(dados, metrica == "Espaco em uso (%)")
temp  <- subset(dados, metrica == "Temperatura (Celsius)")


nrow(dados)
table(ram$id_servidor)

# ----------------------------------------------------------

# Uso da CPU ao longo do tempo - servidores de uma empresa juntos

# 1. Escolhe a empresa (a da medição mais recente, ou fixe com um número)
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

# 2. Descobre a empresa da medição mais recente
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

# 3. Procura o nome da empresa
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

nome_empresa <- dados$empresa[dados$id_empresa == id_empresa_escolhida][1]

# 4. Filtra a CPU só dessa empresa
cpu_empresa <- subset(cpu, id_empresa == id_empresa_escolhida)

# 5. Mantém só o dia da última medição da empresa
ultimo_dia <- format(max(cpu_empresa$dt_hora), "%Y-%m-%d")
cpu_empresa <- subset(cpu_empresa, format(dt_hora, "%Y-%m-%d") == ultimo_dia)

# 6. Remove da legenda os servidores que não sobraram
cpu_empresa$id_servidor <- droplevels(cpu_empresa$id_servidor)

grafico <- ggplot(cpu_empresa, aes(x = dt_hora, y = valor, color = id_servidor)) +
  geom_line() +
  geom_point() +
  geom_hline(yintercept = 70, linetype = "dashed", colour = "orange") +
  geom_hline(yintercept = 85, linetype = "dashed", colour = "red") +
  scale_x_datetime(date_breaks = "1 min", date_labels = "%H:%M") +
  labs(title = paste("Uso da CPU ao longo do tempo - empresa", nome_empresa),
       x = "Horário", y = "Uso (%)", color = "Servidor") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

print(grafico)

# --------------------------------------------------------------

# CPU ao longo do tempo de TODOS os servidores de uma empresa separadamente

# 1. Escolhe a empresa (a da medição mais recente, ou fixe com um número)
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

# 2. Filtra a CPU só dessa empresa
cpu_empresa <- subset(cpu, id_empresa == id_empresa_escolhida)

# 3. Mantém só o dia da última medição da empresa
ultimo_dia <- format(max(cpu_empresa$dt_hora), "%Y-%m-%d")
cpu_empresa <- subset(cpu_empresa, format(dt_hora, "%Y-%m-%d") == ultimo_dia)

# 4. Remove da legenda os servidores que não sobraram
cpu_empresa$id_servidor <- droplevels(cpu_empresa$id_servidor)

ggplot(cpu_empresa, aes(x = dt_hora, y = valor)) +
  geom_line() +
  facet_wrap(~ id_servidor, scales = "free_x")

# --------------------------------------------------------------

# Temperatura da CPU ao longo do tempo - servidores de uma empresa

# 1. Descobre a empresa da medição mais recente
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

# 2. Procura o nome da empresa
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

nome_empresa <- dados$empresa[dados$id_empresa == id_empresa_escolhida][1]
temp_empresa <- subset(temp, id_empresa == id_empresa_escolhida)

if (nrow(temp_empresa) == 0) {
  
  print(paste("A empresa", id_empresa_escolhida, "não possui leituras de temperatura."))
  
} else {
  
  ultimo_dia <- format(max(temp_empresa$dt_hora), "%Y-%m-%d")
  temp_empresa <- subset(temp_empresa, format(dt_hora, "%Y-%m-%d") == ultimo_dia)
  temp_empresa$id_servidor <- droplevels(temp_empresa$id_servidor)
  
  grafico <- ggplot(temp_empresa, aes(x = dt_hora, y = valor, color = id_servidor)) +
    geom_line() +
    geom_point() +
    geom_hline(yintercept = 70, linetype = "dashed", colour = "orange") +
    geom_hline(yintercept = 80, linetype = "dashed", colour = "red") +
    scale_x_datetime(date_breaks = "1 min", date_labels = "%H:%M") +
    labs(title = paste("Temperatura da CPU ao longo do tempo - empresa", nome_empresa),
         x = "Horário", y = "Temperatura (°C)", color = "Servidor") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  print(grafico)
}

# --------------------------------------------------------------

# Uso da RAM ao longo do tempo - servidores de uma empresa

# 1. Descobre a empresa da medição mais recente
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

# 2. Procura o nome da empresa
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

nome_empresa <- dados$empresa[dados$id_empresa == id_empresa_escolhida][1]

ram_empresa <- subset(ram, id_empresa == id_empresa_escolhida)

if (nrow(ram_empresa) == 0) {
  
  print(paste("A empresa", id_empresa_escolhida, "não possui dados de RAM."))
  
} else {
  
  ultimo_dia <- format(max(ram_empresa$dt_hora), "%Y-%m-%d")
  ram_empresa <- subset(ram_empresa, format(dt_hora, "%Y-%m-%d") == ultimo_dia)
  ram_empresa$id_servidor <- droplevels(ram_empresa$id_servidor)
  
  grafico <- ggplot(ram_empresa, aes(x = dt_hora, y = valor, color = id_servidor)) +
    geom_line() +
    geom_point() +
    geom_hline(yintercept = 75, linetype = "dashed", colour = "orange") +
    geom_hline(yintercept = 90, linetype = "dashed", colour = "red") +
    scale_x_datetime(date_breaks = "1 min", date_labels = "%H:%M") +
    labs(title = paste("Uso da Memória RAM ao longo do tempo - empresa", nome_empresa),
         x = "Horário", y = "Uso (%)", color = "Servidor") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  print(grafico)
}

# --------------------------------------------------------------

# Média de uso por tipo de servidor (pagamento, auditoria, transito)

# 1. Descobre a empresa da medição mais recente
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

# 2. Procura o nome da empresa
id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

nome_empresa <- dados$empresa[dados$id_empresa == id_empresa_escolhida][1]

# 3. Filtra os dados dessa empresa
dados_empresa <- subset(dados, id_empresa == id_empresa_escolhida)

# 4. Mantém só as métricas percentuais de uso
percentuais <- subset(dados_empresa, metrica %in% c("Porcentagem de Uso (%)",
                                                    "Uso da Memoria (%)",
                                                    "Espaco em uso (%)"))

# 5. Média por tipo de servidor e componente
media <- aggregate(valor ~ tipo_servidor + componente, data = percentuais, FUN = mean)

# 6. Gráfico
ggplot(media, aes(x = tipo_servidor, y = valor, fill = componente)) +
  geom_col(position = "dodge") +
  labs(title = paste("Média de uso por tipo de servidor - empresa", nome_empresa),
       x = "Tipo de servidor", y = "Uso médio (%)", fill = "Componente")

# --------------------------------------------------------------
# Ranking dos servidores com mais alertas - empresa

# Alertas da empresa escolhida
alertas_empresa <- subset(dados, !is.na(alerta) & id_empresa == id_empresa_escolhida)

id_empresa_escolhida <- dados$id_empresa[which.max(dados$dt_hora)]

nome_empresa <- dados$empresa[dados$id_empresa == id_empresa_escolhida][1]

if (nrow(alertas_empresa) == 0) {
  
  print(paste("A empresa", id_empresa_escolhida, "não possui alertas."))
  
} else {
  
  # 1. Conta os alertas de cada servidor
  alertas_empresa$id_servidor <- droplevels(alertas_empresa$id_servidor)
  ranking <- as.data.frame(table(alertas_empresa$id_servidor))
  names(ranking) <- c("id_servidor", "qtd_alertas")
  
  # 2. Ordena do maior para o menor e fica com os 5 primeiros
  ranking <- ranking[order(ranking$qtd_alertas, decreasing = TRUE), ]
  ranking <- head(ranking, 5)
  
  # 3. Fixa a ordem das barras (o maior fica no topo)
  ranking$id_servidor <- factor(ranking$id_servidor, levels = rev(ranking$id_servidor))
  
  # 4. Gráfico
  grafico <- ggplot(ranking, aes(x = id_servidor, y = qtd_alertas)) +
    geom_col(fill = "firebrick") +
    geom_text(aes(label = qtd_alertas), hjust = -0.3) +
    coord_flip() +
    scale_y_continuous(expand = expansion(mult = c(0, 0.15))) +
    labs(title = paste("Ranking de servidores com mais alertas - empresa", nome_empresa),
         x = "Servidor", y = "Quantidade de alertas")
  
  print(grafico)
}
# --------------------------------------------------------------

# Histograma do uso da PCPU
ggplot(cpu, aes(x = valor)) +
  geom_histogram(binwidth = 5, fill = "lightblue", color = "gray") +
  labs(title = "Distribuição do uso da CPU",
       x = "Uso (%)", y = "Quantidade de medições")

