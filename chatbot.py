import openai
def bot():
    # Set your OpenAI API key
    mykey = "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"
    openai.api_key = mykey
    while True:
            # Create the message input for OpenAI Chat API
            msg = input("enter 'q' to quit> ")
            if msg == "q":
                break
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": msg}
            ]

            # Call OpenAI Chat API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature = 1.2
            )

            # Get the generated response from OpenAI
            text1 = response.choices[0].message.content

            # Print and speak the recognized text and the generated response
            print("< ", text1)