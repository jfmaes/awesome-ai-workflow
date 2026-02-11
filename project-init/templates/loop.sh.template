#!/bin/bash
set -uo pipefail

# =============================================================================
# Ralph Loop — Multi-CLI support (Claude Code + OpenAI Codex)
# =============================================================================
# Usage:
#   ./loop.sh build                        # Build mode, unlimited iterations
#   ./loop.sh build 20                     # Build mode, max 20 iterations
#   ./loop.sh plan                         # Plan mode, unlimited
#   ./loop.sh plan 5                       # Plan mode, max 5 iterations
#   ./loop.sh plan-work "description"      # Scoped plan for feature branch
#   ./loop.sh plan-work "description" 5    # Scoped plan, max 5 iterations
#   ./loop.sh reflect                      # Reflection mode (run after build session)
#
# Environment variables:
#   RALPH_CLI=claude|codex                 # Force CLI (auto-detected if unset)
#   RALPH_MODEL=<model>                    # Override model for all modes
#   RALPH_PROMPTS_DIR=<dir>               # Override prompts directory (default: prompts)
# =============================================================================

# --- Configuration ---
RALPH_CLI="${RALPH_CLI:-}"
PROMPTS_DIR="${RALPH_PROMPTS_DIR:-prompts}"
LOG_DIR="logs"

# --- CLI detection ---
if [ -z "$RALPH_CLI" ]; then
    if command -v claude &>/dev/null; then
        RALPH_CLI="claude"
    elif command -v codex &>/dev/null; then
        RALPH_CLI="codex"
    else
        echo "Error: Neither 'claude' nor 'codex' CLI found in PATH"
        echo "Install one of:"
        echo "  Claude Code: https://docs.anthropic.com/en/docs/claude-code"
        echo "  Codex CLI:   npm install -g @openai/codex"
        exit 1
    fi
fi

# --- Model defaults per CLI ---
# Claude: sonnet (fast build), opus (deep planning/reflection)
# Codex:  codex (default for all modes)
cli_model_build() {
    if [ "$RALPH_CLI" = "claude" ]; then echo "sonnet"; else echo "codex"; fi
}
cli_model_plan() {
    if [ "$RALPH_CLI" = "claude" ]; then echo "opus"; else echo "codex"; fi
}

# --- Parse arguments ---
MODE=""
PROMPT_FILE=""
MAX_ITERATIONS=0
WORK_SCOPE=""
CLI_MODEL=""

case "${1:-}" in
    build)
        MODE="build"
        CLI_MODEL="${RALPH_MODEL:-$(cli_model_build)}"
        PROMPT_FILE="${PROMPTS_DIR}/PROMPT_build.md"
        MAX_ITERATIONS=${2:-0}
        ;;
    plan)
        MODE="plan"
        CLI_MODEL="${RALPH_MODEL:-$(cli_model_plan)}"
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
        CLI_MODEL="${RALPH_MODEL:-$(cli_model_plan)}"
        WORK_SCOPE="$2"
        PROMPT_FILE="${PROMPTS_DIR}/PROMPT_plan_work.md"
        MAX_ITERATIONS=${3:-5}
        ;;
    reflect)
        MODE="reflect"
        CLI_MODEL="${RALPH_MODEL:-$(cli_model_plan)}"
        PROMPT_FILE="${PROMPTS_DIR}/PROMPT_reflect.md"
        MAX_ITERATIONS=1  # Reflect is typically one pass
        ;;
    *)
        echo "Usage: ./loop.sh <mode> [options]"
        echo ""
        echo "Modes:"
        echo "  build [max_iterations]              Build mode (implements tasks from plan)"
        echo "  plan [max_iterations]               Plan mode (creates/updates implementation plan)"
        echo "  plan-work \"description\" [max_iter]   Scoped plan for a specific feature"
        echo "  reflect                             Reflection mode (run after build session)"
        echo ""
        echo "Environment variables:"
        echo "  RALPH_CLI=claude|codex              Force CLI (auto-detected if unset)"
        echo "  RALPH_MODEL=<model>                 Override model (claude: sonnet/opus, codex: codex)"
        echo "  RALPH_PROMPTS_DIR=<dir>             Override prompts directory (default: prompts)"
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

# --- Ensure log directory exists ---
mkdir -p "$LOG_DIR"

# --- Display config ---
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "not-a-git-repo")
HAS_REMOTE=$(git remote 2>/dev/null | head -1)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ralph Loop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  CLI:    $RALPH_CLI"
echo "  Mode:   $MODE"
echo "  Prompt: $PROMPT_FILE"
echo "  Model:  $CLI_MODEL"
echo "  Branch: $CURRENT_BRANCH"
echo "  Remote: ${HAS_REMOTE:-none}"
[ $MAX_ITERATIONS -gt 0 ] && echo "  Max:    $MAX_ITERATIONS iterations"
[ -n "$WORK_SCOPE" ] && echo "  Scope:  $WORK_SCOPE"
echo "  Logs:   $LOG_DIR/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# --- Pre-flight checks ---
# Check if we're in a git repository (required for loop operation)
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    echo "The Ralph loop requires git for commit tracking and push operations."
    echo "Run 'git init' to initialize a repository first."
    exit 1
fi

# --- Safety check ---
read -p "Start loop? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# --- CLI execution functions ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_claude() {
    local prompt="$1"
    local model="$2"
    local log_file="$3"

    echo "$prompt" | claude -p \
        --dangerously-skip-permissions \
        --model "$model" \
        --output-format stream-json \
        --verbose \
        2>&1 | tee "${log_file}.jsonl" | python3 -u "${SCRIPT_DIR}/ralph_stream_parser.py"
}

run_codex() {
    local prompt="$1"
    local model="$2"
    local log_file="$3"

    codex exec \
        --yolo \
        --model "$model" \
        --json \
        "$prompt" \
        2>&1 | tee "${log_file}.jsonl" | python3 -u "${SCRIPT_DIR}/ralph_stream_parser.py"
}

# --- Main loop ---
ITERATION=0
REVIEW_APPROVED=0
REVIEW_FIXED=0
REVIEW_DISCARDED=0
REVIEW_SKIPPED=0

while true; do
    if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
        echo ""
        echo "--- Reached max iterations: $MAX_ITERATIONS ---"
        break
    fi

    ITERATION=$((ITERATION + 1))
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    LOG_FILE="${LOG_DIR}/ralph_${MODE}_${TIMESTAMP}_iter${ITERATION}.log"

    echo ""
    echo "======================== ITERATION $ITERATION ========================"
    echo "  Started: $(date)"
    echo "  Log:     $LOG_FILE"
    echo ""

    # Run the selected CLI
    if [ "$RALPH_CLI" = "claude" ]; then
        run_claude "$EFFECTIVE_PROMPT" "$CLI_MODEL" "$LOG_FILE"
    elif [ "$RALPH_CLI" = "codex" ]; then
        run_codex "$EFFECTIVE_PROMPT" "$CLI_MODEL" "$LOG_FILE"
    else
        echo "Error: Unknown CLI '$RALPH_CLI' (expected 'claude' or 'codex')"
        exit 1
    fi

    CLI_EXIT=${PIPESTATUS[0]:-0}

    if [ "$CLI_EXIT" -ne 0 ] 2>/dev/null; then
        echo ""
        echo "*** $RALPH_CLI exited with code $CLI_EXIT ***"
        echo "Check log: ${LOG_FILE}.jsonl"
        echo "Continuing to next iteration..."
    fi

    # After build iteration, run review (build mode only)
    if [ "$MODE" = "build" ] && [ -f "${PROMPTS_DIR}/PROMPT_review.md" ]; then
        REVIEW_PROMPT=$(cat "${PROMPTS_DIR}/PROMPT_review.md")
        REVIEW_LOG="${LOG_DIR}/ralph_review_${TIMESTAMP}_iter${ITERATION}.log"

        echo ""
        echo "  >>> Review phase..."
        if [ "$RALPH_CLI" = "claude" ]; then
            run_claude "$REVIEW_PROMPT" "$CLI_MODEL" "$REVIEW_LOG"
        else
            run_codex "$REVIEW_PROMPT" "$CLI_MODEL" "$REVIEW_LOG"
        fi

        # Read and display score
        if [ -f ".ralph_review_score" ]; then
            source .ralph_review_score
            echo "  Review: score=$SCORE action=$ACTION"
            case "$ACTION" in
                approved)  REVIEW_APPROVED=$((REVIEW_APPROVED + 1)) ;;
                fixed)     REVIEW_FIXED=$((REVIEW_FIXED + 1)) ;;
                discarded) REVIEW_DISCARDED=$((REVIEW_DISCARDED + 1)) ;;
                skipped)   REVIEW_SKIPPED=$((REVIEW_SKIPPED + 1)) ;;
            esac
            rm -f .ralph_review_score
        fi
    fi

    # Push changes after each iteration (build/plan-work modes) — only if remote exists
    if [ -n "$HAS_REMOTE" ] && { [ "$MODE" = "build" ] || [ "$MODE" = "plan-work" ]; }; then
        echo ""
        echo "Pushing changes..."
        git push origin "$CURRENT_BRANCH" 2>&1 || {
            echo "Push failed. Creating remote branch..."
            git push -u origin "$CURRENT_BRANCH" 2>&1 || echo "Warning: push failed"
        }
    fi

    echo ""
    echo "--- Iteration $ITERATION complete ($(date)) ---"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Loop finished after $ITERATION iteration(s)"
if [ "$MODE" = "build" ] && [ $((REVIEW_APPROVED + REVIEW_FIXED + REVIEW_DISCARDED + REVIEW_SKIPPED)) -gt 0 ]; then
    echo "Reviews: $REVIEW_APPROVED approved, $REVIEW_FIXED fixed, $REVIEW_DISCARDED discarded, $REVIEW_SKIPPED skipped"
fi
echo "Logs: $LOG_DIR/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# --- Post-loop suggestions ---
if [ "$MODE" = "build" ] && [ $ITERATION -gt 3 ]; then
    echo ""
    echo "Tip: Run './loop.sh reflect' to capture learnings from this session"
fi
if [ "$MODE" = "build" ] && [ $REVIEW_DISCARDED -gt 2 ]; then
    echo "Warning: $REVIEW_DISCARDED discards — consider re-running './loop.sh plan' to improve task definitions"
fi
