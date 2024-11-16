from .ar import messages as ar_messages
from .en import messages as en_messages


def message_locale(key, language='en'):
    """
    Return the translated message for the given key and language.

    Args:
        key (str): The key of the message to be translated.
        language (str): The language code of the message to be translated.

    Returns:
        str: Retrieve message by key and language.
    """
    language = language.lower()
    if language == 'ar':
        return ar_messages.get(key, en_messages.get(key, ""))
    else:
        return en_messages.get(key, "")