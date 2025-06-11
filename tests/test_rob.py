import unittest
from core.rob import ReorderBuffer, ROBEntry

class TestReorderBuffer(unittest.TestCase):
    def setUp(self):
        self.rob = ReorderBuffer(size=4)

    def test_insert_and_peek_commit(self):
        entry = self.rob.insert('ADD', 'R1')
        self.assertIsInstance(entry, ROBEntry)
        self.assertEqual(self.rob.count, 1)
        self.assertEqual(self.rob.peek_commit(), entry)
        self.assertFalse(entry.ready)

    def test_mark_ready_and_commit(self):
        entry = self.rob.insert('AD', 'R2')
        self.rob.mark_ready(entry.id, 42)
        self.assertTrue(entry.ready)
        self.assertEqual(entry.value, 42)
        committed = self.rob.commit()
        self.assertEqual(committed, entry)
        self.assertEqual(self.rob.count, 0)

    def test_commit_not_ready(self):
        entry = self.rob.insert('ADD', 'R3')
        committed = self.rob.commit()
        self.assertIsNone(committed)
        self.assertEqual(self.rob.count, 1)

    def test_circular_behavior(self):
        entries = [self.rob.insert('ADD', f'R{i}') for i in range(4)]
        with self.assertRaises(Exception):
            self.rob.insert('ADD', 'R99')  # ROB cheio
        # Marca todos como prontos e commita
        for e in entries:
            self.rob.mark_ready(e.id, 100+e.id)
        for e in entries:
            committed = self.rob.commit()
            self.assertIsNotNone(committed)
        self.assertTrue(self.rob.is_empty())

    def test_repr(self):
        s = repr(self.rob)
        self.assertIn('head', s)
        self.assertIn('tail', s)
        self.assertIn('buffer', s)

if __name__ == "__main__":
    unittest.main()
