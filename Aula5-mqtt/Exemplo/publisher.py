import paho.mqtt.client as mqtt # Importa a biblioteca reponsável pela comunicação
import time # Importa a biblioteca que permite controlar tempo e pausas
import random # Importa a biblioteca que gera números aleatórios

broker = "10.110.18.11" # Armazena o IP do servidor onde o broker MQTT está em execução
port = 1883 # Armazena a porta usada pelo serviço MQTT no servidor
topic = "sensor/temperaturaMazoti" # Armazena o nome do tópico para ondde os dados serão enviados

# Cria o objeto cliente que fará a conexão e o envio das mensagens MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(broker, port, 60) # Estabelece a conexão com o broker usando IP, porta e tempo de keepalive

while True:
    temperatura = round(random.uniform(20,30),2) # gera valores aleatórios entre 20 e 30 graus
    client.publish(topic, str(temperatura)) # envia o valor gerado para o tópico definido
    print(f"Temperatura enviada: {temperatura}°C") # mostra no terminal o valor que acabou de ser publicado
    time.sleep(2) # faz o programa esperar 2 segundos antes de repitir o processo