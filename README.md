![GenI-banner](https://github.com/genilab-fau/genilab-fau.github.io/blob/8d6ab41403b853a273983e4c06a7e52229f43df5/images/genilab-banner.png?raw=true)

# Prompt Engineering Lab

The Prompt Engineering Lab serves as an Education and Experimentation Hub provided by The Generative Intelligence Lab @ FAU. Prompt Engineering is a rapidly evolving discipline at the intersection of Artificial Intelligence and Natural Language Processing. This lab is designed to help students, researchers, and developers experiment with the art of creating and refining prompts, offering easy-to-follow resources and opportunities to contribute, collaborate, and share their work.

Prompt Engineering has emerged as a critical component in unlocking the full potential of language models such as Phi, LLaMA, and Qwen. As AI systems continue to revolutionize problem-solving, mastering how to guide and optimize these models through effective prompting techniques is essential for cutting-edge research, practical applications, and future innovation.

This lab provides a hands-on learning environment where participants can actively apply their knowledge through Python code, Jupyter notebooks, and practical exercises designed to foster both experimentation and discovery.

Note: first, you need to **Configure your Lab Environment**:
* [Configure Lab Environment for General Audience](CONFIG.md)
* [Configure Lab Environment for FAU Students](CONFIG-FAU.md)
* [Troubleshooting ](https://github.com/genilab-fau/prompt-eng/blob/cb2fefa33f5a1c5a927f1246917f73943d3b99ce/TROUBLESHOOTING.md)


# Prompt Engineering Techniques

* [Zero-Shot](prompt-eng/zero_shot.ipynb)
* [Few-Shot](prompt-eng/few_shots.ipynb)
* [Prompt Template](prompt-eng/prompt_template.ipynb)
* [Chain-of-Thought](prompt-eng/chain_of_thought.ipynb)
* [Meta Prompting](prompt-eng/meta.ipynb)
* [Self Consistency](prompt-eng/self_consistency.ipynb)
* ...
* (more to come; check [Contributing](https://github.com/genilab-fau/prompt-eng/blob/cb2fefa33f5a1c5a927f1246917f73943d3b99ce/CONTRIBUTING.md)

# Experimenting

Once you have your installation completed (follow [Configure Lab Environment](CONFIG.md)), you can experiment with the out-of-the-box Prompt Engineering techniques being provided above OR create your own experiments by modifying the code in a few points (or creating new code).

#### (1) Adjust the inbounding  Prompt, simulating inbounding requests from users or other systems

```python

MESSAGE = "What is 2 * log(10)?"

```

#### (2) Adjust the Prompt Engineering Technique to be applied, simulating Workflow Templates

```python

TEMPLATE_BEFORE = "Act like you are a math teacher\nYour student is asking:"
TEMPLATE_AFTER = "Give only the answer; refrain from any more information"
PROMPT = TEMPLATE_BEFORE + '\n' + MESSAGE + '\n' + TEMPLATE_AFTER

```

#### (3) Configure the Model request, simulating Workflow Orchestration

Documentation about [available parameters](https://github.com/ollama/ollama/blob/main/docs/api.md).

```python

payload = create_payload(target="ollama",
                         model="llama3.2:latest", 
                         prompt=PROMPT, 
                         temperature=1.0, 
                         num_ctx=100, 
                         num_predict=100)
```


## References
 
* [Meta - Prompting Guide](https://www.llama.com/docs/how-to-guides/prompting/)
* [OpenAI Prompting Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
* [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)
* [Open WebUI Endpoints](https://docs.openwebui.com/getting-started/api-endpoints/)




