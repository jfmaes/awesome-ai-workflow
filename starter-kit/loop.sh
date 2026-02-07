#!/bin/bash
set -euo pipefail

# =============================================================================
# Ralph Loop — Enhanced with plan-work and reflect modes
# =============================================================================
# Usage:
#   ./loop.sh                              # Build mode, unlimited iterations
#   ./loop.sh 20                           # Build mode, max 20 iterations
#   ./loop.sh plan                         # Plan mode, unlimited
#   ./loop.sh plan 5                       # Plan mode, max 5 iterations
#   ./loop.sh plan-work "description"      # Scoped plan for feature branch
#   ./loop.sh plan-work "description" 5    # Scoped plan, max 5 iterations
#   ./loop.sh reflect                      # Reflection mode (run after build session)
# =============================================================================

# --- Configuration ---
# Override these via environment variables if needed
CLAUDE_MODEL="${RALPH_MODEL:-opus}"          # opus for planning/complex, sonnet for speed
PROMPTS_DIR="${RALPH_PROMPTS_DIR:-prompts}"  # directory containing prompt files

# --- Parse arguments ---
MODE="build"
PROMPT_FILE="${PROMPTS_DIR}/PROMPT_build.md"
MAX_ITERATIONS=0
WORK_SCOPE=""

case "${1:-}" in
    plan)
        MODE="plan"
        PROMPT_FILE="${PROMPTS_DIR}/PROMPT_plan.md"
        MAX_ITERATIONS=${2:-0}
        ;;
    plan-work)
        if [ -z "${2:-}" ]; then
            echo "Error: plan-work requires a work description"
            echo "Usage: ./loop.sh plan-work \"user auth with OAuth\""
            exit 1
        fi
        MODE="plan-work"
        WORK_SCOPE="$2"
        PROMPT_FILE="${PROMPTS_DIR}/PROMPT_plan_work.md"
        MAX_ITERATIONS=${3:-5}
        ;;
    reflect)
        MODE="reflect"
        PROMPT_FILE="${PROMPTS_DIR}/PROMPT_reflect.md"
        MAX_ITERATIONS=1  # Reflect is typically one pass
        ;;
    [0-9]*)
        MAX_ITERATIONS=$1
        ;;
    "")
        # defaults already set
        ;;
    *)
        echo "Unknown mode: $1"
        echo "Usage: ./loop.sh [plan|plan-work|reflect] [max_iterations]"
        exit 1
        ;;
esac

# --- Verify prompt file exists ---
if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: $PROMPT_FILE not found"
    echo "Available prompts:"
    ls -1 "${PROMPTS_DIR}"/PROMPT_*.md 2>/dev/null || echo "  None found in ${PROMPTS_DIR}/"
    exit 1
fi

# --- For plan-work: substitute WORK_SCOPE into prompt ---
EFFECTIVE_PROMPT=""
if [ "$MODE" = "plan-work" ]; then
    EFFECTIVE_PROMPT=$(sed "s/\${WORK_SCOPE}/${WORK_SCOPE}/g" "$PROMPT_FILE")
else
    EFFECTIVE_PROMPT=$(cat "$PROMPT_FILE")
fi

# --- Display config ---
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "not-a-git-repo")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 Ralph Loop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Mode:   $MODE"
echo "  Prompt: $PROMPT_FILE"
echo "  Model:  $CLAUDE_MODEL"
echo "  Branch: $CURRENT_BRANCH"
[ $MAX_ITERATIONS -gt 0 ] && echo "  Max:    $MAX_ITERATIONS iterations"
[ -n "$WORK_SCOPE" ] && echo "  Scope:  $WORK_SCOPE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# --- Safety check ---
read -p "Start loop? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# --- Main loop ---
ITERATION=0

while true; do
    if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
        echo ""
        echo "━━━ Reached max iterations: $MAX_ITERATIONS ━━━"
        break
    fi

    ITERATION=$((ITERATION + 1))
    echo ""
    echo "======================== ITERATION $ITERATION ========================"
    echo ""

    # Run Claude with the prompt
    # -p: headless mode (non-interactive, reads from stdin)
    # --dangerously-skip-permissions: auto-approve all tool calls
    # --model: select model (opus for planning/complex, sonnet for speed)
    # --verbose: detailed logging
    echo "$EFFECTIVE_PROMPT" | claude -p \
        --dangerously-skip-permissions \
        --model "$CLAUDE_MODEL" \
        --verbose

    # Push changes after each iteration (build/plan-work modes)
    if [ "$MODE" = "build" ] || [ "$MODE" = "plan-work" ]; then
        git push origin "$CURRENT_BRANCH" 2>/dev/null || {
            echo "Push failed. Creating remote branch..."
            git push -u origin "$CURRENT_BRANCH" 2>/dev/null || echo "Warning: push failed (may not be a git repo)"
        }
    fi

    echo ""
    echo "━━━ Iteration $ITERATION complete ━━━"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏁 Loop finished after $ITERATION iteration(s)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# --- Post-loop suggestion ---
if [ "$MODE" = "build" ] && [ $ITERATION -gt 3 ]; then
    echo ""
    echo "💡 Tip: Run './loop.sh reflect' to capture learnings from this session"
fi
