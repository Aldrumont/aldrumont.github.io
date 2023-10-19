import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Configurar os pinos do GPIO
PINS = {
    "verde": 12,
    "vermelho": 21,
    "branco": 20,
    "azul": 16
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(list(PINS.values()), GPIO.OUT)
GPIO.output(list(PINS.values()), GPIO.HIGH)

# Callback quando uma mensagem PUBLISH é recebida do servidor.
def on_message(client, userdata, message):
    print(f"Recebida mensagem '{message.payload.decode()}' no tópico '{message.topic}'")

    cor = message.payload.decode().lower()

    if cor in PINS.keys():
        estado_atual = GPIO.input(PINS[cor])
        novo_estado = GPIO.HIGH if estado_atual == GPIO.LOW else GPIO.LOW
        GPIO.output(PINS[cor], novo_estado)
        acao = "aceso" if novo_estado == GPIO.LOW else "apagado"  # Lembre-se, a lógica está invertida
        print(f"LED {cor} {acao}.")
    elif cor == "apagar":
        GPIO.output(list(PINS.values()), GPIO.HIGH)
        print("Todos os LEDs apagados.")

# Configurações do MQTT
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "aldrumont/insidegg"

client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

# Loop para continuar processando mensagens
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Desconectado pelo usuário")
finally:
    GPIO.cleanup()
    print("GPIO limpo e desconectado do broker.")
