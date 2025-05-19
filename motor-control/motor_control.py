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
                self.motor_min = -100
                self.motor_max = 100

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

        def _setPWMA(self, value):
                self.PWMA.ChangeDutyCycle(value)

        def _setPWMB(self, value):
                self.PWMB.ChangeDutyCycle(value)

        def _setMotor(self, value, IN1, IN2, PWM):
                if(value >= 0):
                        GPIO.output(IN1,GPIO.HIGH)
                        GPIO.output(IN2,GPIO.LOW)
                else:
                        GPIO.output(IN1,GPIO.LOW)
                        GPIO.output(IN2,GPIO.HIGH)
                        value = -value
                PWM.ChangeDutyCycle(value)

        def _setMotorA(self, target):
                PA = max(target, self.motor_min)
                PA = min(target, self.motor_max)
                self._setMotor(PA, self.AIN1, self.AIN2, self.PWMA)

        def _setMotorB(self, target):
                PB = max(target, self.motor_min)
                PB = min(target, self.motor_max)
                self._setMotor(PB, self.BIN1, self.BIN2, self.PWMB)


        def setMotors(self, left, right):
                self._setMotorA(left)
                self._setMotorB(right)

        def stop(self):
                self._setMotor(0, self.AIN1, self.AIN2, self.PWMA)
                self._setMotor(0, self.BIN1, self.BIN2, self.PWMB)
                
                
        def testForward(self):
                self.setMotors(100, 100)
                time.sleep(1)
                self.stop()
                time.sleep(1)
        
        def testLeft(self):
                self.setMotors(-100, 100)
                time.sleep(1)
                self.stop()
                time.sleep(1)
        
        def testRight(self):
                self.setMotors(100, -100)
                time.sleep(1)
                self.stop()
                time.sleep(1)
        
        def testBack(self):
                self.setMotors(-100, -100)
                time.sleep(1)
                self.stop()
                time.sleep(1)
                

if __name__=='__main__':

        controler = MotorControl()
        try:
                while True:
                        controler.testForward()
                        controler.testLeft()
                        controler.testRight()
                        controler.testBack()

        except KeyboardInterrupt:
                GPIO.cleanup()
