import unittest
import sys

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
	room = Room(room_name="Tyler's Room")
	room2 = Room(room_name="Austin's Room")
	db.session.add(room)
	db.session.add(room2)

	rgb_led = RGBLed(
		id=1, 
		device_name="LED Strip1",
		type='rgbleds',
		red=0,
		green=0,
		blue=0
	)
	rgb_led2 = RGBLed(
		id=3, 
		device_name="LED Strip2",
		type='rgbleds',
		red=0,
		green=0,
		blue=0
	)
	led = SimpleDevice(id=2, device_name="LED1", type='simpledevices')

	room.devices.append(rgb_led)
	room.devices.append(led)
	room2.devices.append(rgb_led2)
	db.session.commit()

@cli.command()
def test():
	tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)

	if result.wasSuccessful():
		return 0
	sys.exit(result)


	

if __name__ == '__main__':
	cli()
