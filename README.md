# Pookie Companion

Pookie is a realistic, emotionally intelligent AI companion designed for **Calvin Mugasira**.

This repository now includes both design artifacts and a starter runtime core that can be integrated with a real AI model provider.

## What is included

- `pookie_system_prompt.md` — complete companion behavior prompt
- `pookie_profile_memory.json` — persistent memory seed for Calvin's profile and goals
- `conversation_runtime.md` — voice/text architecture with interruption handling and smart reasoning loop
- `src/pookie_companion.py` — Python conversation state engine with interruption-aware turn management
- `tests/test_pookie_companion.py` — unit tests for state transitions and context behavior

## Quick start

1. Load `pookie_system_prompt.md` as your LLM system instruction.
2. Load `pookie_profile_memory.json` into your memory store.
3. Use `PookieCompanion` from `src/pookie_companion.py` to manage runtime state.
4. Connect your model (OpenAI/local/other) to `build_context()` and stream responses.
5. Wire TTS + ASR with interruption cancellation as defined in `conversation_runtime.md`.

## Goal

Build a warm, highly smart, context-aware companion that supports Calvin's emotional wellbeing, studies, innovation projects, and long-term ambitions through natural text and voice conversation.
