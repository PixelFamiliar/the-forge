#!/usr/bin/env python3
"""
reaction_matrix.py v2 — JSON-driven inter-agent reactions with cooldowns.

Reads patterns from /state/ops_policy.json instead of hardcoded rules.
Called during heartbeat to process today's events and trigger cross-agent tasks.

Usage:
    python3 reaction_matrix.py              # dry run
    python3 reaction_matrix.py --execute    # creates tasks + updates cooldowns
"""

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

STATE_DIR = Path("/Users/scott/clawd/state")
POLICY_PATH = STATE_DIR / "ops_policy.json"
EVENTS_PATH = STATE_DIR / "events.jsonl"
TASKS_DIR = Path("/Users/scott/clawd/tasks/inbox")

def load_policy():
    with open(POLICY_PATH) as f:
        return json.load(f)

def save_policy(policy):
    with open(POLICY_PATH, "w") as f:
        json.dump(policy, f, indent=2)

def get_today_events():
    if not EVENTS_PATH.exists():
        return []
    today = datetime.now().strftime("%Y-%m-%d")
    events = []
    with open(EVENTS_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("date", "").startswith(today):
                    events.append(event)
            except json.JSONDecodeError:
                continue
    return events

def check_cooldown(pattern):
    last_fired = pattern.get("last_fired_at")
    if not last_fired:
        return True
    cooldown_min = pattern.get("cooldown_minutes", 60)
    last_fired_dt = datetime.fromisoformat(last_fired)
    return datetime.now() > last_fired_dt + timedelta(minutes=cooldown_min)

def tags_match(event_tags, pattern_tags):
    return all(tag in event_tags for tag in pattern_tags)

def source_matches(event_agent, pattern_source):
    if pattern_source == "*":
        return True
    return event_agent == pattern_source

def create_task(target, action, source_agent, trigger_tags, execute=False):
    task_id = f"reaction_{random.randint(10000, 99999)}"
    task = {
        "id": task_id,
        "assigned_to": target,
        "action": action,
        "triggered_by": source_agent,
        "trigger_tags": trigger_tags,
        "priority": "medium",
        "status": "inbox",
        "created_at": datetime.now().isoformat(),
    }
    if execute:
        task_path = TASKS_DIR / f"{task_id}.json"
        with open(task_path, "w") as f:
            json.dump(task, f, indent=2)
        print(f"  ✅ CREATED: {task_path.name}")
    else:
        print(f"  🔍 DRY RUN: Would create task for {target} → {action}")
    return task

def process_reactions(execute=False):
    policy = load_policy()
    matrix_config = policy.get("reaction_matrix", {})
    if not matrix_config.get("enabled", False):
        print("⚠️  Reaction matrix disabled in ops_policy.json")
        return

    patterns = matrix_config.get("patterns", [])
    events = get_today_events()

    if not events:
        print("📭 No events today — nothing to react to.")
        return

    print(f"📊 Processing {len(events)} events against {len(patterns)} patterns...\n")

    fired = skipped_cd = skipped_prob = 0

    for event in events:
        agent = event.get("agent_id", "")
        etags = event.get("tags", [])
        for i, pattern in enumerate(patterns):
            if not source_matches(agent, pattern["source"]):
                continue
            if not tags_match(etags, pattern["tags"]):
                continue
            if not check_cooldown(pattern):
                skipped_cd += 1
                continue
            prob = pattern.get("probability", 1.0)
            roll = random.random()
            if roll > prob:
                skipped_prob += 1
                continue
            print(f"  🔥 MATCH: {agent} [{', '.join(etags)}] → {pattern['target']} will {pattern['action']}")
            create_task(pattern["target"], pattern["action"], agent, etags, execute)
            if execute:
                patterns[i]["last_fired_at"] = datetime.now().isoformat()
            fired += 1

    if execute and fired > 0:
        policy["reaction_matrix"]["patterns"] = patterns
        save_policy(policy)

    print(f"\n📈 Summary: {fired} fired, {skipped_cd} skipped (cooldown), {skipped_prob} skipped (probability)")

def main():
    parser = argparse.ArgumentParser(description="Reaction Matrix v2")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    print(f"🔄 Reaction Matrix v2 — {'EXECUTE' if args.execute else 'DRY RUN'}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    process_reactions(execute=args.execute)

if __name__ == "__main__":
    main()
