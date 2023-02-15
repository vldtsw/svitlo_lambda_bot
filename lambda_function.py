import json
import os
import sys
import ipaddress
import requests

# Get the path of the current file and append the vendored folder to the system path
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

# Retrieve the Telegram Bot API token from the environment variables
TOKEN = os.environ["TELEGRAM_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def lambda_handler(event, context):
    try:
        # Load the request body as a JSON object
        data = json.loads(event["body"])

        if "callback_query" in data:
            # Get the callback query data
            callback_data = data["callback_query"]["data"]
            chat_id = data["callback_query"]["message"]["chat"]["id"]
            message_id = data["callback_query"]["message"]["message_id"]

            response = f"Callback data received {callback_data=}"
            data = {
                "text": response.encode("utf8"),
                "chat_id": chat_id,
                "message_id": message_id,
            }

            url = BASE_URL + "/editMessageText"

            # Send the updated response back to the user
            requests.post(url=url, data=data)

        elif "message" in data:
            # Get the text of the message and the chat ID
            message = str(data["message"]["text"])
            chat_id = data["message"]["chat"]["id"]
            first_name = data["message"]["chat"]["first_name"]

            # Check if the message starts with the word "ping"
            if message.startswith("ping "):
                # Split the message into words and get the second word (the IP address and port)
                ip_port = message.split()[1]

                # Try to validate the IP address
                try:
                    ip = ip_port.split(":")[0]
                    ipaddress.ip_address(ip)

                    keyboard = {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "Update",
                                    "callback_data": f"update {ip_port}"
                                }
                            ]
                        ]
                    }

                    # Try to make a head request to the URL using the IP address and port
                    try:
                        resp = requests.head(url=f"http://{ip_port}", timeout=5)
                        response = f"IP address is reachable (:\n" \
                                   f"Status code: {resp.status_code}"

                    except Exception:
                        response = f"IP address is not reachable ):"
                        keyboard = None

                except ValueError:
                    response = "Invalid <IP address>:<port>"
                    keyboard = None

            # If the message starts with "/start"
            elif message.startswith("/start"):
                response = (
                    f"Hello, {first_name}!\n"
                    f"I am a simple bot that can ping an IP address.\n"
                    f"Please, send me a message in the following format:\n"
                    f"ping <IP address>:<port>"
                )
                keyboard = None

            # If the message doesn't match either "ping" or "start"
            else:
                response = "Send message in format 'ping <IP address>:<port>'"
                keyboard = None

            # Prepare the data to send to the Telegram API
            data = {
                "text": response.encode("utf8"),
                "chat_id": chat_id,
                "reply_markup": json.dumps(keyboard) if keyboard else None
            }
            url = BASE_URL + "/sendMessage"

            # Send the response back to the user
            requests.post(url=url, data=data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}
