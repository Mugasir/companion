# Conversation Runtime Blueprint (Text + Voice + Smart AI Core)

This document defines how to run Pookie in real-time with interruption support,
long-term memory, and a highly intelligent AI reasoning pipeline.

## Runtime components

1. **Input adapters**
   - Text input listener
   - Real-time speech recognition (ASR) listener with partial transcripts
2. **Dialogue manager**
   - Turn tracking
   - Interrupt detection
   - Context/state updates
3. **Smart reasoning engine**
   - Uses system prompt + profile memory + session memory + user intent analysis
   - Can call tools for planning, summarization, reminders, and project guidance
4. **Output adapters**
   - Text response stream
   - Voice synthesis (TTS) stream
5. **Memory store**
   - Profile memory (stable)
   - Episodic memory (recent sessions)
   - Long-term insights (goals, preferences, recurring concerns)

## State model

Maintain these states:

- `LISTENING`
- `THINKING`
- `SPEAKING`
- `INTERRUPTED`

Transition rules:

- `LISTENING -> THINKING` when user turn is complete
- `THINKING -> SPEAKING` when response generation starts
- `SPEAKING -> INTERRUPTED` when user starts talking or submits new text
- `INTERRUPTED -> LISTENING` immediately after stopping output stream
- `LISTENING -> THINKING` with newly captured user input

## Interruption handling (critical)

When interruption is detected:

1. Stop TTS/audio stream immediately.
2. Stop text streaming output immediately.
3. Mark unfinished assistant turn as cancelled.
4. Preserve context up to the last completed thought.
5. Process new user input as highest priority.
6. Continue naturally without awkward restarts.

Pseudo-flow:

```text
on_user_signal(input_chunk):
  if assistant_state == SPEAKING:
    stop_tts_stream()
    stop_text_stream()
    assistant_state = INTERRUPTED
  buffer_user_input(input_chunk)

on_user_turn_finalized(final_input):
  assistant_state = THINKING
  context = assemble_context(memory, conversation_history, final_input)
  response = smart_generate_response(context)
  assistant_state = SPEAKING
  stream_response(response)
```

## Smart AI reasoning loop

To make Pookie "highly smart", run this chain per turn:

1. **Intent detection**: emotional support, study help, project planning, or mixed.
2. **Emotion detection**: infer likely emotional tone and confidence level.
3. **Memory retrieval**: pull top relevant profile + project + recent commitments.
4. **Reasoning**: produce supportive and practical response with clear next action.
5. **Safety and quality check**: ensure tone is warm, respectful, and clear.
6. **Adaptive response length**: concise by default; expand on request.

## Context retention strategy

For each turn:

- Keep full short-term transcript for current session.
- Summarize every N turns into rolling memory notes.
- Store durable items only when relevant (goals, commitments, preferences, milestones).

Memory write criteria (save only if true):

- Important personal fact
- Ongoing project update
- Long-term goal or deadline
- Emotional pattern recurring over time
- Explicit user preference

## Emotional intelligence loop

Before finalizing each response:

1. What emotion is likely present?
2. Did we acknowledge it clearly?
3. Did we provide practical next-step support?
4. Is the tone warm and natural?
5. Did we ask at most 1-2 useful questions?

## Recommended response structure

For emotionally loaded turns:

1. Validate feeling
2. Clarify focus with one question
3. Offer one practical action
4. Encourage based on known strengths

For technical/study turns:

1. Confirm objective
2. Explain clearly in steps
3. Provide concrete example
4. Ask if Calvin wants deeper or simpler version

## AI integration recommendations

- Use a streaming LLM API for low-latency conversational feel.
- Use cancellable async tasks for both text and TTS streams.
- Trigger interruption when VAD detects speech during TTS.
- Tag each assistant message with a `turn_id` so cancellation is precise.
- Keep memory retrieval fast via hybrid profile + recent-summary lookups.
- Add a reflection pass for complex planning prompts (optional, under latency budget).

## Acceptance checklist

- Calvin can use text or voice interchangeably.
- Pookie responses feel warm, human, and smart.
- Interrupting Pookie halts output immediately.
- New direction is handled without context loss.
- System remembers Calvin's studies, projects, goals, and priorities across sessions.
