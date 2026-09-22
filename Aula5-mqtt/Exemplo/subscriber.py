import paho.mqtt.client as mqtt # Importa a biblioteca reponsável pela comunicação
import time # Importa a biblioteca que permite controlar tempo e pausas
import random # Importa a biblioteca que gera números aleatórios

broker = "10.110.18.11" # Armazena o IP do servidor onde o broker MQTT está em execução
port = 1883 # Armazena a porta usada pelo serviço MQTT no servidor
topic = "sensor/temperaturaMazoti" # Armazena o nome do tópico para ondde os dados serão enviados

def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.topic} -> {msg.payload.decode()}")

# Cria o objeto cliente que fará a conexão e o envio das mensagens MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(broker, port, 60) # Estabelece a conexão com o broker usando IP, porta e tempo de keepalive

client.subscribe(topic)
# Inscreve o cliente no tópico definido, permitindo receber mensagens publicadas nele

client.on_message = on_message
# Associa a função on_message como callback, ou seja, ela será chamada automaticamente ao receber mensagens

client.loop_forever()
# Mantém o cliente em execução contínua, aguardando e processando mensagens recebidas