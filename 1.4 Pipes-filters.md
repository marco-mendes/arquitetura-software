### Seção: Estilo Arquitetural Pipes and Filters

O estilo arquitetural Pipes and Filters (Tubos e Filtros) é amplamente utilizado em sistemas que necessitam processar fluxos de dados de maneira sequencial e independente. Nesse estilo, os dados fluem através de uma série de componentes de processamento, denominados "Filtros", conectados por canais de comunicação, chamados de "Pipes".

<img width="1098" alt="image" src="https://github.com/user-attachments/assets/dbf18625-fe5a-4142-b9e5-58ac0ff93ff3" />


#### Definição e Características

O conceito principal do Pipes and Filters é dividir um sistema em uma cadeia de filtros que realizam transformações específicas nos dados, interligados por pipes que transportam os dados de um filtro para outro. Algumas características principais desse estilo incluem:

- **Modularidade:** Cada filtro é um componente independente que realiza uma transformação específica.
- **Flexibilidade:** Os filtros podem ser reorganizados ou substituídos sem afetar os outros componentes.
- **Reutilização:** Filtros podem ser usados em diferentes pipelines.
- **Concorrência:** Cada filtro pode ser executado em paralelo, processando dados de forma independente.


#### Exemplos

##### Exemplo de linha de comando Linux

Este exemplo simplificado utiliza os comandos **cat** e **grep** para demonstrar o padrão **Pipes and Filters**. Suponha que você tenha um arquivo chamado `dados.txt` contendo os seguintes dados:

**dados.txt**:
```
Service A,up,120
Service B,down,0
Service C,up,95
```

**Passo a Passo**

**1. Exibir o conteúdo do arquivo**

O comando `cat` é usado para exibir o conteúdo do arquivo:

**Comando:**
```bash
cat dados.txt
```
**Saída:**
```
Service A,up,120
Service B,down,0
Service C,up,95
```

**2. Filtrar serviços com status "up"**

Usamos o comando `grep` para selecionar apenas as linhas onde o status seja "up":

**Comando:**
```bash
cat dados.txt | grep ",up,"
```
**Saída:**
```
Service A,up,120
Service C,up,95
```
**Explicação:**
- `cat dados.txt`: Lê o conteúdo do arquivo.
- `grep ",up,": Filtra as linhas que contêm a palavra "up" seguida por uma vírgula.

**3. Filtrar serviços com duração maior que 100 segundos**

Adicionamos mais um filtro usando `grep` para selecionar apenas as linhas onde a duração seja maior que 100 segundos:

**Comando:**
```bash
cat dados.txt | grep ",up," | grep ",120"
```
**Saída:**
```
Service A,up,120
```
**Explicação:**
- `grep ",120"`: Filtra as linhas que contêm ",120" (duração de 120 segundos).

**Combinação dos Comandos**
Os comandos podem ser encadeados com pipes (`|`) para formar um pipeline:
```bash
cat dados.txt | grep ",up," | grep ",120"
```

**Resultado Final**
- Apenas os serviços que atendem às condições especificadas serão exibidos no terminal.


**Exemplo de Kafka com Arquivos Simulados**

Este exemplo expande o uso do Kafka simulando o trânsito de mensagens entre as etapas como arquivos intermediários. Os arquivos representam os dados que seriam transferidos entre os tópicos no Kafka.

**1. Produção de Dados (Producer)**
```python
from kafka import KafkaProducer
import json

# Configura o produtor para enviar mensagens para o Kafka.
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simula a escrita das mensagens em um arquivo.
with open('entrada.json', 'w') as file:
    messages = []
    for i in range(5):
        message = {'id': i, 'valor': i * 10}
        messages.append(message)
        producer.send('entrada', message)
    json.dump(messages, file, indent=4)

producer.close()
```
**Arquivo Gerado:** `entrada.json`
```json
[
    {"id": 0, "valor": 0},
    {"id": 1, "valor": 10},
    {"id": 2, "valor": 20},
    {"id": 3, "valor": 30},
    {"id": 4, "valor": 40}
]
```

**2. Filtro (Consumer e Transformer)**
```python
from kafka import KafkaConsumer, KafkaProducer
import json

# Configura o consumidor para ler mensagens do tópico "entrada".
consumer = KafkaConsumer(
    'entrada',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Configura o produtor para enviar mensagens processadas para o tópico "saida".
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Processa cada mensagem lida e adiciona um campo "processado".
processed_messages = []
for message in consumer:
    dado = message.value
    dado['processado'] = True
    processed_messages.append(dado)
    producer.send('saida', dado)

# Simula a escrita das mensagens processadas em um arquivo.
with open('saida_intermediaria.json', 'w') as file:
    json.dump(processed_messages, file, indent=4)

consumer.close()
producer.close()
```
**Arquivo Gerado:** `saida_intermediaria.json`
```json
[
    {"id": 0, "valor": 0, "processado": true},
    {"id": 1, "valor": 10, "processado": true},
    {"id": 2, "valor": 20, "processado": true},
    {"id": 3, "valor": 30, "processado": true},
    {"id": 4, "valor": 40, "processado": true}
]
```

**3. Consumo de Dados Processados**
```python
from kafka import KafkaConsumer
import json

# Configura o consumidor para ler mensagens do tópico "saida".
consumer = KafkaConsumer(
    'saida',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Exibe as mensagens processadas e as salva em um arquivo final.
final_messages = []
for message in consumer:
    final_messages.append(message.value)
    print(f"Dados processados: {message.value}")

with open('saida_final.json', 'w') as file:
    json.dump(final_messages, file, indent=4)

consumer.close()
```
**Arquivo Gerado:** `saida_final.json`
```json
[
    {"id": 0, "valor": 0, "processado": true},
    {"id": 1, "valor": 10, "processado": true},
    {"id": 2, "valor": 20, "processado": true},
    {"id": 3, "valor": 30, "processado": true},
    {"id": 4, "valor": 40, "processado": true}
]
```

**Resumo do Processo**
1. O arquivo `entrada.json` representa os dados originais enviados pelo produtor.
2. O arquivo `saida_intermediaria.json` contém os dados processados pelo filtro e enviados ao tópico "saida".
3. O arquivo `saida_final.json` armazena os dados finais consumidos do tópico "saida".

#### Benefícios do Estilo Pipes and Filters

1. **Escalabilidade:** É possível adicionar novos filtros ou modificar o pipeline para atender a novas demandas sem alterar a arquitetura geral do sistema.
2. **Manutenção Simples:** A modularidade facilita a identificação e correção de problemas em filtros específicos.
3. **Reutilização de Componentes:** Filtros podem ser utilizados em diferentes pipelines, aumentando a eficiência do desenvolvimento.

#### Desafios

1. **Latência:** A comunicação entre filtros pode introduzir atrasos, especialmente em pipelines com muitos componentes.
2. **Erro de Acoplamento:** Se não bem projetado, um filtro pode depender excessivamente de outros, reduzindo a independência dos componentes.
3. **Gerenciamento de Estado:** Filtros normalmente são projetados como componentes sem estado. Se for necessário gerenciar estado, isso pode complicar a implementação.

#### Exemplo Mais Elaborado
<img width="1102" alt="image" src="https://github.com/user-attachments/assets/3eb7c776-9617-40bf-aee5-1725139627dc" />

Aqui está uma implementação simplificada do diagrama "Pipes and Filters" com Kafka e MongoDB que suporta o desenho acima.

#### Produção de Dados (Producer)
```python
from kafka import KafkaProducer
import json

# Configura o produtor para enviar mensagens ao Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Geração de informações de serviço simuladas
messages = [
    {"service": "Service A", "status": "up", "duration": 120},
    {"service": "Service B", "status": "down", "duration": 0},
    {"service": "Service C", "status": "up", "duration": 95}
]

for message in messages:
    producer.send('service-info', message)
producer.close()
```

#### Filtro de Duração (Duration Filter)
```python
from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    'service-info',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Filtra apenas serviços com duração maior que 100 segundos
for message in consumer:
    data = message.value
    if data['duration'] > 100:
        producer.send('duration-filtered', data)
consumer.close()
producer.close()
```

#### Filtro de Uptime (Uptime Filter)
```python
consumer = KafkaConsumer(
    'service-info',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Filtra serviços com status "up"
for message in consumer:
    data = message.value
    if data['status'] == 'up':
        producer.send('uptime-filtered', data)
consumer.close()
producer.close()
```

#### Calculadora de Duração (Duration Calculator)
```python
consumer = KafkaConsumer(
    'duration-filtered',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Adiciona um cálculo de duração acumulada
accumulated_duration = 0
for message in consumer:
    data = message.value
    accumulated_duration += data['duration']
    data['accumulated_duration'] = accumulated_duration
    producer.send('duration-calculated', data)
consumer.close()
producer.close()
```

#### Calculadora de Uptime (Uptime Calculator)
```python
consumer = KafkaConsumer(
    'uptime-filtered',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Calcula a porcentagem de uptime
uptime_count = 0
total_services = 0
for message in consumer:
    data = message.value
    total_services += 1
    if data['status'] == 'up':
        uptime_count += 1
    data['uptime_percentage'] = (uptime_count / total_services) * 100
    producer.send('uptime-calculated', data)
consumer.close()
producer.close()
```

#### Output para MongoDB
```python
from kafka import KafkaConsumer
import pymongo
import json

# Configura conexão com o MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['service_db']
collection = db['service_data']

consumer = KafkaConsumer(
    'duration-calculated',
    'uptime-calculated',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Insere os dados no MongoDB
for message in consumer:
    collection.insert_one(message.value)
consumer.close()
```

### Resumo
Este código implementa os componentes do diagrama "Pipes and Filters", utilizando Kafka como transporte de dados e MongoDB como destino final. Cada filtro e transformador opera independentemente, seguindo o padrão arquitetural descrito.


