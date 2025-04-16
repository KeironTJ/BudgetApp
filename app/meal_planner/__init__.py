from flask import Blueprint

bp = Blueprint('meal_planner', __name__)

from app.meal_planner import routes