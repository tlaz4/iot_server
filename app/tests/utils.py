from app.api.models import Device, Room, SimpleDevice, RGBLed
from app import db

def create_room(room_name="Living Room"):
	room = Room(room_name=room_name)
	db.session.add(room)
	db.session.commit()

	return room

def create_simple_device():
	room = create_room()
	led = SimpleDevice(id=2, device_name="LED1", type='simpledevices')
	room.devices.append(led)

	db.session.commit()

	return led

def create_rgb_device():
	room = create_room()

	rgb_led = RGBLed(
		id=1, 
		device_name="LED Strip1",
		type='rgbleds',
		red=0,
		green=0,
		blue=0
	)
	room.devices.append(rgb_led)

	db.session.commit()

	return rgb_led