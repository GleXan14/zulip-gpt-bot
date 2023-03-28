
import openai
import zulip


# Set up OpenAI API credentials
openai.api_key = "YOUR_OPENAI_API_KEY"

# Set up Zulip API client
client = zulip.Client(config_file="~/zuliprc", client="bot")

# Define a function to handle incoming messages
def handle_message(msg):
    # Check if message is a private message
    if msg["type"] == "private":
        # Get the message content
        content = msg["content"]

        messages=[
            {
                "role":"user",
                "content":content
            }
        ]
        
        # Call the OpenAI API to generate a response
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.9
        )

        # Send the response back to the user
        client.send_message(
            {
                "type": "private",
                "to": msg["sender_email"],
                "content": response["choices"][0]["message"]["content"]
            }
        )

# Call the 'register' endpoint to start receiving messages
client.call_on_each_message(handle_message)