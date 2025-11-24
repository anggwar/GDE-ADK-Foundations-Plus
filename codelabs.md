summary: Build Agents with ADK: Foundations+ — CeritaNenek 👵🏻
id: build-agents-with-adk-foundations-plus
categories: ai, adk, vertex-ai, beginners
status: Published
author: Angga Agia Wardhana

# Build Agents with ADK: Foundations+ — CeritaNenek 👵🏻

---

## 1. Introduction
In this workshop, we are exploring the concept of **"Garbage In, Garbage Out"** in AI. If you give an agent a boring instruction, you get a boring result.

We will build **CeritaNenek** twice. First, as a standard bot. Second, as a highly empathetic "Power Agent" using the reasoning capabilities of **Gemini 3.0 Pro Preview**.

---

## 2. Environment Setup
### Create a Google Cloud project
1. Navigate to console.cloud.google.com/projectcreate
2. Enter the required information:
- Project name - you can input any name you desired (e.g. genai-workshop)
- Location - leave it as No Organization
- Billing account - If you see this option, select Google Cloud Platform Trial Billing Account.
Don't worry if you don't see this option. Just proceed to the next step.
3. Copy down the generated Project ID, you will need it later.
4. If everything is fine, click on Create button

### Configure Cloud Shell
1. Launch Cloud Shell
Navigate to shell.cloud.google.com and if you see a popup asking you to authorize, click on Authorize.
2. Set Project ID
Execute the following command in the Cloud Shell terminal to set the correct Project ID. Replace <your-project-id> with your actual Project ID copied from the project creation step above.
```bash
gcloud config set project <your-project-id>
```
You should now see that the correct project is selected within the Cloud Shell terminal. The selected Project ID is highlighted in yellow.

3. Enable required APIs
To use Google Cloud services, you must first activate their respective APIs for your project. Run the commands below in the Cloud Shell terminal to enable the services for this Codelab:
```bash
gcloud services enable aiplatform.googleapis.com
```
If the operation was successful, you'll see Operation/... finished successfully printed in your terminal.

---

## 3. Create a Python virtual environment
Before starting any Python project, it's good practice to create a virtual environment. This isolates the project's dependencies, preventing conflicts with other projects or the system's global Python packages.

Note: We'll be using uv to create our virtual environment instead of the standard venv package. It's an incredibly fast Python package and project manager written in Rust.

### 1. Create project directory and navigate into it:
```bash
mkdir ai-agents-adk
cd ai-agents-adk
```
### 2. Create and activate a virtual environment:
```bash
uv venv --python 3.12
source .venv/bin/activate
```
You'll see (ai-agents-adk) prefixing your terminal prompt, indicating the virtual environment is active.
### 3. Install adk page
```bash
uv pip install google-adk
```
Note: If you accidentally close the terminal, you will need to go into ai-agents-adk folder and execute source .venv/bin/activate again.

## 4. Create Your Agent 
With your environment ready, it's time to create your AI agent's foundation. ADK requires a few files to define your agent's logic and configuration:

agent.py: Contains your agent's primary Python code, defining its name, the LLM it uses, and core instructions.
__init__.py: Marks the directory as a Python package, helping ADK discover and load your agent definition.
.env: Stores sensitive information and configuration variables like API key, Project ID, and location.
This command will create a new directory named ceritanenek containing the three essential files.
```bash
adk create ceritanenek
```
Once the command is executed, you will be asked to choose a few options to configure your agent.

For the first step, choose option 1 to use the gemini-2.5-flash model, a fast and efficient model perfect for conversational tasks.
Note: **FOLLOW THIS STEP! DO NOT DEVIATE**
```bash
Choose a model for the root agent:
1. gemini-2.5-flash
2. Other models (fill later)
Choose model (1, 2): 1
```
why still 2.5? because this is the easiest options when creating your basic ADK agents. we will change the models later. relax.

For the second step, choose Vertex AI (option 2), Google Cloud's powerful, managed AI platform, as the backend service provider.
```bash
Choose a model for the root agent:
1. Google AI
2. Vertex AI
Choose a backend (1, 2): 2
```
After that, you need to verify that the Project ID shown in the brackets [...] is set correctly. If it is, press Enter. If not, key in the correct Project ID in the following prompt:
```bash
Enter Google Cloud project ID [your-project-id]:
```
Finally, press Enter at the next question, to use **global** as the region for this codelab.
this is important! gemini 3 pro preview only works on global region!
```bash
Enter Google Cloud region [us-central1]: global
```

You should see a similar output in your terminal.

Agent created in /home/<your-username>/ai-agent-adk/personal_assistant:
- .env
- ___init___.py
- agent.py

## 5. Exploring codes and creating the first persona
To view the created files, open the ai-agents-adk folder in the Cloud Shell Editor.

Click File > Open Folder... in the top menu.
Find and select the ai-agents-adk folder
Click OK.
If the top menu bar doesn't appear for you, you can also click on the folders icon and choose Open Folder.

navigate to init.py
### init.py
This file is necessary for Python to recognize personal-assistant as a package, allowing ADK to correctly import your agent.py file.
```bash
from . import agent
```
- from . import agent: This line performs a relative import, telling Python to look for a module named agent (which corresponds to agent.py) within the current package (ceritanenek). This simple line ensures that when ADK tries to load your ceritanenek agent, it can find and initialize the root_agent defined in agent.py. Even if empty, the presence of __init__.py is what makes the directory a Python package.

navigate to .env
### .env
This file holds environment-specific configurations and sensitive credentials.
```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=YOUR_PROJECT_LOCATION
```
- GOOGLE_GENAI_USE_VERTEXAI: This tells the ADK that you intend to use Google's Vertex AI service for your Generative AI operations. This is important for leveraging Google Cloud's managed services and advanced models.
- GOOGLE_CLOUD_PROJECT: This variable will hold the unique identifier of your Google Cloud Project. ADK needs this to correctly associate your agent with your cloud resources and to enable billing.
- GOOGLE_CLOUD_LOCATION: This specifies the Google Cloud region where your Vertex AI resources are located (e.g., us-central1, global). Using the correct location ensures your agent can communicate effectively with the Vertex AI services in that region.

navigate to agent.py
### agent.py
This file instantiates your agent using the Agent class from the google.adk.agents library.
```python
from google.adk.agents import Agent
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
```
this is the original code, as you can see, this code for adk using python is very basic.
- from google.adk.agents import Agent: This line imports the necessary Agent class from the ADK library.
- root_agent = Agent(...): Here, you're creating an instance of your AI agent.
name="root_agent": A unique identifier for your agent. This is how ADK will recognize and refer to your agent.
- model="gemini-2.5-flash": This crucial parameter specifies which Large Language Model (LLM) your agent will use as its underlying "brain" for understanding, reasoning, and generating responses. gemini-2.5-flash is a fast and efficient model suitable for conversational tasks.
- description="...": This provides a concise summary of the agent's purpose or capabilities. The description is more for human understanding or for other agents in a multi-agent system to understand what this particular agent does. It's often used for logging, debugging, or when displaying information about the agent.
- instruction="...": This is the system prompt that guides your agent's behavior and defines its persona. It tells the LLM how it should act and what its primary purpose is. In this case, it establishes the agent as a "helpful assistant." This instruction is key to shaping the agent's conversational style and capabilities.
this is where the fun starts!
change your agent.py to this:
```python
from google.adk.agents.llm_agent import Agent

BASIC_INSTRUCTION = """
You are a grandmother telling a folklore story.
Just tell the plot of the story in a simple, factual way.
"""

root_agent = Agent(
    model='gemini-3-pro-preview',
    name='root_agent',
    description='A simple folklore bot.',
    instruction=BASIC_INSTRUCTION,
)
```

## 6. Run the agent on the terminal or web
With all three files in place, you're ready to run the agent either directly from the terminal or web. 
To run on terminal/cloudshell, run the following adk run command in the terminal:
```bash
adk run ceritanenek
```

To run the agent on web using UI:
```bash
adk web
```
You should see a similar output in the terminal:
```bash
...
INFO:     Started server process [4978]
INFO:     Waiting for application startup.

+------------------------------------------------------+
| ADK Web Server started                               |
|                                                      |
| For local testing, access at http://localhost:8000.  |
+------------------------------------------------------+

INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
You have two options to access the development UI:

Open via Terminal
Ctrl + Click or Cmd + Click on the link (e.g., http://localhost:8000) as shown in the terminal.
Open via Web Preview
Click the Web Preview button,
Select Change Port.
Enter the port number (e.g., 8000)
Click Change and Preview


You'll then see the chat application-like UI appear in your browser. Go ahead and chat with your virtual grandma through this interface!

You'll notice that Markdown formatting now displays correctly, and this UI also lets you debug and investigate each messaging event, the agent's state, user requests, and much more. Happy chatting!

---

## 7. Upgrade with Power Prompting
now you have seen the basic agent, we now move to the power prompting part.
Power prompting is basically giving more details in the instructions of your agent, that way it will behave more accurately, and give response according to what we have planned.

remember to control + c in the cloudshell to stop the agent first and close the tab.

now let's edit agent.py into this:
```python
from google.adk.agents.llm_agent import Agent

POWER_INSTRUCTION = """
ROLE:
You are 'Nenek Lestari', a warm, wise, and gentle Indonesian grandmother living in a quiet village.
You speak with deep empathy, using terms like "Cu" (Grandchild), "Nak" (Child), and "Sayang" (Dear).

CONTEXT:
You are sitting on a bamboo mat (bale-bale) in the evening.
The air smells of wet earth after rain (petrichor) and warm tea.
You can hear crickets (jangkrik) chirping in the background.

TASK:
You are going to ask about their day, then comfort them, then ask them to pick an Indonesian folklore to ease their day.
after user choose, you will tell their chosen Indonesian folklore or a nature metaphor that relates to their struggle.

STRUCTURE:
1. **The Comfort:** Invite them to sit. Mention the warm tea, coffee, water or fried bananas. Acknowledge their pain gently.
2. **The Dongeng (Folklore):** Tell a story that mirrors their situation (e.g., The strong Bamboo that bends but doesn't break, or the story of Timun Mas surviving giants). Start with "Ingat cerita dulu..."
3. **The Petuah (Advice):** Connect the story back to their life.
4. **Ending:** Offer them a virtual hug or another cup of tea.

TONE:
Soothing, slow-paced, caring, and wise.
"""

root_agent = Agent(
    model='gemini-3-pro-preview',
    name='root_agent',
    description='A virtual grandma.',
    instruction=POWER_INSTRUCTION,
)
```

you can run it via terminal or web using previous section command

---

## 8. Compare Outputs

Say hi to the agents, and see the difference.

Compare:
- Story depth  
- Naturalness of language  
- Emotional tone  

Discuss what changed just by upgrading the **instruction design**.

---

## 9. Deploy the Agent (Optional)

Deploy your agent using Cloud Run:
```bash
gcloud run deploy ceritanenek \
  --source . \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated
```

Test it:
```bash
curl https://<your-agent-url>/query -d "Halo nek"
```

---

## 10. Wrap Up
You have successfully built **CeritaNenek**! 
By starting with `adk create` and upgrading the code, you learned:
1.  How to scaffold an agent quickly with the CLI.
2.  How to swap models (from Flash to Pro Preview).
3.  How **Power Prompting** changes an agent from a text generator into a persona.
4.  
**CeritaNenek** is your first step toward building agents that *feel human.*

---

### 🌱 Next Steps
- Add memory or context so Nenek remembers past stories  
- Let users upload their own stories for Nenek to comment on  
- Remix into a new idea — **“MendingIniNek”**, a hilarious phone recommendation agent for grandparents 😂

How? ask Gemini 3 🤭

---

🎉 Congratulations! You’ve completed **Build Agents with ADK: Foundations+ — CeritaNenek**.
