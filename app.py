from google import genai

def example():
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Hello, Gemini!",
    )
    print(response.text)

if __name__ == '__main__':
    example()