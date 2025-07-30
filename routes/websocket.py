from flask import Blueprint
from flask_socketio import emit, join_room, leave_room
from app import socketio

websocket_bp = Blueprint('websocket', __name__)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'message': 'Connected to analysis server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_analysis')
def handle_join_analysis(data):
    analysis_id = data.get('analysis_id')
    if analysis_id:
        join_room(analysis_id)
        emit('joined_analysis', {'analysis_id': analysis_id})

@socketio.on('leave_analysis')
def handle_leave_analysis(data):
    analysis_id = data.get('analysis_id')
    if analysis_id:
        leave_room(analysis_id)
        emit('left_analysis', {'analysis_id': analysis_id})
