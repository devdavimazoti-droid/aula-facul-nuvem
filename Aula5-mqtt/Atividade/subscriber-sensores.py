import paho.mqtt.client as mqtt
import json
import requests
import time
import asyncio
import websockets

API_KEY = "XGRMJCQAJZZ5E843"
broker = "10.110.18.11"
port = 1883


topicTemp = "sensorMz/temperatura"
topicUmid = "sensorMz/umidade"
topicPres = "sensorMz/pressao"
topicUmidSolo = "sensorMz/umidadeSolo"
topicCO2 = "sensorMz/CO2"

clientes_conectados = set()

loop = None  # será preenchido quando o loop de fato começar a rodar


async def lidar_com_conexao(websocket):

    clientes_conectados.add(websocket)
    print("Navegador conectado!")

    try:
        await websocket.wait_closed()
    finally:
        # Se a conexão cair ou a aba fechar, removemos da lista.
        clientes_conectados.remove(websocket)
        print("Navegador desconectou.")


async def enviar_dados_para_o_front(mensagem_json):
    # Se a lista estiver vazia (ninguém com o site aberto), não fazemos nada
    if not clientes_conectados:
        return

    # Copia a lista antes de iterar, para evitar erro caso alguém
    # conecte/desconecte durante o envio
    for cliente in list(clientes_conectados):
        try:
            await cliente.send(mensagem_json)
        except websockets.exceptions.ConnectionClosed:
            pass


async def iniciar_websocket():
    global loop
    loop = asyncio.get_running_loop()  # pega o loop que está DE FATO rodando
    async with websockets.serve(lidar_com_conexao, "localhost", 8765):
        await asyncio.Future()  # Trava aqui e mantém o servidor rodando


def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()

    dados = json.loads(mensagem)

    print("--- Dados recebidos ---")
    print(f"Sensor: {dados['sensor']}")
    print(f"Medida: {dados['medida']}")
    print(f"Medição: {dados['medicao']} {dados['unidade']}")
    print(f"Timestamp: {dados['timestamp']}")
    print("-----------------------")

    if loop is not None:
        asyncio.run_coroutine_threadsafe(enviar_dados_para_o_front(mensagem), loop)

    response = requests.get(f"https://api.thingspeak.com/update?api_key={API_KEY}&field{dados['sensor']}={dados['medicao']}")
    print(f"Resposta da API: {response}\n")

    time.sleep(15)



client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(broker, port, 60)


client.subscribe([(topicTemp, 0), (topicUmid, 0), (topicPres, 0), (topicUmidSolo, 0), (topicCO2, 0)])
client.on_message = on_message


client.loop_start()


asyncio.run(iniciar_websocket())