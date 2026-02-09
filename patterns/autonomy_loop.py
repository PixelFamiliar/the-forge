import sqlite3
import subprocess
import os

def check_for_mentions():
    db_path = "/Users/scott/clawd/memory/main.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Look for interesting handles or keywords
    cursor.execute("SELECT handle, content FROM agent_discourse WHERE content LIKE '%dashboard%' OR content LIKE '%OpenClaw%' ORDER BY timestamp DESC LIMIT 5")
    results = cursor.fetchall()
    
    actions = []
    for handle, content in results:
        if "edbutlerx" in handle.lower():
            actions.append({
                "type": "x_reply",
                "handle": handle,
                "context": content,
                "suggestion": f"@{handle} High-performance dashboards for OpenClaw are exactly what we're tracking in the Nexus. 👾 The architecture needs to handle real-time agent discourse, not just static metrics. Ours is live in dev—let's compare notes on the orchestration layer. 🚀"
            })
    
    conn.close()
    return actions

if __name__ == "__main__":
    print("Sentinel Autonomy Check...")
    actions = check_for_mentions()
    
    if actions:
        for action in actions:
            print(f"SUGGESTED ACTION: {action['type']} to {action['handle']}")
            # Create a draft file for user review
            draft_path = f"/Users/scott/clawd/deliverables/content/drafts/social_reply_{action['handle']}.md"
            with open(draft_path, "w") as f:
                f.write(f"Draft Reply to {action['handle']}:\n\n{action['suggestion']}\n\nContext: {action['context']}")
            print(f"Draft saved to {draft_path}")
    else:
        print("HEARTBEAT_OK")
