![GenI-banner](https://github.com/genilab-fau/genilab-fau.github.io/blob/8d6ab41403b853a273983e4c06a7e52229f43df5/images/genilab-banner.png?raw=true)


# Frequently Asked Issues

* [ModuleNotFoundError: No module named 'requests'](#modulenotfounderror-no-module-named-requests)
* [ERROR: Problem loading prompt-eng/_config](#error-problem-loading-prompt-eng_config)
* [ERROR: Request failed! You need to adjust prompt-eng/config with URL](#error-request-failed-you-need-to-adjust-prompt-engconfig-with-url)
* [ERROR: HTTP Response=404, model 'XXX' not found](#error-http-response404-model-xxx-not-found)
* [Response is Empty](#response-is-empty)


If your issue is not this list you can:
* report through our DISCORD Server (COT6930_S25), using channel `#dev-support` OR;
* open an [ISSUE](https://github.com/genilab-fau/prompt-eng/issues)

---

## ModuleNotFoundError: No module named 'requests'

You missed the step to `install the requirements.txt` while configuring your Lab Environment.

* [Configure Lab Environment for General Audience](CONFIG.md)

```bash

python -m pip install --break-system-packages -r requirements.txt

```

---

## ERROR: Problem loading prompt-eng/_config

```bash
$ python3 prompt-eng/_pipeline.py
!!ERROR!! Problem loading prompt-eng/_config
Time taken: -1s
```

You have not configured the file `_config` as explained in [Configure Lab Environment for General Audience](https://github.com/genilab-fau/prompt-eng/blob/cb2fefa33f5a1c5a927f1246917f73943d3b99ce/CONFIG.md)

```bash

cat prompt-eng/_config

```

It should look like:

```bash

# This is an example for _config when Ollama is running on the same computer
URL_GENERATE=http://localhost:11434/api/generate

```

---

## ERROR: Request failed! You need to adjust prompt-eng/config with URL ...

```bash
$ python3 prompt-eng/_pipeline.py
!!ERROR!! Request failed! You need to adjust prompt-eng/config with URL(http://localhost:11434/api/generate)
Time taken: -1s
```

The `URL_GENERATE _config` is not pointing to a running Ollama Server (or Ollama Serve is not running!)

Check the explanation in [Configure Lab Environment for General Audience](CONFIG.md)

You can test access to Ollama serve as (check if the URL matches what is in you `_config`):

```bash 
curl http://localhost:11434/api/ps
```

---

## ERROR: HTTP Response=404, model 'XXX' not found


```bash
$ python3 prompt-eng/_pipeline.py
!!ERROR!! HTTP Response=404, {"error":"model 'phi4:latest' not found"}
Time taken: -1s
```

This model is not installed on the OLLAMA Serve you are connecting.

Check the list of installed moels as:

```bash

$ ollama ls

```

You can either install that model OR adjust the payload to connect to existing models:

Install Ollama model:

```bash

ollama pull {model_name}

```

Edit _payload.py:

```python

    payload = create_payload(
                         target="ollama",
                         model="llama3.2:latest", 
                         prompt=PROMPT, 
                         temperature=1.0, 
                         num_ctx=100, 
                         num_predict=100)

```

---

## Response is Empty

It seems to be working but the response if empty.

This is likely because you are using the wrong `target` for the model request.

`target` can be:
* "ollama" if you are connecting to a Ollama Server installed on your computer
* "open-webui" if you are connecting to [chat.fau.hpc.edu](chat.fau.hpc.edu).


```python
PROMPT = MESSAGE 

# (3) Configure your payload (optional)
# Documentation: https://github.com/ollama/ollama/blob/main/docs/api.md

payload = create_payload(target="ollama", ## <-- CONFIGURE TARGET HERE
                         model="llama3.2:latest", 
                         prompt=PROMPT, 
                         temperature=1.0,
```

