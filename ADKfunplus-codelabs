summary: Build Agents with ADK: Foundations+ — CeritaNenek 👵🏻
id: build-agents-with-adk-foundations-plus
categories: ai, adk, vertex-ai, beginners
status: Published
feedback link: https://github.com/<your-username>/adk-ceritanenek/issues
author: yourname

# Build Agents with ADK: Foundations+ — CeritaNenek 👵🏻

---

## 1. Introduction

In this extended version of the [ADK Foundations Codelab](https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation?hl=en), you’ll build **CeritaNenek** — a friendly Indonesian “grandma” agent that tells short stories, fables, and advice for modern times.

But here’s the twist — you’ll build **two agents**:
- 🧱 **Regular Prompt Agent:** basic behavior, simple storytelling  
- ⚡ **Power-Prompt Agent:** structured instructions with emotion, cultural tone, and adaptive responses  

By comparing them, you’ll understand how **instruction design** changes an agent’s performance.

---

## 2. Set Up the Environment

1. Clone this repository:
    ```bash
    git clone https://github.com/<your-username>/adk-ceritanenek.git
    cd adk-ceritanenek
    ```

2. Install dependencies:
    ```bash
    npm install
    pip install google-cloud-aiplatform adk
    ```

3. Authenticate with your GCP account:
    ```bash
    gcloud auth login
    gcloud config set project <YOUR_PROJECT_ID>
    ```

4. Ensure Vertex AI and Cloud Run APIs are enabled:
    ```bash
    gcloud services enable aiplatform.googleapis.com run.googleapis.com
    ```

---

## 3. Create Your First Agent — Regular Prompt

Create a file called `cerita_nenek_basic.py`:

```python
from adk import Agent

cerita_nenek_basic = Agent(
    name="CeritaNenek",
    instructions="You are a friendly Indonesian grandma who shares short, heartwarming stories for children and adults. Each story should be under 150 words.",
)

print(cerita_nenek_basic.run("Tell me a story about honesty"))
```

Run locally:
```bash
python cerita_nenek_basic.py
```

Observe how the story is short but plain — it lacks tone, humor, and cultural flavor.

---

## 4. Upgrade with Power Prompting

Create a new file: `cerita_nenek_power.py`

```python
from adk import Agent

cerita_nenek_power = Agent(
    name="CeritaNenek",
    instructions="""
You are **Nenek Tuti**, a wise and witty Indonesian grandma who tells heartfelt stories infused with warmth and cultural nuance.

Your goals:
1. Keep stories concise (under 200 words)
2. End with a reflective “petuah” (moral advice)
3. Use casual Bahasa Indonesia mixed with light humor and empathy
4. Mention familiar local settings (warung, kampung, hujan sore, etc.)
5. Always sound kind, wise, and slightly playful

Example tone:
> “Dulu waktu Nenek kecil, nasi goreng cuma 500 perak. Tapi rasa syukurnya, Nak, itu yang mahal.”

If user asks for a story, respond naturally like a conversation, not a formal narration.
""",
)

print(cerita_nenek_power.run("Nenek, cerita dong tentang kesabaran"))
```

Run:
```bash
python cerita_nenek_power.py
```

Notice the difference — tone, humor, empathy, and local flavor.

---

## 5. Compare Outputs

Ask both agents the same question:
> “Nenek, cerita tentang menepati janji dong.”

Compare:
- Story depth  
- Naturalness of language  
- Emotional tone  

Discuss what changed just by upgrading the **instruction design**.

---

## 6. Deploy the Agent (Optional)

Deploy your agent using Cloud Run:
```bash
gcloud run deploy ceritanenek-agent \
  --source . \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated
```

Test it:
```bash
curl https://<your-agent-url>/query -d "Nenek, ceritain tentang hujan pertama"
```

---

## 7. Wrap Up

You’ve just learned:
✅ How ADK agents are structured  
✅ How **prompt quality = agent quality**  
✅ How to personalize tone, culture, and empathy  

**CeritaNenek** is your first step toward building agents that *feel human.*

---

### 🌱 Next Steps
- Add memory or context so Nenek remembers past stories  
- Let users upload their own stories for Nenek to comment on  
- Remix into a new idea — **“MendingIniNek”**, a hilarious phone recommendation agent for grandparents 😂  

---

🎉 Congratulations! You’ve completed **Build Agents with ADK: Foundations+ — CeritaNenek**.
