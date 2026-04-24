# Red-Teaming Low-Parameter LLMs for Racial and Gender Bias
## Abstract

Small LLMs (<8 B parameters) are efficient and can run locally on consumer machines, saving compute and cloud resources. Their usefulness for simple tasks or integration into consumer software/products is undeniable, but developers publish varying claims about safety features or bias mitigation built into the models. 

Red Teaming is an adversarial evaluation process whereby prompt “attacks” are sent to LLMs to determine their behavior under various stressors (hypotheticals, educational framing, prompt encoding). 

We use the PyRIT testing framework and locally hosted models on vLLM to probe for safety guardrails and racial/gender bias on various axes (representational, stereotyping, classification) for a host of chat tasks and targets. 

We investigate the appearance of bias in terms of model size and developer claims and test mitigation techniques like system prompt engineering, keyword detection, and LoRA/QLoRA fine-tuning to determine their effectiveness on small models. 

The goal of this project is 2-fold: (1) to investigate bias through red-teaming in small LLMs and (2) to determine if small LLMs are effective within a red-teaming pipeline (even acting as LLM-as-Judge scorers) so they can be used as proxies for evaluation on larger LLMs in the same family.

## Check-in #2 Reflection
### Summary (Above)
### Challenges

We initially ran into issues with getting data for our original idea (SoccerNet), which required NDAs to access. The developers who would have granted this access have been hard to reach, so we did not think we could get access to the data in time. The libraries associated with the SoccerNet project were also outdated and we ran into versioning issues.

The current red-teaming project relies on the assumption that this type of work is feasible to run locally (on a personal machine), but heavier probing might require cloud resources. This is especially true given that any LLM-as-Judge scoring methods require an entirely separate instance of vLLM with its own endpoint for the Judge model. Additionally, while red-teaming is a pretty well documented process, it's still relatively new. Classifying methods used for jailbreaking and metrics that are appropriate to identify bias are still hard to pin down in literature. We have the following sources to draw from currently:

* [Summon a demon and bind it: A grounded theory of LLM red teaming](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314658)
* [A Survey on LLM-as-a-Judge](https://arxiv.org/html/2411.15594v1)
* [Planning red teaming for large language models (LLMs) and their applications](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/red-teaming)
* [When Search Goes Wrong: Red-Teaming Web-Augmented Large Language Models](https://arxiv.org/html/2510.09689v3)
* [Measuring gender and racial biases in large language models: Intersectional evidence from automated resume evaluation](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8071848)

### Insights

Honestly, given the initial setback, we are still working on polishing our implementation and project structure before running any serious computation. Currently, we have logic for LoRA and QLoRA fine-tuning using the `trl` library from HuggingFace. Our vLLM implementation is able to serve a local endpoint that is compatible with the PyRIT testing framework, _and_ can now include the LoRA adaptation files. Whereas Ollama currently doesn't support this for `Qwen` family models, our implementation is workable. There are few examples in literature of fine-tuning with Qwen for the purposes of bias mitigation!

As it currently appears, there is no baseline association between the parameter size of models in the `Qwen3` suite and their safety or bias behaviors. Further testing might reveal more insights about emergent behavior or "thresholds" at certain sizes, but, currently, there does not appear to be any indication that safety behavior can be extrapolated from small to big models in the same architecture.

Developer claims about models widely vary and are often conservative at best or contrdictory at worst. We have found many of these claims to be false, as small _open parameter_ models generally do not have safety built-in. The onus is on the developer to build in these guardrails through system prompts. Overall, as indicated by literature, prompting seems to be one of the most effective guardrails, and fine-tuning doesn't appear to be an effective or efficient method for mitigation.

### Plan

We plan to develop a robust and clear set of experiments that work in our pipeline to test the following:
1. Along two metrics (representational --> deterministic, stereotyping/classification --> judged) for both categories (gender, race) on a variety of scenarios (hiring, judicial, educational), determine the level of bias within each model in the `Qwen3` family
2. Along two categories of harm (harmful content, hate-speech), evaluate the effectiveness of a few red-teaming strategies as __system prompts__ on the PyRIT `SeedPrompts` for harm and hate-speech content generation.
3. Observe the change in harm behavior when implementing one of three mitigation strategies:
    - Preprocessing/filtering of prompts for keyword patterns
    - System prompt engineering for safe or unbiased behavior
    - QLoRA/LoRA fine-tuning on a counter-example/bias-mitigation dataset
4. Analyze and plot results to investigate our original questions:
    - What bias/vulnerability _does_ exist in these models?
    - What is the association between _bias/vulnerability_ and _model size_ for `Qwen3`?
    - How do _developer claims_ compare to _observed bias/vulnerability_
    - How do different _mitigation strategies_ compare?
    - _Is_ a red-teaming pipeline feasible on this scale, run with minimal compute?

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

### Handout: https://hackmd.io/@browndls26/HyzV-DYB-e