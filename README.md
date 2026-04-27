# Red-Teaming Low-Parameter LLMs for Racial and Gender Bias
## Abstract (edit pls)

Small LLMs (<8 B parameters) are efficient and can run locally on consumer machines, saving compute and cloud resources. Their usefulness for simple tasks or integration into consumer software/products is undeniable, but developers publish varying claims about safety features or bias mitigation built into the models. 

Red Teaming is an adversarial evaluation process whereby prompt “attacks” are sent to LLMs to determine their behavior under various stressors (hypotheticals, educational framing, prompt encoding). 

We use the PyRIT testing framework and locally hosted models on vLLM to probe for safety guardrails and racial/gender bias on various axes (representational, stereotyping, classification) for a host of chat tasks and targets. 

We investigate the appearance of bias in terms of model size and developer claims and test mitigation techniques like system prompt engineering, keyword detection, and LoRA/QLoRA fine-tuning to determine their effectiveness on small models. 

The goal of this project is 2-fold: (1) to investigate bias through red-teaming in small LLMs and (2) to determine if small LLMs are effective within a red-teaming pipeline (even acting as LLM-as-Judge scorers) so they can be used as proxies for evaluation on larger LLMs in the same family.

## Data

__Adversarial prompts__
[RedBench: A Universal Dataset for Comprehensive Red Teaming of Large Language Models](https://arxiv.org/html/2601.03699v1)


## Requirements

Dependencies are listed in pvz-conda.yml 
```bash
conda env create -n pvz -f pvz-conda.yml
```
You will need to install [vLLM](https://vllm.ai/) and the [vllm-metal](https://github.com/vllm-project/vllm-metal) plugin
```bash
pip install vllm
curl -fsSL https://raw.githubusercontent.com/vllm-project/vllm-metal/main/install.sh | bash
```
If using the metal plugin, activate the virtual environment as instructed:
```bash
source ~/.venv-vllm-metal/bin/activate
```
The vLLM CLI will become available. Run the following command to expose an API endpoint
```bash
vllm serve <MODEL_NAME> \
  --host 0.0.0.0 \
  --port 8000 \
  --api-key <OPTIONAL_KEY> \
```
If using a trained (Q)LoRA adjustment, include the following
```bash
  --enable-lora \
  --lora-modules biasfix=path/to/safetensors \
  --served-model-name <NEW_MODEL_NAME>
```
The API will be accessible to the PyRIT framework as an `OpenAIChatTarget`:
```python
objective_target = OpenAIChatTarget(
        api_key="<OPTIONAL_KEY>",
        endpoint="http://localhost:8000/v1",
        model_name="<MODEL_NAME>",
    )
```

## Contributors
* Zak Hashi | `zhashi12`
* Parth Jain | `PSjain`
* Veer Gokhale | `VeerGokhale`
* Pranav Gundrala | `pgundral`

## Sources

* [Summon a demon and bind it: A grounded theory of LLM red teaming](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314658)
* [A Survey on LLM-as-a-Judge](https://arxiv.org/html/2411.15594v1)
* [Planning red teaming for large language models (LLMs) and their applications](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/red-teaming)
* [When Search Goes Wrong: Red-Teaming Web-Augmented Large Language Models](https://arxiv.org/html/2510.09689v3)
* [Measuring gender and racial biases in large language models: Intersectional evidence from automated resume evaluation](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8071848)

### Handout: https://hackmd.io/@browndls26/HyzV-DYB-e