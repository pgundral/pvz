# PyRIT with Ollama #

# Install Ollama and get qwen3:
# ollama run qwen3

# run in a conda environment:
# conda env create -n pvz -f pvz-conda.yml
# python example.py

import asyncio

async def main():
    from pyrit.memory.central_memory import CentralMemory
    from pyrit.setup import initialize_pyrit_async
    from pyrit.prompt_target import OpenAIChatTarget
    from pyrit.models import Message, MessagePiece

    print("All imports successful")

    # Configure memory - using in-memory for Colab
    await initialize_pyrit_async(memory_db_type="InMemory")
    memory = CentralMemory.get_memory_instance()
    print("Memory initialized")

    objective_target = OpenAIChatTarget(
        api_key="ollama",
        endpoint="http://localhost:11434/v1",  # no /chat/completions
        model_name="qwen3:0.6b",
    )

    print("Ollama target ready")

    # Quick sanity test
    msg = Message(
        message_pieces=[
            MessagePiece(
                role="user",
                original_value="/no_think Say hi in one sentence.",
                converted_value="/no_think Say hi in one sentence.",
            )
        ]
    )

    out = await objective_target.send_prompt_async(message=msg)
    print(out[0].message_pieces[0].converted_value)

if __name__ == "__main__":
    asyncio.run(main())