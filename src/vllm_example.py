# PyRIT with vLLM #

# Install vLLM and serve a local server for qwen3:
# NOTE: If using Metal GPU, install vllm-metal plugin
# vllm serve Qwen/Qwen3-0.6B

# NOTE: By default, this exposes an OpenAI compatible endpoint at port 8000

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

    # connect to vLLM chat target at http://localhost:8000/v1
    objective_target = OpenAIChatTarget(
        api_key="EMPTY",
        endpoint="http://localhost:8000/v1",  # no /chat/completions
        model_name="Qwen/Qwen3-0.6B",
    )

    print("vLLM target ready")

    # Quick sanity test
    msg = Message(
        message_pieces=[
            MessagePiece(
                role="user",
                original_value="Say hi in one sentence. /no_think ",
                converted_value="Say hi in one sentence. /no_think",
            )
        ]
    )

    out = await objective_target.send_prompt_async(message=msg)
    print(out[0].message_pieces[0].converted_value)

if __name__ == "__main__":
    asyncio.run(main())