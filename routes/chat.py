import uuid 

from flask import request, jsonify
from app.models import Chat, Customer, ChatMessage, db
from localization import message_locale
from utilities.responses import Message, Option, ReplyResponse

# Helper function to fetch a customer by device ID
def get_customer_by_device_id(device_id):
    return Customer.query.filter_by(device_id=device_id).first()


# Save a message to the ChatMessage table
def save_chat_message(chat_uuid, message, is_bot=True):
    if chat_uuid and message:
        chat_message = ChatMessage(
            chat_uuid=chat_uuid,
            message=message,
            is_bot=is_bot
        )
        db.session.add(chat_message)
        db.session.commit()

# Helper function to create a new chat
def create_new_chat(customer):

    new_chat = Chat(
        uuid=str(uuid.uuid4()),
        customer_id=customer.id,
        classification=None,
        additional_data={},
    )
    db.session.add(new_chat)
    db.session.commit()
    return new_chat

# Helper function to build the response object
def build_reply_response(chat_uuid, bot_message, options=[]):

    return ReplyResponse(
        messages=[Message(type="text", content=bot_message)],
        chat_uuid=chat_uuid,
        options_type="switch",
        options=options,
        is_chat_ended=False,
        filters={},
        limit=None
    )

# Start a new chat
def chat():
    data = request.get_json()
    device_id = data.get('device_id')
    language = data.get('language', 'en')

    # Validate request data
    if not device_id:
        return jsonify({"error": message_locale("MISSING_REQUIRED_FIELDS", language)}), 400

    # Check if user exists
    customer = get_customer_by_device_id(device_id)
    if not customer:
        customer = Customer(
            device_id=device_id,
        )
        db.session.add(customer)
        db.session.commit()
        # return jsonify({f"error": "New User Created With Device ID {device_id}"}), 201

    # Always start a new chat
    new_chat = create_new_chat(customer)

    # Fetch localized message for the bot
    bot_message = message_locale("START_MESSAGE", language)
    save_chat_message(new_chat.uuid, bot_message, is_bot=True)

    # Build response
    options = [
        Option(content=message_locale("OPTION_PROPERTY_INVESTOR", language), id=1, is_selected=False),
        Option(content=message_locale("OPTION_HOME_BUYER", language), id=2, is_selected=False)
    ]
    response = build_reply_response(new_chat.uuid, bot_message, options)

    # Commit all changes at once for efficiency
    db.session.commit()

    return jsonify(response.dict()), 201
