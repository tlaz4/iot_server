import unittest
import json

from app.tests.base import BaseTestCase
from app import db
from app.tests.utils import create_room, create_simple_device, create_rgb_device

class TestRoomService(BaseTestCase):
	"""Test the room service"""

	def test_get_room(self):
		room = create_room()

		with self.client:
			response = self.client.get('/api/rooms/1')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertEqual(1, data['data']['id'])
			self.assertEqual('Living Room', data['data']['room_name'])
			self.assertIn('success', data['status'])

	def test_invalid_room(self):
		with self.client:
			response = self.client.get('api/rooms/2')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 404)
			self.assertIn('fail', data['status'])

	def test_get_all_rooms(self):
		room1 = create_room()
		room2 = create_room(room_name="Kitchen")

		with self.client:
			response = self.client.get('api/rooms')
			data = json.loads(response.data.decode())

			self.assertEqual(response.status_code, 200)
			self.assertEqual(len(data['data']['rooms']), 2)
			self.assertEqual(data['data']['rooms'][0]['room_name'], 'Living Room')
			self.assertEqual(data['data']['rooms'][1]['room_name'], 'Kitchen')
			self.assertIn('success', data['status'])

class TestDeviceService(BaseTestCase):
	"""Test the device service"""

	def test_get_device(self):
		device = create_simple_device()

		with self.client:
			response = self.client.get('api/devices/2')
			data = json.loads(response.data.decode())

			self.assertEqual(response.status_code, 200)
			self.assertEqual(2, data['data']['id'])
			self.assertEqual('LED1', data['data']['device_name'])
			self.assertEqual('simpledevices', data['data']['type'])
			self.assertIn('success', data['status'])

	def test_get_invalid_device(self):
		with self.client:
			response = self.client.get('api/devices/2')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 404)
			self.assertIn('fail', data['status'])


	def test_patch_device(self):
		device = create_rgb_device()
		patch_data = {'red': 225}

		with self.client:
			response = self.client.patch(
				'/api/devices/1',
				data=json.dumps(patch_data),
				content_type='application/json'
			)
			response_data = json.loads(response.data.decode())

			self.assertEqual(response_data['data']['device_name'], 'LED Strip1')
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response_data['data']['red'], 225)
			self.assertEqual('rgbleds', response_data['data']['type'])
			self.assertIn('success', response_data['status'])

	def test_patch_device_invalid_attribute(self):
		device = create_rgb_device()
		patch_data = {'purple': 225}

		with self.client:
			response = self.client.patch(
				'/api/devices/1',
				data=json.dumps(patch_data),
				content_type='application/json'
			)
			response_data = json.loads(response.data.decode())

			self.assertEqual(response.status_code, 400)
			self.assertIn('fail', response_data['status'])
			self.assertIn('Attribute does not exist', response_data['message'])


