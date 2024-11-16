from flask import request, jsonify
from sqlalchemy.orm import subqueryload

from app.models import Chat
from localization import message_locale

def chat_history():
    """
    This endpoint returns the chat history for a given customer.

    Parameters:
        chat_uuid (str): The UUID of the chat to retrieve the history for.

    Returns:
        A JSON response containing the chat history for the customer.
    """
    chat_uuid = request.args.get('uuid')
    print(f"Received chat UUID: {chat_uuid}")

    # Validate request data
    if not chat_uuid:
        return jsonify({"error": message_locale("MISSING_REQUIRED_FIELDS")}), 400

    # Retrieve chat history with messages in one query
    chat_history = Chat.query \
        .filter_by(uuid=chat_uuid) \
        .options(subqueryload(Chat.messages)) \
        .all()
    

    # Check if chat history is empty
    if len(chat_history) == 0:
        return jsonify({"error": message_locale("NO_CHAT_FOUND", "en")}), 404
    
    # Structure the response
    history = [
        {
            "chat_uuid": chat.uuid,
            "messages": [
                {
                    "message_id": message.id,
                    "message": message.message,
                    "is_bot": message.is_bot,
               }
                for message in chat.messages
            ]

        }
        for chat in chat_history
    ]

    return jsonify(history), 200
