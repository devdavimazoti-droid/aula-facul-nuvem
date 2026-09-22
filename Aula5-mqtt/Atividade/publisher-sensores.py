import paho.mqtt.client as mqtt
import time
import random
import json

broker = "10.110.18.11"
port = 1883


topicTemp = "sensorMz/temperatura"
topicUmid = "sensorMz/umidade"
topicPres = "sensorMz/pressao"
topicUmidSolo = "sensorMz/umidadeSolo"
topicCO2 = "sensorMz/CO2"

def publicacaoDados(id, medida, unidade, topic):

    dados = {
        "sensor" : str(id),
        "medida" : medida,
        "medicao" : round(random.uniform(10, 50), 2),
        "unidade" : unidade,
        "timestamp" : time.time()
    }
    mensagem = json.dumps(dados)
    client.publish(topic, mensagem)
    print(f"Enviado: {mensagem}\n")
    time.sleep(15)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(broker, port, 60)

while True:
    publicacaoDados(1, "temperatura", "°C", topicTemp)
    publicacaoDados(2, "umidade", "%", topicUmid)
    publicacaoDados(3, "pressao", "bar", topicPres)
    publicacaoDados(4, "umidadeSolo", "%", topicUmidSolo)
    publicacaoDados(5, "nivelCO2", "ppm", topicCO2)
    