from flask import Blueprint

bp = Blueprint('activity_planner', __name__)

from app.activity_planner import routes