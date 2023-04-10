import GeneralPin
# Подключаем Flask
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
# Настройка пинов
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Реле
RelePin = GeneralPin.RelePin
for r in RelePin:
    GPIO.setup(r, GPIO.OUT)
    GPIO.output(r, GPIO.HIGH)
def RELE(ACTION, DATA):
    if ACTION == 'LAN_RELE':
        for n in range(0, len(RelePin)):
            if 'RELE'+str(n+1) == DATA:
                if GPIO.input(RelePin[n]) == 1:
                    GPIO.output(RelePin[n], GPIO.LOW)
                    return 'OFF'
                else:
                    GPIO.output(RelePin[n], GPIO.HIGH)
                    return 'ON'
    elif ACTION == 'NUR_RELE':
        ReleInput = '';
        for m in RelePin:
            ReleInput = ReleInput + str(GPIO.input(m))
        return ReleInput
# Датчик температуры и влажности
import Adafruit_DHT
DHT_SENSOR = Adafruit_DHT.DHT22
def DHT22(ACTION):
    if ACTION != None:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, GeneralPin.DHT22Pin)
        if ACTION == 'TEM_DHT22':
            return int(temperature)
        elif ACTION == 'HUM_DHT22':
            return int(humidity)
# Датчик воды
WaterPin = GeneralPin.WaterPin;
def WaterData(ACTION):
    if ACTION == 'WAR_DAT':
        Data = ''
        for n in WaterPin:
            GPIO.setup(n, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            Data = Data + str(GPIO.input(n))
        return Data
# Обратная связь
@app.route("/")
def home():
    if request.is_json:
        # Реле
        ReleButton = RELE('LAN_RELE', request.args.get('ReleButton'))
        ReleData = RELE(request.args.get('ReleData'), '')
        Temperature = DHT22(request.args.get('Temperature'))
        Humidity = DHT22(request.args.get('Humidity'))
        Water = WaterData(request.args.get('Water'))
        return jsonify({'ReleButton': ReleButton, 'ReleData': ReleData, 'Temperature': Temperature, 'Humidity': Humidity, 'Water': Water})
    return render_template('index.html')
# Запускаем
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)

    
