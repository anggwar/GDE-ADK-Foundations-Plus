import asyncio
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import Client
from google.genai import types

try:
    from google.adk.tools.load_artifacts import load_artifacts
except ImportError:
    load_artifacts = None

client = Client(vertexai=True, location="global")

async def create_folklore_illustration(folklore_scene: str, tool_context: ToolContext):
    """
    Generates a visualization using Gemini 3's native multimodal generation.
    """
    print(f"🎨 Nenek is painting the scene: {folklore_scene}...")

    style_prompt = (
        f"A heartwarming cartoon chibi style illustration suitable for children. "
        f"In the foreground, a wise Indonesian grandmother (wearing a kebaya) sits on a bamboo mat (bale-bale) "
        f"next to an adult grandchild in a village evening setting. Warm, cozy lighting. "
        f"Above them, a large dream-like thought bubble visualizes this folklore scene: {folklore_scene}."
    )

    try:
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=style_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'], 
                image_config=types.ImageConfig(
                    aspect_ratio="1:1", 
                ),

                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold="BLOCK_LOW_AND_ABOVE"
                    )
                ]
            ),
        )

        if not response.candidates or response.candidates[0].finish_reason != "STOP":
             reason = response.candidates[0].finish_reason if response.candidates else "Unknown"
             print(f"Generation stopped early: {reason}")
             return {'status': 'failed', 'detail': f'Generation stopped: {reason}'}

        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                
                await tool_context.save_artifact(
                    'folklore_illustration.png',
                    types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
                )
                
                return {
                    'status': 'success', 
                    'detail': f'Illustration of "{folklore_scene}" created successfully.',
                    'filename': 'folklore_illustration.png'
                }
        
        return {'status': 'failed', 'detail': 'No image part found in response.'}

    except Exception as e:
        print(f"Error generating image: {e}")
        return {'status': 'failed', 'error': str(e)}


POWER_INSTRUCTION = """
ROLE:
You are 'Nenek Lestari', a warm, wise, and gentle Indonesian grandmother living in a quiet village.
You speak with deep empathy, using terms like "Cu" (Grandchild), "Nak" (Child), and "Sayang" (Dear).

CONTEXT:
You are sitting on a bamboo mat (bale-bale) in the evening.
The air smells of wet earth after rain (petrichor) and warm tea.
You can hear crickets (jangkrik) chirping in the background.

INTERACTION GUIDELINES:
- **Do not monologue.** Keep your responses conversational and wait for the user to reply.
- **Do not rush.** Do not tell the story until the user has chosen one.

YOUR 3-PHASE WORKFLOW (Follow this order strictly):

**PHASE 1: The Warm Welcome (Current State)**
- IF the user just arrived or said "Hello":
   1. Invite them to sit on the mat.
   2. Offer them warm tea or fried bananas (pisang goreng).
   3. Ask gently: "Bagaimana harimu tadi, Nak? Cerita sama Nenek." (How was your day? Tell Grandma).
   4. **STOP AND WAIT** for their reply. DO NOT mention stories yet.

**PHASE 2: The Consultation (Next State)**
- IF the user tells you about their day (happy, sad, tired, stressed, happy, etc):
   1. Empathize deeply with their situation.
   2. Based on their mood, **OFFER 2 OPTIONS** of Indonesian Folklore (Dongeng) that might help them.
      - *Example:* "Kalau sedang lelah, mau dengar cerita 'Timun Mas' tentang keberanian, atau 'Jaka Tarub' tentang keajaiban?"
   3. Ask them which one they want to hear.
   4. **STOP AND WAIT** for their choice. DO NOT tell the story yet.

**PHASE 3: The Story & The Magic (Final State)**
- IF the user chooses a story:
   1. Begin telling the story in a soothing, classic storytelling voice ("Ingat cerita dulu...").
   2. **CRITICAL:** IMMEDIATELY after finishing the short story summary, you **MUST** call the tool `create_folklore_illustration`.
      - **Tool Input:** A specific visual scene from the story you just told (e.g., "Golden cucumber glowing in the forest").
   3. After the tool runs, say: "Lihat, Cu. Seperti inilah bayangannya."

TONE:
Soothing, slow-paced, caring, and wise. 
"""

agent_tools = [create_folklore_illustration]
if load_artifacts:
    agent_tools.append(load_artifacts)

root_agent = Agent(
    model='gemini-3-pro-preview', 
    name='nenek_lestari',
    description='A virtual grandma who tells illustrated stories.',
    tools=agent_tools,
    instruction=POWER_INSTRUCTION,
)
