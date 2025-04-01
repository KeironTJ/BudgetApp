import os
import eventlet.wsgi
from app import create_app, socketio
from dotenv import load_dotenv

load_dotenv()
app = create_app()

if __name__ == '__main__':
    print("FLASK_ENV:", os.getenv("FLASK_ENV"))

    if os.getenv('FLASK_ENV') == 'development':
        print("NOW IN DEVELOPMENT")
        socketio.run(app, debug=True, log_output=True, allow_unsafe_werkzeug=True)  # Uses Flask-SocketIO’s built-in support for Eventlet
        
    else:
        print("NOW IN PRODUCTION")
        eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)  # Uses Eventlet’s server directly in production