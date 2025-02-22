![GenI-banner](https://github.com/genilab-fau/genilab-fau.github.io/blob/8d6ab41403b853a273983e4c06a7e52229f43df5/images/genilab-banner.png?raw=true)

# Configuring the Prompt Engineering Lab

If you are a FAU student, go to 
* [Configure Lab Environment for FAU Students](CONFIG-FAU.md)



The configuration requires:
* the **Prompt Engineering Lab**, which provides the simulated GenAI pipeline, and;
* Ollama Server as the server for GenAI models.

You have a few options for this configuration:

* (Option 1): Install both **Prompt Engineering Lab** and **OLLAMA Server** on the same computer (RECOMMENDED)
* (Option 2): Install **Prompt Engineering Lab** on one computer and use the **OLLAMA Server** installed on other computer in the same network (or accessible through the Internet, if feasible)


We recommend using [Visual Code Studio](https://code.visualstudio.com) and installing everything on your computer.

For both options, the installation steps include:
* (Step 1) Bringing up **Ollama Server**
* (Step 2) Downloading **Prompt Engineering Lab** on your computer
* (Step 3) Connecting the **Prompt Engineering Lab** with the **Ollama Server**
* (Step 4) Test the Environment



# (Step 1) Bringing up Ollama Server

Download and install OLLAMA following the instructions at:

[OLLAMA Download](https://ollama.com/download)

Detailed installation instructions at:

[OLLAMA Installation](https://github.com/ollama/ollama)

Once downloaded and installed, you can install GenAI models as:

```bash

ollama pull llama3.2

```

The list of models available are at:

[OLLAMA Model Library](https://ollama.com/library)

You can check the list of models installed in your computer as:


```bash

ollama ps

```

You can start OLLAMA Server to being able to access the models from the **Prompt Engineering Lab** as:

```bash

ollama server

```

Note: if you install OLLAMA server on another computer, you need to make it listen to all network devices so you can access from the **Prompt Engineering Lab** :


```bash
export OLLAMA_HOST=0.0.0.0
ollama server
```


At this point, OLLAMA is up and running and serving requests through port 11434.

> Note: If there is a `bind port error`  while initializing OLLAMA server, `check if the service is already running`, for instance:


```bash 
curl http://localhost:11434/api/ps
```


If you have issue making OLLAMA to work, check * [Troubleshooting ](https://github.com/genilab-fau/prompt-eng/blob/cb2fefa33f5a1c5a927f1246917f73943d3b99ce/TROUBLESHOOTING.md)




# (Step 2) Downloading **Prompt Engineering Lab** on your computer


Just clone the **Prompt Engineering Lab** into your computer using:

```bash

git clone https://github.com/genilab-fau/prompt-eng.git prompt-eng

```

This will create the folder ./prompt-eng with the code and instructions inside it.

Next, you need to install the `requirements.txt`:

```bash

python -m pip install --break-system-packages -r requirements.txt

```

# (Step 3) Connecting the **Prompt Engineering Lab** with the **Ollama Server**


Finally, you need to configure the environment so that the **Prompt Engineering Lab** connected to your Model Server (Ollama).

You need to create the configuration file `_config` with the following parameters (a template is available; `just rename _config.example to _config`)


```bash

# This is an example for _config when Ollama is running on the same computer
URL_GENERATE=http://localhost:11434/api/generate

```

```bash

# This is an example for _config when Ollama is running on other computer
URL_GENERATE=http://OTHER_COMPUTER_IP:11434/api/generate

```

Note: if you install OLLAMA server on another computer, remember to make it listen to all network devices to be able to access remotely:

```bash
export OLLAMA_HOST=0.0.0.0
ollama server
```

# (Step 4) Test the Environment


* Test if the `_pipeline` is connecting to your OLLAMA server:

```bash

python prompt-eng/_pipeline.py

```


If all goes well:


```bash

$ python3 prompt-eng/_pipeline.py
1 + 1 = 2
Time taken: 3.111s

```

If you are having problems, check * [Troubleshooting ](https://github.com/genilab-fau/prompt-eng/blob/cb2fefa33f5a1c5a927f1246917f73943d3b99ce/TROUBLESHOOTING.md)

