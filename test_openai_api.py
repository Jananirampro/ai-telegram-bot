import openai

openai.api_key = "<your api key>"  # Your actual key here

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, can you hear me?"}
        ]
    )
    print("✅ API call succeeded.")
    print("Bot reply:", response['choices'][0]['message']['content'])

except Exception as e:
    print("❌ Error calling OpenAI API:")
    print(e)
