#!/usr/bin/env bash
# ==============================================================================
# homeserver docker_manager.sh - Docker Container & Stack Maintenance Utility
# Usage:
#   ./docker_manager.sh list
#   ./docker_manager.sh stats
#   ./docker_manager.sh logs <container_name> [lines]
#   ./docker_manager.sh restart <container_name>
#   ./docker_manager.sh restart-stack <stack_name>
#   ./docker_manager.sh prune
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSH_CMD="$SCRIPT_DIR/ssh_exec.sh"

COMMAND="${1:-list}"
ARG2="$2"
ARG3="$3"

case "$COMMAND" in
    list|ps)
        $SSH_CMD "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}'"
        ;;
    stats)
        $SSH_CMD "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}'"
        ;;
    logs)
        if [ -z "$ARG2" ]; then
            echo "Usage: $0 logs <container_name> [lines]"
            exit 1
        fi
        LINES="${ARG3:-50}"
        $SSH_CMD "docker logs --tail $LINES $ARG2"
        ;;
    restart)
        if [ -z "$ARG2" ]; then
            echo "Usage: $0 restart <container_name>"
            exit 1
        fi
        echo "Restarting container '$ARG2' on homeserver..."
        $SSH_CMD "docker restart $ARG2"
        echo "✅ Container '$ARG2' restarted successfully."
        ;;
    restart-stack)
        if [ -z "$ARG2" ]; then
            echo "Usage: $0 restart-stack <stack_name>"
            echo "Available stacks: homepage, opengym, navidrome, kanbanboard, vikunja, dailytxt, homer, audiobookself"
            exit 1
        fi
        STACK="$ARG2"
        $SSH_CMD "bash -s" << EOF
STACK="$STACK"
case "\$STACK" in
    homepage)      DIR="/opt/Homepage" ;;
    opengym)       DIR="/opt/openGym" ;;
    navidrome)     DIR="/opt/navidrome" ;;
    homer)         DIR="/opt/homer" ;;
    vikunja)       DIR="/opt/vikunja" ;;
    dailytxt)      DIR="/opt/DailyTxT" ;;
    kanboard|kanbanboard) DIR="/root/docker-compose/kanbanboard" ;;
    audiobookshelf|audiobookself) DIR="/root/docker-compose/audiobookself" ;;
    *) echo "Unknown stack '\$STACK'"; exit 1 ;;
esac
echo "Restarting stack in \$DIR..."
cd "\$DIR" && docker compose restart
echo "✅ Stack '\$STACK' restarted successfully."
EOF
        ;;
    prune)
        echo "Pruning dangling Docker images, unused networks, and build cache on homeserver..."
        $SSH_CMD "docker image prune -f && docker builder prune -f"
        echo "✅ Docker cleanup completed."
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Usage: $0 {list|stats|logs|restart|restart-stack|prune}"
        exit 1
        ;;
esac
