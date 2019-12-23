class TransmitInterface:

	def __init__(self):
		self.protocols = {
			'simpledevices': self.simple_device_protocol,
			'rgbleds': self.simple_device_protocol
		}

	def simple_device_protocol(self, data):
		print(data)

	def rgbled_protocol(self, data):
		print(data)

	def init_protocol(self, type, data):
		return self.protocols[type](data)
