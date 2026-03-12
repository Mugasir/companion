from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class AssistantState(str, Enum):
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    SPEAKING = "SPEAKING"
    INTERRUPTED = "INTERRUPTED"


@dataclass
class Turn:
    role: str
    content: str
    turn_id: int
    cancelled: bool = False


@dataclass
class PookieCompanion:
    """
    Runtime core for Pookie.

    This class is intentionally provider-agnostic so it can be integrated with
    OpenAI, local LLMs, or other AI backends. It focuses on conversation state,
    interruption handling, and memory-aware context assembly.
    """

    profile_memory: Dict
    state: AssistantState = AssistantState.LISTENING
    turns: List[Turn] = field(default_factory=list)
    next_turn_id: int = 1
    active_assistant_turn_id: Optional[int] = None

    def add_user_message(self, text: str) -> None:
        if self.state == AssistantState.SPEAKING:
            self.interrupt()
        self.turns.append(Turn(role="user", content=text.strip(), turn_id=self._alloc_turn_id()))
        self.state = AssistantState.THINKING

    def start_assistant_message(self, draft_text: str) -> int:
        self.state = AssistantState.SPEAKING
        turn = Turn(role="assistant", content=draft_text, turn_id=self._alloc_turn_id())
        self.turns.append(turn)
        self.active_assistant_turn_id = turn.turn_id
        return turn.turn_id

    def complete_assistant_message(self) -> None:
        self.active_assistant_turn_id = None
        self.state = AssistantState.LISTENING

    def interrupt(self) -> None:
        if self.state != AssistantState.SPEAKING:
            return
        self.state = AssistantState.INTERRUPTED
        if self.active_assistant_turn_id is not None:
            turn = self._find_turn(self.active_assistant_turn_id)
            if turn:
                turn.cancelled = True
        self.active_assistant_turn_id = None
        self.state = AssistantState.LISTENING

    def build_context(self, latest_user_input: str) -> Dict:
        """Builds rich context payload for an AI reasoning engine."""
        recent_turns = [
            {
                "role": t.role,
                "content": t.content,
                "turn_id": t.turn_id,
                "cancelled": t.cancelled,
            }
            for t in self.turns[-12:]
            if not t.cancelled
        ]
        return {
            "profile": self.profile_memory,
            "recent_turns": recent_turns,
            "latest_input": latest_user_input,
            "state": self.state.value,
            "emotional_checklist": [
                "detect_user_emotion",
                "acknowledge_feeling",
                "provide_actionable_next_step",
                "keep_warm_human_tone",
            ],
        }

    def _alloc_turn_id(self) -> int:
        tid = self.next_turn_id
        self.next_turn_id += 1
        return tid

    def _find_turn(self, turn_id: int) -> Optional[Turn]:
        for t in self.turns:
            if t.turn_id == turn_id:
                return t
        return None
