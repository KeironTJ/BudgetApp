from flask import Blueprint, render_template
from flask_limiter.errors import RateLimitExceeded

bp = Blueprint('main', __name__)

@bp.app_errorhandler(RateLimitExceeded)
def handle_ratelimit_error(error):
	retry_after = getattr(error, 'description', None)
	retry_after = getattr(error, 'retry_after', None)
	retry_header = str(int(retry_after)) if isinstance(retry_after, (int, float)) else '60'
	reset_in = getattr(error, 'reset_in', None)
	limit_value = getattr(getattr(error, 'limit', None), 'limit', '')

	return (
		render_template(
			'main/429.html',
			title='Slow down',
			limit=str(limit_value),
			reset_in=reset_in,
		),
		429,
		{
			'Retry-After': retry_header,
		},
	)

from app.main import routes