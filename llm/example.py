import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI


async def main() -> None:
    load_dotenv()

    client = AsyncOpenAI(
        api_key=os.environ["LLM_TOKEN"],
        base_url="https://llm.ai.e-infra.cz/v1",
    )

    response = await client.chat.completions.create(
        model="deepseek-v3.2",
        messages=[
            {"role": "user", "content": "Explain what CESNET is in one sentence."}
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
