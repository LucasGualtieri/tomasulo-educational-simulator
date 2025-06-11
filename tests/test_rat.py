import unittest
from core.rat import RegisterAliasTable

class TestRegisterAliasTable(unittest.TestCase):
    def setUp(self):
        self.rat = RegisterAliasTable(num_registers=4)

    def test_initial_state(self):
        for i in range(4):
            reg = f'R{i}'
            self.assertIsNone(self.rat.get_tag(reg))
            self.assertTrue(self.rat.is_valid(reg))

    def test_set_alias_and_validity(self):
        self.rat.set_alias('R1', 'TAG1')
        self.assertEqual(self.rat.get_tag('R1'), 'TAG1')
        self.assertFalse(self.rat.is_valid('R1'))

    def test_set_valid(self):
        self.rat.set_alias('R2', 'TAG2')
        self.rat.set_valid('R2')
        self.assertTrue(self.rat.is_valid('R2'))
        self.assertEqual(self.rat.get_tag('R2'), 'TAG2')

    def test_clear_alias(self):
        self.rat.set_alias('R3', 'TAG3')
        self.rat.clear_alias('R3', 'TAG3')
        self.assertIsNone(self.rat.get_tag('R3'))
        self.assertTrue(self.rat.is_valid('R3'))

    def test_clear_alias_wrong_tag(self):
        self.rat.set_alias('R1', 'TAG1')
        self.rat.clear_alias('R1', 'TAGX')  # Não deve limpar
        self.assertEqual(self.rat.get_tag('R1'), 'TAG1')
        self.assertFalse(self.rat.is_valid('R1'))

    def test_repr(self):
        s = repr(self.rat)
        self.assertIn('R0', s)
        self.assertIn('tag', s)
        self.assertIn('valid', s)

if __name__ == "__main__":
    unittest.main()
