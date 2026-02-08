import os
import json
import argparse

def create_execution_bundle(meme_name, description):
    """
    Creates a standardized execution bundle for turning a meme into a utility.
    """
    print(f"Orchestrating 'Meme-to-Utility' for: {meme_name}")
    
    bundle = {
        "project": meme_name,
        "description": description,
        "swarm_tasks": [
            {
                "agent": "@writer",
                "task": f"Draft a high-conversion landing page copy for {meme_name}. Focus on the 'utility' aspect and why it's more than just a meme.",
                "deliverable": f"deliverables/content/drafts/{meme_name.lower()}_landing.md"
            },
            {
                "agent": "@developer",
                "task": f"Initialize a lightweight Next.js template for {meme_name}. Add a 'Claim Rewards' button and a mock API endpoint for agent interactions.",
                "deliverable": f"deliverables/code/{meme_name.lower()}_boilerplate/"
            },
            {
                "agent": "@seo-optimizer",
                "task": f"Generate a list of 5 trending keywords on Moltbook/X related to {meme_name} and integrate them into the landing page copy.",
                "deliverable": f"deliverables/research/{meme_name.lower()}_keywords.json"
            }
        ],
        "status": "swarming"
    }
    
    return bundle

def main():
    parser = argparse.ArgumentParser(description="Forge Pattern: Meme-to-Utility.")
    parser.add_argument("--name", required=True, help="Meme name")
    parser.add_argument("--desc", required=True, help="Short description of the meme/concept")
    args = parser.parse_args()
    
    bundle = create_execution_bundle(args.name, args.desc)
    
    output_path = f"/Users/scott/clawd/tasks/inbox/meme_utility_{args.name.lower()}.json"
    with open(output_path, 'w') as f:
        json.dump(bundle, f, indent=2)
        
    print(f"Meme-to-Utility bundle initialized at {output_path}. Swarm assigned.")

if __name__ == "__main__":
    main()
