import RPi.GPIO as GPIO
import time

class MotorControl(object):
        def __init__(self, ain1=12, ain2=13, ena=6, bin1=20, bin2=21, enb=26):
                self.AIN1 = ain1
                self.AIN2 = ain2
                self.BIN1 = bin1
                self.BIN2 = bin2
                self.ENA = ena
                self.ENB = enb
                self.PA  = 50
                self.PB  = 50
                self.motor_min = -100
                self.motor_max = 100
                self.motorDelta = 0
                self.acceleration = 1

                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                GPIO.setup(self.AIN1,GPIO.OUT)
                GPIO.setup(self.AIN2,GPIO.OUT)
                GPIO.setup(self.BIN1,GPIO.OUT)
                GPIO.setup(self.BIN2,GPIO.OUT)
                GPIO.setup(self.ENA,GPIO.OUT)
                GPIO.setup(self.ENB,GPIO.OUT)
                self.PWMA = GPIO.PWM(self.ENA,500)
                self.PWMB = GPIO.PWM(self.ENB,500)
                self.PWMA.start(self.PA)
                self.PWMB.start(self.PB)
                self.stop()

        def setPWMA(self, value):
                self.PA = value
                self.PWMA.ChangeDutyCycle(self.PA)

        def setPWMB(self, value):
                self.PB = value
                self.PWMB.ChangeDutyCycle(self.PB)

        def _setMotor(self, value, IN1, IN2, PWM):
                if(value >= 0):
                        GPIO.output(IN1,GPIO.HIGH)
                        GPIO.output(IN2,GPIO.LOW)
                else:
                        GPIO.output(IN1,GPIO.LOW)
                        GPIO.output(IN2,GPIO.HIGH)
                        value = -value
                PWM.ChangeDutyCycle(value)

        def setMotorA(self, target):
                error = target - self.PA
                PA = self.PA
                PA += error * self.acceleration
                self.PA = max(int(PA), self.motor_min)
                self.PA = min(int(PA), self.motor_max)
                self._setMotor(self.PA, self.AIN1, self.AIN2, self.PWMA)

        def setMotorB(self, target):
                error = target - self.PB
                PB = self.PB
                PB += error * self.acceleration
                self.PB = max(int(PB), self.motor_min)
                self.PB = min(int(PB), self.motor_max)
                self._setMotor(self.PB, self.BIN1, self.BIN2, self.PWMB)


        def setMotor(self, left, right):
                self.setMotorA(left)
                self.setMotorB(right)

        def stop(self):
                self.PA = 0
                self._setMotor(self.PA, self.AIN1, self.AIN2, self.PWMA)
                self.PB = 0
                self._setMotor(self.PB, self.BIN1, self.BIN2, self.PWMB)
                
                
        def test1(self):
                t = 5
                dt = 0.1
                while t > 0:
                    self.setMotor(100, 100)
                    time.sleep(dt)
                    t -= dt
                

if __name__=='__main__':

        controler = MotorControl()
        try:
                while True:
                        controler.test1()
                        time.sleep(5)
                        controler.stop()

        except KeyboardInterrupt:
                GPIO.cleanup()
