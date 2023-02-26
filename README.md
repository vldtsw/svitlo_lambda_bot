This is a simple Python Telegram bot that checks the status of an IP address and port to help you determine if there is electricity in your home. The bot can be set up on AWS Lambda platform and uses webhooks to receive and respond to messages sent via Telegram - https://t.me/lambdatest_bot
### Usage
To use the bot, you need to send a message in the following format:

`ping <IP address>:<port>`

When you send this message, the bot will respond with the status code of the IP address and port specified in the message. If the IP address and port are reachable, the bot will return a success response. If the IP address and port are not reachable, the bot will return an error response.

If the message starts with "/start", the bot will return a greeting and a brief explanation of its functionality.

### Set up

1. Clone the repository
`git clone https://github.com/vldtsw/svitlo_lambda_bot`

2. Install the required packages by running:
`pip install -r requirements.txt`
3. Obtain your Telegram Bot API token and add it to the AWS Lambda environment variables by following these steps:
   1. Go to the BotFather in Telegram and create a new bot by following the instructions. 
   2. Once your bot is created, BotFather will provide you with a token. Copy this token and keep it safe. 
   3. Go to the AWS Management Console and navigate to the AWS Lambda service. 
   4. Create a new Lambda function and give it a name. 
   5. Under "Function code", upload the project code by selecting the ZIP file or uploading the files directly. 
   6. Under "Environment variables", click on "Edit". 
   7. Add a new environment variable called "TELEGRAM_BOT_TOKEN" and set its value to the token you obtained from BotFather. 
   8. Click on "Save".

4. Deploy the bot to AWS Lambda platform and configure webhook:
   1. In the AWS Lambda function page, click on "Add trigger" and select "API Gateway" as the trigger type. 
   2. Choose "REST API" and "Create an API". 
   3. Choose "Open" for the security option. 
   4. Click on "Add". 
   5. In the API Gateway page, select the created API and click on "Create Resource". 
   6. Enter a name for the resource, e.g. "telegram-bot". 
   7. Click on "Create Method" and select "POST". 
   8. Select "Lambda Function" as the integration type and choose your Lambda function. 
   9. Click on "Save". 
   10. In the "Integration Request" section, click on "Mapping Templates". 
   11. Add a new mapping template with the content type "application/json" and the following template:`{"body": $input.json('$')}`
   12. Click on "Save". 
   13. Deploy the API by selecting the resource and clicking on "Deploy API". Choose a deployment stage, e.g. "prod". 
   14. Copy the URL of the deployed API.
5. Start using the bot by sending messages to it in Telegram:
   1. Open the Telegram app and search for your bot using its username. 
   2. Send a message to the bot in the following format: ping <IP address>:<port>.
   3. If the IP address and port are reachable, the bot will respond with a success message. If they are not reachable, the bot will respond with an error message.

That's it! You now have a fully functional Python Telegram bot deployed on AWS Lambda platform.