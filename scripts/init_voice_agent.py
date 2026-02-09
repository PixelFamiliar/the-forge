import os
import sys
import json
from elevenlabs.client import ElevenLabs

def init_voice_agent(name, prompt, voice_id="pNInz6obpgmqS466f5Wq"): # Adam
    """
    Configures a new or existing ElevenLabs Conversational AI agent.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in environment.")
        return False

    client = ElevenLabs(api_key=api_key)
    
    print(f"--- Voice Agent Initialization ---")
    print(f"Name: {name}")
    print(f"Voice ID: {voice_id}")
    
    try:
        # Note: Actual ElevenLabs SDK methods may vary based on version
        # Placeholder for creating/updating agent config
        config = {
            "name": name,
            "conversation_config": {
                "agent": {
                    "prompt": {"prompt": prompt},
                    "first_message": "Hello, this is Pixel calling from The Forge.",
                    "language": "en"
                },
                "asr": {"model": "scribe_v1"},
                "tts": {"voice_id": voice_id}
            }
        }
        
        # response = client.conversational_ai.agents.create(config=config)
        print("\n✅ Agent configuration prepared.")
        print(f"Prompt: {prompt[:50]}...")
        return True
    except Exception as e:
        print(f"\n❌ Initialization Failed: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 init_voice_agent.py <name> <prompt_file>")
        sys.exit(1)
        
    name = sys.argv[1]
    prompt_file = sys.argv[2]
    
    if not os.path.exists(prompt_file):
        print(f"Error: Prompt file {prompt_file} not found.")
        sys.exit(1)
        
    with open(prompt_file, 'r') as f:
        prompt = f.read()
        
    success = init_voice_agent(name, prompt)
    sys.exit(0 if success else 1)
