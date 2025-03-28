from flask import Flask
from flask_cors import CORS
from flask_sse import sse
from flask_migrate import Migrate
from models import db  # Import after app is defined

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Load configuration correctly
from config import Config
app.config.from_object(Config)

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Import and register authentication system
import auth  

# Register API Blueprint
from api import api_bp
app.register_blueprint(api_bp)  # This is the missing part!

# Register Server-Sent Events (SSE) Blueprint
app.register_blueprint(sse, url_prefix='/stream')

# Initialize cache
from cache import cache
cache.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
