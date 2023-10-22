import openai
import argparse

def main():
    parser = argparse.ArgumentParser(description="Query OpenAI Completion API")
    parser.add_argument("--changelog", help="The CHANGELOG to summarize")
    parser.add_argument("--api-key", help="The OpenAI API key")

    args = parser.parse_args()

    openai.api_key = args.api_key

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarise the next git commit log in a friendly human-readable way, max two sentences."},
            {"role": "user", "content": args.changelog}
        ])

    # Get the completion response from the API
    completion_response = completion.choices[0].message.content

    
    # Return the completion response to the invoker
    print(completion_response)

if __name__ == "__main__":
    main()