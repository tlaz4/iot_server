from flask import Blueprint
from flask_restful import Resource, Api
from app import db
from app.api.models import Room

room_blueprint = Blueprint('room', __name__)
api = Api(room_blueprint)

class Rooms(Resource):

	def get(self, room_id):
		room = Room.query.filter_by(id=room_id).first()

		if not room:
			response_object = {'status': 'fail', 'message': 'Room does not exist!'}
			return response_object, 404

		else:
			response_object = {'status': 'success', 'data': room.to_json()}
			return response_object, 200

class RoomList(Resource):

	def get(self):
		rooms = Room.query.all()

		response_object = {
			'status': 'success',
			'data': {
				'rooms': [room.to_json() for room in rooms]
			}
		}
		return response_object, 200

api.add_resource(Rooms, '/api/rooms/<room_id>')
api.add_resource(RoomList, '/api/rooms')

