#!/usr/bin/env python3
"""
cap_gate.py — Quota enforcement for the agent swarm.

Usage:
    python3 cap_gate.py --action post_tweet
    python3 cap_gate.py --action draft_content
    python3 cap_gate.py --action substack

Exit codes:
    0 = ALLOWED (proceed)
    1 = BLOCKED (quota full)

Agents call this BEFORE taking any capped action.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

STATE_DIR = Path("/Users/scott/clawd/state")
POLICY_PATH = STATE_DIR / "ops_policy.json"
EVENTS_PATH = STATE_DIR / "events.jsonl"

def load_policy():
    with open(POLICY_PATH) as f:
        return json.load(f)

def count_today_events(action_tag):
    if not EVENTS_PATH.exists():
        return 0
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    with open(EVENTS_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("date", "").startswith(today) and action_tag in event.get("tags", []):
                    count += 1
            except json.JSONDecodeError:
                continue
    return count

def check_tweet_gate(policy):
    quota = policy.get("x_daily_quota", {})
    limit = quota.get("limit", 5)
    today_count = count_today_events("tweet_posted")
    if today_count >= limit:
        return False, f"Tweet quota full ({today_count}/{limit})"
    return True, f"Tweet quota OK ({today_count}/{limit})"

def check_content_gate(policy):
    cp = policy.get("content_policy", {})
    if not cp.get("enabled", True):
        return True, "Content policy disabled"
    limit = cp.get("max_drafts_per_day", 8)
    today_count = count_today_events("content_drafted")
    if today_count >= limit:
        return False, f"Content quota full ({today_count}/{limit})"
    return True, f"Content quota OK ({today_count}/{limit})"

def check_substack_gate(policy):
    cp = policy.get("content_policy", {})
    if not cp.get("enabled", True):
        return True, "Content policy disabled"
    limit = cp.get("max_substack_per_week", 2)
    if not EVENTS_PATH.exists():
        return True, f"Substack quota OK (0/{limit})"
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_start_str = week_start.strftime("%Y-%m-%d")
    count = 0
    with open(EVENTS_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("date", "") >= week_start_str and "substack_published" in event.get("tags", []):
                    count += 1
            except json.JSONDecodeError:
                continue
    if count >= limit:
        return False, f"Substack quota full ({count}/{limit})"
    return True, f"Substack quota OK ({count}/{limit})"

GATES = {
    "post_tweet": check_tweet_gate,
    "draft_content": check_content_gate,
    "substack": check_substack_gate,
}

def log_event(agent_id, action, tags, title=""):
    event = {
        "date": datetime.now().isoformat(),
        "agent_id": agent_id,
        "action": action,
        "tags": tags,
        "title": title,
    }
    with open(EVENTS_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Cap Gate — quota enforcement")
    parser.add_argument("--action", required=True, choices=list(GATES.keys()),
                        help="Action to check quota for")
    parser.add_argument("--log", action="store_true",
                        help="Also log the event (call AFTER the action succeeds)")
    parser.add_argument("--agent", default="unknown",
                        help="Agent ID for event logging")
    parser.add_argument("--title", default="",
                        help="Event title for logging")
    args = parser.parse_args()

    policy = load_policy()
    gate_fn = GATES[args.action]
    allowed, reason = gate_fn(policy)

    if args.log and allowed:
        tag_map = {
            "post_tweet": ["tweet_posted"],
            "draft_content": ["content_drafted"],
            "substack": ["substack_published"],
        }
        log_event(args.agent, args.action, tag_map.get(args.action, []), args.title)

    print(reason)
    sys.exit(0 if allowed else 1)

if __name__ == "__main__":
    main()
