import openai

# Load your OpenAI API key from environment or configuration
OPENAI_API_KEY = "your_openai_api_key"


async def generate_custom_instructions(injury_description):
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"Provide concise first aid instructions for: {injury_description}",
        max_tokens=100,
        temperature=0.5,
    )
    return response.choices[0].text.strip()
