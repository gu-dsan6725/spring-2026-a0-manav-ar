import os

from groq import Groq

from ec2_metadata import (
    fetch_all_ec2_metadata,
    print_ec2_metadata,
)


def _get_ai_response() -> object:
    """Get AI response from Groq."""
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models, what is the future of ai and beyond",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion


def _print_ai_response(
    chat_completion: object,
) -> None:
    """Print AI response and metadata."""
    print("=" * 80)
    print("AI RESPONSE:")
    print("=" * 80)
    print(chat_completion.choices[0].message.content)
    print("\n" + "=" * 80)
    print("AI METADATA:")
    print("=" * 80)
    print(f"Model: {chat_completion.model}")
    print(f"Finish Reason: {chat_completion.choices[0].finish_reason}")
    print(f"Total Tokens: {chat_completion.usage.total_tokens}")
    print(f"Prompt Tokens: {chat_completion.usage.prompt_tokens}")
    print(f"Completion Tokens: {chat_completion.usage.completion_tokens}")
    print("=" * 80)


def main() -> None:
    """Main entry point."""
    ec2_metadata = fetch_all_ec2_metadata()

    chat_completion = _get_ai_response()

    _print_ai_response(chat_completion)
    print_ec2_metadata(ec2_metadata)


if __name__ == "__main__":
    main()
