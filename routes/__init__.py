from flask import Blueprint
from .reply import reply
from .chat import chat
from .chat_history import chat_history
from .create_user import create_user

main = Blueprint('main', __name__)

# Register routes
main.route('/reply', methods=['POST'])(reply)
main.route('/chat', methods=['POST'])(chat)
main.route('/chat_history', methods=['GET'])(chat_history)
main.route('/create_user', methods=['POST'])(create_user)
