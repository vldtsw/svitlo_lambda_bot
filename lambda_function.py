import json
import os
import sys
import ipaddress
import requests

# Get the path of the current file and append
# the vendored folder to the system path
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

# Retrieve the Telegram Bot API token from the environment variables
TOKEN = os.environ["TELEGRAM_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_response(response, chat_id, keyboard=None, message_id=None):
    # Prepare the data to send to the Telegram API
    data = {
        "text": response.encode("utf8"),
        "chat_id": chat_id,
    }

    # Add the inline keyboard to the data, if specified
    if keyboard is not None:
        data["reply_markup"] = json.dumps(keyboard)

    # If a message ID is specified, use the editMessageText API
    # method to update the message
    if message_id is not None:
        data["message_id"] = message_id
        url = BASE_URL + "/editMessageText"
    # Otherwise, use the sendMessage API method to send a new message
    else:
        url = BASE_URL + "/sendMessage"

    # Send the data to the Telegram API
    requests.post(url=url, data=data)


def create_keyboard(ip_port, status):
    return {
        "inline_keyboard": [
            [
                {
                    "text": "Update",
                    "callback_data": f"{status} {ip_port}"
                }
            ]
        ]
    }


def handle_callback_query(data):
    # Get the callback query data
    callback_data = data["callback_query"]["data"]
    chat_id = data["callback_query"]["message"]["chat"]["id"]
    message_id = data["callback_query"]["message"]["message_id"]

    response, keyboard = handle_ping_command(message=callback_data)

    send_response(
        response=response, chat_id=chat_id, message_id=message_id, keyboard=keyboard
    )


def ping(ip_port):
    # Try to make a head request to the URL using the IP address and port
    try:
        resp = requests.head(url=f"http://{ip_port}", timeout=3)
        response = f"IP address is reachable 💡\n" \
                   f"Status code: {resp.status_code}"
        status = "up"

    except Exception:
        response = "IP address is not reachable ⬛"
        status = "down"

    return response, status


def handle_ping_command(message):
    # Split the message into words and get the second word
    # (the IP address and port)
    ip_port = message.split()[1]
    # Try to validate the IP address
    try:
        ip = ip_port.split(":")[0]
        ipaddress.ip_address(ip)

        response, status = ping(ip_port=ip_port)

        # if "up " in message:
        #     response = ""
        # elif "down " in message:
        #     response = ""
        # todo: add responses "now reachable" and "became unreachable"

        keyboard = create_keyboard(ip_port=ip_port, status=status)

    except ValueError:
        response = "Invalid <IP address>:<port>"
        keyboard = None

    return response, keyboard


def handle_start_command(first_name):
    response = (
        f"Hello, {first_name}!\n"
        f"I am a simple bot that can ping an IP address.\n"
        f"Please, send me a message in the following format:\n"
        f"ping <IP address>:<port>"
    )
    keyboard = None
    return response, keyboard


def handle_default_message():
    response = "Send message in format 'ping <IP address>:<port>'"
    keyword = None
    return response, keyword


def handle_message(data):
    # Get the text of the message and the chat ID
    message = data["message"]["text"]
    chat_id = data["message"]["chat"]["id"]
    first_name = data["message"]["chat"]["first_name"]

    # Check if the message starts with the word "ping"
    if message.startswith("ping "):
        response, keyboard = handle_ping_command(message=message)

    # If the message starts with "/start"
    elif message.startswith("/start"):
        response, keyboard = handle_start_command(first_name)

    # If the message doesn't match either "ping" or "start"
    else:
        response, keyboard = handle_default_message()

    send_response(response=response, chat_id=chat_id, keyboard=keyboard)


def lambda_handler(event, context):
    try:
        # Load the request body as a JSON object
        data = json.loads(event["body"])

        if "message" in data:
            handle_message(data)

        elif "callback_query" in data:
            handle_callback_query(data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}
