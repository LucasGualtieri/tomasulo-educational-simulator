"""
Unit tests for the `parse` function in core/parser.py

Covers:
- Happy paths: correct parsing of all supported instructions and combinations
- Edge cases: empty files, invalid lines, unsupported opcodes, malformed operands, etc.

Assumptions:
- The Instruction class is available and imported as in the tested file.
- The test file is a sibling to core/parser.py.
"""

import os
import tempfile
import pytest

from core.parser import parse
from core.instruction import Instruction

@pytest.mark.usefixtures("tmp_path")
class TestParse:
    # -------------------- HAPPY PATHS --------------------
    @pytest.mark.happy
    def test_parse_all_supported_instructions(self, tmp_path):
        """
        Test parsing a file with all supported instruction types, one of each.
        """
        content = (
            "ADD R1, R2, R3\n"
            "ADDI R4, R5, 10\n"
            "BEQ R6, R7, 20\n"
            "BNE R8, R9, 30\n"
            "LW R10, 100(R11)\n"
            "SW R12, 200(R13)\n"
            "NOP\n"
        )
        file_path = tmp_path / "instructions.txt"
        file_path.write_text(content)

        instructions = parse(str(file_path))
        assert len(instructions) == 7

        # ADD
        i = instructions[0]
        assert i.opcode == "ADD"
        assert i.rd == "R1"
        assert i.r1 == "R2"
        assert i.r2 == "R3"
        assert i.imediato is None

        # ADDI
        i = instructions[1]
        assert i.opcode == "ADDI"
        assert i.rd == "R4"
        assert i.r1 == "R5"
        assert i.imediato == 10
        assert i.r2 is None

        # BEQ
        i = instructions[2]
        assert i.opcode == "BEQ"
        assert i.r1 == "R6"
        assert i.r2 == "R7"
        assert i.imediato == 20
        assert i.rd is None

        # BNE
        i = instructions[3]
        assert i.opcode == "BNE"
        assert i.r1 == "R8"
        assert i.r2 == "R9"
        assert i.imediato == 30
        assert i.rd is None

        # LW
        i = instructions[4]
        assert i.opcode == "LW"
        assert i.rd == "R10"
        assert i.r1 == "R11"
        assert i.imediato == 100
        assert i.r2 is None

        # SW
        i = instructions[5]
        assert i.opcode == "SW"
        assert i.r1 == "R12"
        assert i.r2 == "R13"
        assert i.imediato == 200
        assert i.rd is None

        # NOP
        i = instructions[6]
        assert i.opcode == "NOP"
        assert i.rd is None
        assert i.r1 is None
        assert i.r2 is None
        assert i.imediato is None

    @pytest.mark.happy
    def test_parse_ignores_empty_and_whitespace_lines(self, tmp_path):
        """
        Test that empty lines and lines with only whitespace are ignored.
        """
        content = "\n   \nADD R1, R2, R3\n\n  \nNOP\n"
        file_path = tmp_path / "instructions.txt"
        file_path.write_text(content)

        instructions = parse(str(file_path))
        assert len(instructions) == 2
        assert instructions[0].opcode == "ADD"
        assert instructions[1].opcode == "NOP"

    @pytest.mark.happy
    def test_parse_trims_leading_and_trailing_spaces(self, tmp_path):
        """
        Test that leading and trailing spaces in instruction lines are trimmed.
        """
        content = "   ADD R1, R2, R3   \n   NOP   \n"
        file_path = tmp_path / "instructions.txt"
        file_path.write_text(content)

        instructions = parse(str(file_path))
        assert len(instructions) == 2
        assert instructions[0].opcode == "ADD"
        assert instructions[1].opcode == "NOP"

    @pytest.mark.happy
    def test_parse_is_case_sensitive(self, tmp_path):
        """
        Test that opcodes are case-sensitive (e.g., 'add' is not valid).
        """
        content = "add R1, R2, R3\nADD R1, R2, R3\n"
        file_path = tmp_path / "instructions.txt"
        file_path.write_text(content)

        # Only the second line should be parsed successfully
        instructions = parse(str(file_path))
        assert len(instructions) == 1
        assert instructions[0].opcode == "ADD"

    # -------------------- EDGE CASES --------------------
    @pytest.mark.edge
    def test_parse_empty_file(self, tmp_path):
        """
        Test parsing an empty file returns an empty list.
        """
        file_path = tmp_path / "empty.txt"
        file_path.write_text("")
        instructions = parse(str(file_path))
        assert instructions == []

    @pytest.mark.edge
    def test_parse_file_with_only_invalid_lines(self, tmp_path, capsys):
        """
        Test that a file with only invalid lines returns an empty list and prints errors.
        """
        content = "INVALID R1, R2, R3\nADDI R1, R2\nLW R1, 100R2\n"
        file_path = tmp_path / "bad.txt"
        file_path.write_text(content)
        instructions = parse(str(file_path))
        assert instructions == []
        captured = capsys.readouterr()
        assert "Unsupported opcode" in captured.out
        assert "ADDI expects 3 operands" in captured.out
        assert "Invalid format for LW operand" in captured.out

    @pytest.mark.edge
    def test_parse_mixed_valid_and_invalid_lines(self, tmp_path, capsys):
        """
        Test that valid lines are parsed and invalid lines are skipped with error messages.
        """
        content = (
            "ADD R1, R2, R3\n"
            "INVALID R1, R2, R3\n"
            "ADDI R4, R5, 10\n"
            "LW R10, 100(R11)\n"
            "SW R12, 200R13\n"  # malformed
            "NOP\n"
        )
        file_path = tmp_path / "mixed.txt"
        file_path.write_text(content)
        instructions = parse(str(file_path))
        assert len(instructions) == 4
        assert [i.opcode for i in instructions] == ["ADD", "ADDI", "LW", "NOP"]
        captured = capsys.readouterr()
        assert "Unsupported opcode" in captured.out
        assert "Invalid format for SW operand" in captured.out

    @pytest.mark.edge
    def test_parse_lw_and_sw_operand_format_errors(self, tmp_path, capsys):
        """
        Test that LW and SW with malformed operands are skipped and print errors.
        """
        content = (
            "LW R1, 100R2\n"      # missing parentheses
            "SW R1, (R2)\n"       # missing immediate
            "LW R1, 100(R2, R3)\n" # too many registers
        )
        file_path = tmp_path / "bad_lw_sw.txt"
        file_path.write_text(content)
        instructions = parse(str(file_path))
        assert instructions == []
        captured = capsys.readouterr()
        assert "Invalid format for LW operand" in captured.out
        assert "Invalid format for SW operand" in captured.out

    @pytest.mark.edge
    def test_parse_wrong_operand_count(self, tmp_path, capsys):
        """
        Test that instructions with wrong number of operands are skipped and print errors.
        """
        content = (
            "ADD R1, R2\n"         # too few
            "ADDI R1, R2, 10, 20\n" # too many
            "BEQ R1, R2\n"         # too few
            "LW R1\n"              # too few
            "SW R1, 100(R2), R3\n" # too many
            "NOP R1\n"             # NOP should have no operands
        )
        file_path = tmp_path / "bad_operands.txt"
        file_path.write_text(content)
        instructions = parse(str(file_path))
        assert instructions == []
        captured = capsys.readouterr()
        assert "ADD expects 3 operands" in captured.out
        assert "ADDI expects 3 operands" in captured.out
        assert "BEQ expects 3 operands" in captured.out
        assert "LW expects 2 operands" in captured.out
        assert "SW expects 2 operands" in captured.out
        assert "NOP expects no operands" in captured.out

    @pytest.mark.edge
    def test_parse_immediate_not_integer(self, tmp_path, capsys):
        """
        Test that instructions with non-integer immediates are skipped and print errors.
        """
        content = (
            "ADDI R1, R2, ten\n"
            "BEQ R1, R2, twenty\n"
            "LW R1, abc(R2)\n"
            "SW R1, xyz(R2)\n"
        )
        file_path = tmp_path / "bad_immediate.txt"
        file_path.write_text(content)
        instructions = parse(str(file_path))
        assert instructions == []
        captured = capsys.readouterr()
        assert "invalid literal for int()" in captured.out or "Invalid format for LW operand" in captured.out

    @pytest.mark.edge
    def test_parse_file_not_found(self):
        """
        Test that parsing a non-existent file raises FileNotFoundError.
        """
        with pytest.raises(FileNotFoundError):
            parse("nonexistent_file.txt")