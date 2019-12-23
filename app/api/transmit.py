import sys
import json
import subprocess
#import RPi.GPIO as GPIO

# this should handle device id in addition to needed data
class TransmitInterface:

	def __init__(self):
		self.protocols = {
			'simpledevices': self.simple_device_protocol,
			'rgbleds': self.rgbled_protocol
		}

	def simple_device_protocol(self, data):
		# GPIO.setwarnings(False)
		# GPIO.setmode(GPIO.BCM)

		# # turn on device depending on status
		# # if status is set to true, also check for timer
		# # attribute, execute script to turn off device depending on timer
		# #TODO add check timer attribute
		# if(data['status']):
		# 	GPIO.setup(27, GPIO.OUT)
		# 	GPIO.output(27, GPIO.LOW)
		# 	subprocess.call(["at", "now", "+", "2", "hours", "-f", "commands/radio.sh"])
		# else:
		# 	GPIO.setup(27, GPIO.OUT)
		# 	GPIO.output(27, GPIO.LOW)
		# 	GPIO.cleanup()

		pass
			

	def rgbled_protocol(self, data):
		if not data['status']:
			data['red'], data['green'], data['blue'] = 0, 0, 0

		tx_data = self.format_data(data)
		

	def init_protocol(self, type, data):
		return self.protocols[type](data)

	def format_data(self, data):
		tx_data = 0

		# format device into data
		tx_data |= data['id']
		# format pattern into data
		tx_data |= data['pattern'] << 4
		# format colour into data
		tx_data |= data['red'] << 8
		tx_data |= data['green'] << 16
		tx_data |= data['blue'] << 24

		return tx_data


def main():
	if len(sys.argv) != 3:
		print("Please enter the device type followed by the data to be transmitted!")
		sys.exit(0)

	transmit_interface = TransmitInterface()
	transmit_interface.init_protocol(sys.argv[1], json.loads(sys.argv[2]))

if __name__ == '__main__':
	main() 
