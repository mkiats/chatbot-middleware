def callback_data_chatbot(chatbot_uuid: str):
    return {
        'command': 'command_callback_selectChatbot',
        'chatbot_uuid': chatbot_uuid
    }

def inline_keyboard_button(text: str, callback_data: str = None) -> object:
    json_obj = {
        'text': text,
        'callback_data': text
    }
    return json_obj