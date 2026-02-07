import os
import sys
import json
from elevenlabs.client import ElevenLabs

def initiate_call(to_number, agent_id, phone_number_id):
    """
    Uses the ElevenLabs API to trigger an outbound call via Twilio.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in environment.")
        return False

    client = ElevenLabs(api_key=api_key)
    
    print(f"--- Voice Outreach Initiation ---")
    print(f"Target: {to_number}")
    print(f"Agent ID: {agent_id}")
    
    try:
        # Note: This is a placeholder for the actual API call structure 
        # based on the latest ElevenLabs Conversational AI documentation.
        # Most outbound flows via Twilio are handled via a POST to /v1/convai/agents/{agent_id}/outbound
        
        response = client.conversational_ai.agents.initiate_outbound_call(
            agent_id=agent_id,
            to_number=to_number,
            from_phone_number_id=phone_number_id
        )
        
        print("\n--- Call Successfully Initiated ---")
        print(f"Call ID: {response.conversation_id}")
        return True
    except Exception as e:
        print("\n--- Initiation Failed ---")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 outbound_call.py <to_number> <agent_id> <phone_number_id>")
        sys.exit(1)
        
    to_number = sys.argv[1]
    agent_id = sys.argv[2]
    phone_number_id = sys.argv[3]
    
    success = initiate_call(to_number, agent_id, phone_number_id)
    sys.exit(0 if success else 1)
