import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from livekit.api.access_token import AccessToken, VideoGrants

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get LiveKit credentials from environment variables
LIVEKIT_API_KEY = "API5SYhjVAN6Mww"  #os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = "SZqfJjMXqMOfxQNqtrvOnRt8KrjXerEqhWTro4i6fBDB"  #os.getenv('LIVEKIT_API_SECRET')
LIVEKIT_URL = "wss://live-voice-assistant-hbk7eu87.livekit.cloud" #os.getenv('LIVEKIT_URL')

@app.route('/get-token', methods=['GET'])
def get_token():
    """
    Generate a LiveKit token for a participant to join a room.

    Query parameters:
    - room: The room name to join
    - identity: (Optional) The participant's identity, defaults to a random UUID
    - name: (Optional) The participant's display name
    """
    try:
        # Get parameters from the request
        room = request.args.get('room')
        identity = request.args.get('identity', f'user-{uuid.uuid4().hex[:8]}')
        name = request.args.get('name', 'User')

        # Validate required parameters
        if not room:
            return jsonify({'error': 'Room name is required'}), 400

        # Create a new access token
        token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)

        # Set token identity and name
        token = token.with_identity(identity)
        token = token.with_name(name)

        # Grant permissions to join the room
        grants = VideoGrants(
            room_join=True,
            room=room,
            can_publish=True,
            can_subscribe=True
        )
        token = token.with_grants(grants)

        # Generate the JWT token
        jwt = token.to_jwt()

        return jsonify({
            'accessToken': jwt,
            'identity': identity,
            'name': name,
            'room': room
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = '9000' #int(os.getenv('PORT', 8080))
    app.run(host='127.0.0.1', port=port, debug=True)
