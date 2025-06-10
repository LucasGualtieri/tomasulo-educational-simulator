import re

from core.instruction import Instruction

def parse_instruction(raw_text: str, id:int = 1) -> Instruction:
    raw_text = raw_text.strip()
    if not raw_text:
        raise ValueError("Empty instruction")

    # Get the opcode and remove it from the line
    tokens = raw_text.split(maxsplit=1)
    opcode = tokens[0].upper()
    operands = []
    if len(tokens) > 1:
        operands = [x.strip() for x in tokens[1].split(',') if x.strip()]

    rd = r1 = r2 = imediato = None

    # R-type instructions (e.g., ADD, SUB, MULT, DIV)
    if opcode in ["ADD", "SUB", "MULT", "DIV"]:
        if len(operands) != 3:
            raise ValueError(f"{opcode} expects 3 operands")
        rd, r1, r2 = operands

    # Immediate arithmetic: e.g., ADDI
    elif opcode == "ADDI":
        if len(operands) != 3:
            raise ValueError("ADDI expects 3 operands")
        rd, r1, immed_str = operands
        imediato = int(immed_str)

    # Branch instructions: e.g., BEQ, BNE (r1, r2, immediate)
    elif opcode in ["BEQ", "BNE"]:
        if len(operands) != 3:
            raise ValueError(f"{opcode} expects 3 operands")
        r1, r2, immed_str = operands
        imediato = int(immed_str)

    # Load word: LW rd, immediate(R register)
    elif opcode == "LW":
        if len(operands) != 2:
            raise ValueError("LW expects 2 operands")
        rd = operands[0]
        m = re.fullmatch(r"(\d+)\((R\d+)\)", operands[1])
        if not m:
            raise ValueError("Invalid format for LW operand (expected immediate(R?))")
        imediato = int(m.group(1))
        r1 = m.group(2)

    # Store word: SW r1, immediate(R register)
    elif opcode == "SW":
        if len(operands) != 2:
            raise ValueError("SW expects 2 operands")
        r1 = operands[0]
        m = re.fullmatch(r"(\d+)\((R\d+)\)", operands[1])
        if not m:
            raise ValueError("Invalid format for SW operand (expected immediate(R?))")
        imediato = int(m.group(1))
        r2 = m.group(2)

    # NOP with no operands
    elif opcode == "NOP":
        if operands:
            raise ValueError("NOP expects no operands")
        # nothing to assign

    else:
        raise ValueError("Unsupported opcode: " + opcode)

    return Instruction(opcode, rd=rd, r1=r1, r2=r2, imediato=imediato, raw_text=raw_text, id=id)

def parse(file_path: str) -> list:
    instructions = []
    id = 0
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # ignora linhas vazias
                try:
                    instr = parse_instruction(line, id)
                    id += 1
                    instructions.append(instr)
                except Exception as e:
                    print(f"Erro ao parsear a linha '{line}': {e}")
    return instructions
