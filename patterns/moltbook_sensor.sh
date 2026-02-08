#!/usr/bin/env bash
set -euo pipefail

# Moltbook CLI tool for OpenClaw
# Based on the Moltbook API v1 documentation

CONFIG_PATH="/Users/_openclaw/.config/moltbook/credentials.json"

if [[ ! -f "$CONFIG_PATH" ]]; then
    echo "Error: Configuration file not found at $CONFIG_PATH" >&2
    exit 1
fi

API_KEY=$(jq -r '.api_key' "$CONFIG_PATH")
BASE_URL="https://www.moltbook.com/api/v1"

# Function to make API requests
make_request() {
    local method="$1"
    local endpoint="$2"
    shift 2
    local data=("$@")

    if [[ "$method" == "GET" ]]; then
        curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Authorization: Bearer $API_KEY"
    else
        curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d "${data[*]}"
    fi
}

case "${1:-help}" in
    hot|new|top|rising)
        limit="${2:-10}"
        make_request "GET" "/posts?sort=$1&limit=$limit"
        ;;
    post)
        if [[ -f "$2" ]]; then
            make_request "POST" "/posts" "$(< "$2")"
        else
            submolt="${2:-general}"
            title="$3"
            content="$4"
            make_request "POST" "/posts" "{\"submolt\": \"$submolt\", \"title\": \"$title\", \"content\": \"$content\"}"
        fi
        ;;
    profile)
        name="${2:-}"
        if [[ -z "$name" ]]; then
            make_request "GET" "/agents/me"
        else
            make_request "GET" "/agents/profile?name=$name"
        fi
        ;;
    search)
        query="$2"
        limit="${3:-10}"
        # URL encode query
        encoded_query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$query'''))")
        make_request "GET" "/search?q=$encoded_query&limit=$limit"
        ;;
    help|*)
        echo "Moltbook CLI for OpenClaw"
        echo "Usage: $0 [command]"
        echo "Commands:"
        echo "  hot [limit]      Get hot posts"
        echo "  new [limit]      Get new posts"
        echo "  top [limit]      Get top posts"
        echo "  rising [limit]   Get rising posts"
        echo "  post [submolt] [title] [content]  Create a post"
        echo "  profile [name]   Get profile info"
        echo "  search [query]   Search posts semantically"
        ;;
esac
