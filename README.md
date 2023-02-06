A simple telegram bot that checks the status of electricity in a house by pinging the IP address and port.

### Usage
To use the bot, send a message in the following format:

`ping <IP address>:<port>`

If the IP address and port are reachable, the bot will return a response indicating the status code.
If the message starts with "/start", the bot will return a greeting and a brief explanation of its functionality.

### Set up

1. Clone the repository
`git clone https://github.com/YOUR-USERNAME/electricity-status-bot.git`

2. Add the Telegram Bot API token to the environment variables.
3. Install the required packages by running:
`pip install -r requirements.txt`
4. Deploy the bot to AWS Lambda platform.
5. Start using the bot by sending messages to it in Telegram.

### Contributing
Feel free to fork the repository and submit a pull request with any improvements or bug fixes.