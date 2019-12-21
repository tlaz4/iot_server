from app import db

class Room(db.Model):
	__tablename__ = 'rooms'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	room_name = db.Column(db.String(64), unique=True)
	devices = db.relationship('Device', backref='room', lazy=True, cascade='all')

	def to_json(self):
		return {
			'id': self.id,
			'room_name': self.room_name,
			'devices': [device.to_json() for device in self.devices]
		}
	
class Device(db.Model):
	__tablename__ = 'devices'

	id = db.Column(db.Integer, primary_key=True)
	device_name = db.Column(db.String(64), unique=True)
	type = db.Column(db.String(50))
	status = db.Column(db.Boolean, default=False)
	room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
	 
	__mapper_args__ = {
		'polymorphic_identity': 'devices',
		'polymorphic_on' : type
	}	

class SimpleDevice(Device):
	__tablename__ = 'simpledevices'

	device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), primary_key=True)

	__mapper_args__ = {
		'polymorphic_identity': 'simpledevices'	
	}

	def to_json(self):
		return {
			'id': self.id,
			'device_name': self.device_name,
			'type': self.type,
			'status': self.status,
		}

class RGBLed(Device):
	__tablename__ = 'rgbleds'	

	device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), primary_key=True)
	red = db.Column(db.Integer)
	green = db.Column(db.Integer)
	blue = db.Column(db.Integer)

	__mapper_args__ = {
		'polymorphic_identity': 'rgbleds'
	}

	def to_json(self):
		return {
			'id': self.id,
			'device_name': self.device_name,
			'type': self.type,
			'status': self.status,
			'red': self.red,
			'green': self.green,
			'blue': self.blue
		}
