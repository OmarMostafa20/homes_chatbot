from flask import request, jsonify
from sqlalchemy.orm.attributes import flag_modified
from app.models import Chat, ChatMessage, db
from services.agent import process_agent
from utilities.responses import Message, ReplyResponse
from localization import message_locale
from data.locations import fetch_sub_locations_by_id

def save_messages(chat_uuid, messages):
    """Save chat messages to the database."""
    if chat_uuid and messages:
        chat_messages = [
            ChatMessage(
                chat_uuid=chat_uuid,
                message=msg['text'],
                is_bot=msg['is_bot']
            ) for msg in messages
        ]
        db.session.bulk_save_objects(chat_messages)
        db.session.commit()

def update_chat_additional_data(chat, data):
    """Update chat's additional data and flag it as modified, merging list filters if needed."""
    chat.additional_data = chat.additional_data or {}

    # Handle merging of filters specifically for consideration_id and property_type_id
    existing_filters = chat.additional_data.get('filters', {})
    new_filters = data.get('filters', {})

    if existing_filters:
        for key in ['consideration_id', 'property_type_id', 'amenity_id']:
            if key in existing_filters and key in new_filters:
                existing_filters[key] = list(set(existing_filters[key] + new_filters[key]))
            elif key in new_filters and key not in existing_filters:
                existing_filters[key] = new_filters[key]

        # Updating the rest of the keys (non-list values)
        existing_filters.update({k: v for k, v in new_filters.items() if k not in ['consideration_id', 'property_type_id', 'amenity_id']})
    else:
        existing_filters = new_filters

    # Update the filters in additional_data
    chat.additional_data['filters'] = existing_filters
    flag_modified(chat, 'additional_data')
    db.session.commit()


def create_response(messages, chat_uuid, options_type=None, options=None,
                    is_chat_ended=False, filters=None):
    """Create and return a bot response."""
    response = ReplyResponse(
        messages=messages,
        chat_uuid=chat_uuid,
        options_type=options_type,
        options=options or [],
        is_chat_ended=is_chat_ended,
        filters=filters or {},
        limit=None
    )
    return jsonify(response.dict()), 200


def reply():
    """Handle bot reply."""
    # Get request data
    data = request.json
    chat_uuid = data.get('chat_uuid')
    user_message = data.get('message')

    # Validate request data
    if not chat_uuid or not user_message:
        return jsonify({"error": message_locale("MISSING_REQUIRED_FIELDS")}), 400

    # Retrieve the chat from the database
    chat = Chat.query.filter_by(uuid=chat_uuid).first()
    if not chat:
        return jsonify({"error": message_locale("NO_CHAT_FOUND")}), 404

    # Check if the chat is ended
    if chat.current_state == "done":
        bot_message = Message(type="text", content=message_locale("CHAT_ALREADY_ENDED"))
        return create_response(messages=[bot_message], chat_uuid=chat.uuid, is_chat_ended=True, filters=chat.additional_data.get('filters', {}))

    if user_message.lower() == "show recommendations":
        bot_message = Message(type="text", content=message_locale("RECOMMENDATIONS_MESSAGE"))
        return create_response(messages=[bot_message], chat_uuid=chat.uuid, is_chat_ended=True, filters=chat.additional_data.get('filters', {}))
    
    # Process the agent's response using chat_uuid and user_message
    agent_output = process_agent(chat_uuid, user_message)

    # Parse the agent's response
    bot_message_content = agent_output.get('messages', [])
    options = agent_output.get('options', [])
    is_chat_ended = agent_output.get('is_chat_ended', False)
    filters = agent_output.get('filters', {})
    options_type = agent_output.get('options_type')

    print(f" filters from agent {filters}")

    sub_locations = []
    for message in bot_message_content:
        if message.get("type") == "region":
            location_id = message.get("content")

            sub_locations = fetch_sub_locations_by_id(location_id)
            filters["location_id"] = sub_locations
            break

    # Save the user's message and the agent's response
    save_messages(chat.uuid, [
        {'text': user_message, 'is_bot': False},
        *[
            {'text': msg['content'], 'is_bot': True} for msg in bot_message_content
        ]
    ])

    # Build the bot message
    bot_messages = [
        Message(type=msg['type'], content=msg['content']) for msg in bot_message_content
    ]

    # Update chat state and additional data if provided
    if filters:
        update_chat_additional_data(chat, {'filters': filters})

    if is_chat_ended:
        chat.current_state = "done"
        db.session.commit()

    # Return the response
    return create_response(
        messages=bot_messages,
        chat_uuid=chat.uuid,
        options_type=options_type,
        options=options,
        is_chat_ended=is_chat_ended,
        filters=chat.additional_data.get('filters', {})
    )
