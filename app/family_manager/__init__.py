from flask import Blueprint

bp = Blueprint('family_manager', __name__)

from app.family_manager import routes