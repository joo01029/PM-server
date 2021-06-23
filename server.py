import spidev
from flask import  Flask, escape,request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
bus = 0
device = 0

spi = spidev.SpiDev()
spi.open(bus,device)
spi.max_speed_hz = 1000000

def analogRead(channel):
    buf = [(1<<2)|(1<<1)|(channel&4) >>2, (channel&3)<6,0]
    buf = spi.xfer3(buf)
    adcValue = ((buf[1] & 0xf)<<8 | buf[2])
    return adcValue

def avarage():
    num = 0
    for i in range(0,100):
        num += analogRead(1)
    return str (num / 100);

@app.route('/')
def getValue():
    value = avarage()
    return jsonify({"value":value})

if __name__ == "__main__":
    app.run(host="192.168.0.35",port=5000) 
