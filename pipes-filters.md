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

##### Exemplo com Apache Kafka
Abaixo está um exemplo mínimo de pipeline de dados utilizando Apache Kafka para ilustrar o estilo Pipes and Filters. Cada parte do código é explicada para maior compreensão:

**Produção de Dados (Producer):**
```python
from kafka import KafkaProducer
import json

# Configura o produtor para enviar mensagens para o Kafka.
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Envia mensagens para o tópico "entrada".
for i in range(5):
    producer.send('entrada', {'id': i, 'valor': i * 10})
producer.close()
```
*Este código inicializa um produtor Kafka que envia cinco mensagens para o tópico "entrada". Cada mensagem contém um ID e um valor calculado.*

**Filtro (Consumer e Transformer):**
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
for message in consumer:
    dado = message.value
    dado['processado'] = True
    producer.send('saida', dado)
consumer.close()
producer.close()
```
*Neste trecho, o consumidor lê mensagens do tópico "entrada", processa os dados adicionando um novo campo, e envia para o tópico "saida".*

**Consumo de Dados Processados:**
```python
from kafka import KafkaConsumer
import json

# Configura o consumidor para ler mensagens do tópico "saida".
consumer = KafkaConsumer(
    'saida',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Exibe as mensagens processadas.
for message in consumer:
    print(f"Dados processados: {message.value}")
consumer.close()
```
*Aqui, um consumidor lê e imprime as mensagens do tópico "saida", exibindo os dados processados.*

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


