import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
from movetest import *
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
import mysql.connector
from threading import Timer, Lock
from time import sleep
import signal
import sys
from sense_hat import SenseHat
from time import sleep
import datetime
import socket

## 기기  ip주소 반환하는부분
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
rpi_ip = '_' + s.getsockname()[0]

##무빙하는 테스트 부분
mh = Raspi_MotorHAT(addr=0x6f)
atexit.register(turnOffMotors)

myMotor = mh.getMotor(2)
pwm = PWM(0x6F);
pwm.setPWMFreq(60);

## 센싱부분
sense = SenseHat()
timer2 = None
lock = Lock()


def closeDB(signal, frame):
    print("BYE")
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    cur.close()
    db.close()
    timer.cancel()
    timer2.cancel()
    sys.exit(0)


def init():
    global cur, db, sense, rpi_ip
    rpi_ip = rpi_ip.replace('.', '')

    query = (
                "CREATE TABLE `userDB`.`" + rpi_ip + "` (`time` DATETIME NOT NULL, `pressure` DOUBLE NOT NULL, `temp` DOUBLE NOT NULL, `humidity` DOUBLE NOT NULL, `id` INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id`))");
    lock.acquire()
    cur.execute(query)
    db.commit()
    lock.release()


def sensing():
    global cur, db, sense, rpi_ip

    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    time = datetime.datetime.now()
    pressure = round(pressure / 1000, 3)
    temp = round(temp, 1)
    humidity = round(humidity, 1)

    rpi_ip = rpi_ip.replace('.', '')
    query = "insert into " + rpi_ip + "(time, pressure, temp, humidity) values (%s, %s, %s, %s)"
    value = (time, pressure, temp, humidity)

    lock.acquire()
    cur.execute(query, value)
    db.commit()
    lock.release()

    global timer2
    timer2 = Timer(60, sensing)
    timer2.start()


db = mysql.connector.connect(host='43.201.32.249', user='admin', password='1234', database='userDB',
                             auth_plugin='mysql_native_password')
cur = db.cursor()
ready = None
timer = None
sense = SenseHat()
timer2 = None
lock = Lock()

signal.signal(signal.SIGINT, closeDB)
init()
sensing()

##페이지
PAGE = """\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<style>
*{
    margin: 0;
    padding: 0;
}
</style>
<body>
<img src="stream.mjpg" width="1080" height="1440" style=" transform: scaleX(-1) scaleY(-1);"/>
</body>
</html>
"""


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


spd = 0
lefrig = 375
dir1 = 0.0


class StreamingHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
        if (self.path[1] == '?'):
            global spd
            global lefrig
            global dir1
            beforey = ((self.path).index('y'))
            xx = float(self.path[4:beforey - 1])
            yy = float(self.path[beforey + 2:])

            print(xx, yy)
            ## xx가 음수면 좌회전 양수면 우회전
            if (xx == 0):
                dir1 = 0
            elif (xx < 0 and lefrig > 325):
                dir1 += -7
            elif (xx > 0 and lefrig < 410):
                dir1 += 5

            ## 모터속도는 yy비율에 맞춰서 좌우회전은 20도씩 천천히
            lefrig = int(375 + dir1)
            pwm.setPWM(0, 0, lefrig)

            print(lefrig, int(spd))
            ## yy가 음수면 후진 양수면 전진
            if (yy == 0):
                spd = 0
            elif (yy > 0 and spd <= 235 and yy <= 1):
                spd += 20 * yy
            elif (yy < 0 and spd >= -235 and yy >= -1):
                spd += 20 * yy

            if (spd == 0):
                myMotor.run(Raspi_MotorHAT.RELEASE)
            elif (spd < 0):
                myMotor.setSpeed(abs(int(spd)))
                myMotor.run(Raspi_MotorHAT.FORWARD)
            elif (spd > 0):
                myMotor.setSpeed(abs(int(spd)))
                myMotor.run(Raspi_MotorHAT.BACKWARD)
        elif self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


with picamera.PiCamera(resolution='1080x1440', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
