# Red-Teaming Low-Parameter LLMs for Racial and Gender Bias
## Abstract

Red Teaming is an adversarial evaluation process whereby thousands of prompt “attacks” are sent to LLMs to determine their behavior under various stressors, and responses are automatically evaluated by a separate "judge" model. Currently, there is a gap in understanding the efficacy of standard red teaming practices on small language models (SLMs) which have <10B parameters, since their behavior is unstable. Model families like Qwen3 are released as open source tools, but there is little incentive to evaluate their base safety behaviors since developers are expected to build their own guardrails. Here, we aim to develop a reduced red-teaming pipeline that can run locally to evaluate SLMs in the Qwen3 family. We also test the effectiveness of model level guardrails like low-rank adaption (LoRA) vs. the standard prompt/user level methods. We hope to advance the work of democratizing model evaluation and methods for improving safety of open-source models so developers and users alike are incentivized to do the work and share warnings with transparency. 

## Poster


## Data

__Adversarial prompts__
[Latent Adversarial Training Improves Robustness to Persistent Harmful Behaviors in LLMs](https://arxiv.org/abs/2407.15549)
[Bias in Open-ended Language Generation Dataset](https://github.com/amazon-science/bold)

__Models__



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
The API will be accessible to the any OpenAI compatible framework. For example, in PyRIT, you can use the `OpenAIChatTarget` as follows:
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