import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'development':
        app.run()
    else:
        # Add any production-specific settings, if needed
        app.run()
