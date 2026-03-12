import json
import unittest
from pathlib import Path

from src.pookie_companion import AssistantState, PookieCompanion


class TestPookieCompanion(unittest.TestCase):
    def setUp(self):
        profile = json.loads(Path('pookie_profile_memory.json').read_text())
        self.engine = PookieCompanion(profile_memory=profile)

    def test_user_message_moves_to_thinking(self):
        self.engine.add_user_message("Hello Pookie")
        self.assertEqual(self.engine.state, AssistantState.THINKING)

    def test_interrupt_marks_assistant_turn_cancelled(self):
        self.engine.add_user_message("Plan my day")
        turn_id = self.engine.start_assistant_message("Sure, let's build a plan")
        self.assertEqual(self.engine.state, AssistantState.SPEAKING)
        self.engine.interrupt()
        self.assertEqual(self.engine.state, AssistantState.LISTENING)
        cancelled_turn = [t for t in self.engine.turns if t.turn_id == turn_id][0]
        self.assertTrue(cancelled_turn.cancelled)

    def test_context_excludes_cancelled_turns(self):
        self.engine.add_user_message("I am overwhelmed")
        self.engine.start_assistant_message("Let's slow down")
        self.engine.interrupt()
        ctx = self.engine.build_context("I want to focus on EduTrack")
        assistant_turns = [t for t in ctx["recent_turns"] if t["role"] == "assistant"]
        self.assertEqual(len(assistant_turns), 0)


if __name__ == '__main__':
    unittest.main()
