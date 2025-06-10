import unittest
import os
from core.parser import parse_instruction, parse
from core.instruction import Instruction

class TestParser(unittest.TestCase):
    def test_parse_r_type(self):
        instr = parse_instruction("ADD R1, R2, R3")
        self.assertIsInstance(instr, Instruction)
        self.assertEqual(instr.opcode, "ADD")
        self.assertEqual(instr.rd, "R1")
        self.assertEqual(instr.r1, "R2")
        self.assertEqual(instr.r2, "R3")
        self.assertIsNone(instr.imediato)

    def test_parse_i_type_addi(self):
        instr = parse_instruction("ADDI R1, R2, 10")
        self.assertEqual(instr.opcode, "ADDI")
        self.assertEqual(instr.rd, "R1")
        self.assertEqual(instr.r1, "R2")
        self.assertEqual(instr.imediato, 10)

    def test_parse_branch_beq(self):
        instr = parse_instruction("BEQ R1, R2, 8")
        self.assertEqual(instr.opcode, "BEQ")
        self.assertEqual(instr.r1, "R1")
        self.assertEqual(instr.r2, "R2")
        self.assertEqual(instr.imediato, 8)

    def test_parse_lw(self):
        instr = parse_instruction("LW R1, 4(R2)")
        self.assertEqual(instr.opcode, "LW")
        self.assertEqual(instr.rd, "R1")
        self.assertEqual(instr.r1, "R2")
        self.assertEqual(instr.imediato, 4)

    def test_parse_sw(self):
        instr = parse_instruction("SW R1, 8(R2)")
        self.assertEqual(instr.opcode, "SW")
        self.assertEqual(instr.r1, "R1")
        self.assertEqual(instr.r2, "R2")
        self.assertEqual(instr.imediato, 8)

    def test_parse_nop(self):
        instr = parse_instruction("NOP")
        self.assertEqual(instr.opcode, "NOP")
        self.assertIsNone(instr.rd)
        self.assertIsNone(instr.r1)
        self.assertIsNone(instr.r2)
        self.assertIsNone(instr.imediato)

    def test_invalid_opcode(self):
        with self.assertRaises(ValueError):
            parse_instruction("FOO R1, R2, R3")

    def test_wrong_operand_count(self):
        with self.assertRaises(ValueError):
            parse_instruction("ADD R1, R2")
        with self.assertRaises(ValueError):
            parse_instruction("ADDI R1, R2")
        with self.assertRaises(ValueError):
            parse_instruction("LW R1")
        with self.assertRaises(ValueError):
            parse_instruction("SW R1")
        with self.assertRaises(ValueError):
            parse_instruction("NOP R1")

    def test_invalid_lw_sw_format(self):
        with self.assertRaises(ValueError):
            parse_instruction("LW R1, R2")
        with self.assertRaises(ValueError):
            parse_instruction("SW R1, R2")

class TestParseFile(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'instructions_test.txt')

    def test_parse_file(self):
        instructions = parse(self.file_path)
        self.assertEqual(len(instructions), 6)
        self.assertEqual(instructions[0].opcode, 'ADD')
        self.assertEqual(instructions[1].opcode, 'ADDI')
        self.assertEqual(instructions[2].opcode, 'BEQ')
        self.assertEqual(instructions[3].opcode, 'LW')
        self.assertEqual(instructions[4].opcode, 'SW')
        self.assertEqual(instructions[5].opcode, 'NOP')
        self.assertEqual(instructions[0].rd, 'R1')
        self.assertEqual(instructions[1].imediato, 10)
        self.assertEqual(instructions[3].r1, 'R7')
        self.assertEqual(instructions[4].imediato, 12)
        self.assertIsNone(instructions[5].rd)
        # Testa os IDs
        for idx, instr in enumerate(instructions):
            self.assertEqual(instr.id, idx)

if __name__ == "__main__":
    unittest.main()
