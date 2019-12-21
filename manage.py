from flask.cli import FlaskGroup

from app import create_app, db
from app.api.models import Room, SimpleDevice, RGBLed

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
	"""
	Recreate the database
	"""
	db.drop_all()
	db.create_all()
	db.session.commit()

@cli.command('seed_db')
def seed_db():
	room = Room(room_name="Living Room")
	db.session.add(room)

	rgb_led = RGBLed(
		id=1, 
		device_name="LED Strip1",
		type='rgbleds',
		red=0,
		green=0,
		blue=0
	)
	led = SimpleDevice(id=2, device_name="LED1", type='simpledevices')

	room.devices.append(rgb_led)
	room.devices.append(led)
	db.session.commit()

	

if __name__ == '__main__':
	cli()
