import unittest

from core.instruction import Instruction

class TestInstruction(unittest.TestCase):

    def test_r_type_instruction(self):
        instr = Instruction("ADD", rd="R1", r1="R2", r2="R3")
        self.assertEqual(instr.opcode, "ADD")
        self.assertEqual(instr.type, "R")
        self.assertEqual(instr.dest_register, "R1")
        self.assertListEqual(instr.src_registers, ["R2", "R3"])
        self.assertEqual(instr.get_latency(), 1)
        self.assertIn("ADD R1, R2, R3", instr.raw)

    def test_i_type_arithmetic(self):
        instr = Instruction("ADDI", rd="R1", r1="R2", imediato=10)
        self.assertEqual(instr.type, "I")
        self.assertEqual(instr.dest_register, "R1")
        self.assertListEqual(instr.src_registers, ["R2"])
        self.assertEqual(instr.get_latency(), 1)

    def test_memory_instruction_lw(self):
        instr = Instruction("LW", rd="R1", r1="R2", imediato=4)
        self.assertEqual(instr.type, "I")
        self.assertEqual(instr.dest_register, "R1")
        self.assertListEqual(instr.src_registers, ["R2"])
        self.assertEqual(instr.get_latency(), 2)
        self.assertTrue(instr.is_memory_op())

    def test_memory_instruction_sw(self):
        instr = Instruction("SW", rd="R1", r1="R2", r2="R3", imediato=8)
        self.assertIsNone(instr.dest_register)
        self.assertListEqual(instr.src_registers, ["R2", "R3"])
        self.assertTrue(instr.is_memory_op())

    def test_branch_instruction(self):
        instr = Instruction("BEQ", r1="R1", r2="R2", imediato=12)
        self.assertTrue(instr.is_branch())
        self.assertEqual(instr.type, "I")
        self.assertListEqual(instr.src_registers, ["R1", "R2"])

    def test_j_type_instruction(self):
        instr = Instruction("J")
        self.assertEqual(instr.type, "J")
        self.assertEqual(instr.get_latency(), 1)

    def test_nop_instruction(self):
        instr = Instruction("NOP")
        self.assertEqual(instr.type, "NOP")
        self.assertEqual(instr.get_latency(), 1)
        self.assertEqual(instr.raw, "NOP")

    def test_arithmetic_check(self):
        instr = Instruction("MUL", rd="R1", r1="R2", r2="R3")
        self.assertTrue(instr.is_arithmetic())
        self.assertFalse(instr.is_memory_op())
        self.assertFalse(instr.is_branch())

    def test_string_representation(self):
        instr = Instruction("ADD", rd="R1", r1="R2", r2="R3", id=0)
        output = str(instr)
        
        self.assertIn("Instr ID: 0", output)
        self.assertIn("ADD R1, R2, R3", output)
        self.assertIn("Opcode: ADD", output)
        self.assertIn("Dest: R1", output)
        self.assertIn("Src: R2, R3", output)
        self.assertIn("Stages: Issue:", output)

if __name__ == "__main__":
    unittest.main()