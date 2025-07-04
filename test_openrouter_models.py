import openai

openai.api_key = "apikey"  # Replace with your OpenRouter key
openai.api_base = "https://openrouter.ai/api/v1"

for model in ["openrouter/cypher-alpha:free", "openrouter/optimus-alpha:free"]:
    print(f"\nTesting {model} ...")
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": "Hello from OpenRouter!"}
            ]
        )
        print("✅ Success:", resp.choices[0].message.content[:100])
    except Exception as e:
        print("❌ Error:", e)
