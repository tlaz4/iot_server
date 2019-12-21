import RPi.GPIO as GPIO
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

if sys.argv[1] == "on":
	GPIO.setup(27, GPIO.OUT)
	GPIO.output(27, GPIO.LOW)
elif sys.argv[1] == "off":
	GPIO.setup(27, GPIO.OUT)
	GPIO.output(27, GPIO.HIGH)
	GPIO.cleanup()
