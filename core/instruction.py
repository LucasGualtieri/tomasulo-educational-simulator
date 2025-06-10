class Instruction:

    LATENCIES = {
        'ADD': 1, 'SUB': 1, 'ADDI': 1,
        'MUL': 3, 'DIV': 8,
        'LW': 2, 'SW': 2,
        'BEQ': 1, 'BNE': 1, 'BLT': 1, 'BGT': 1,
        'J': 1, 'JAL': 1,
        'NOP': 1
    }

    def __init__(self, opcode, rd=None, r1=None, r2=None, imediato=None, raw_text=None, id=None):

        self.opcode = opcode.upper()
        self.rd = rd
        self.r1 = r1
        self.r2 = r2
        self.imediato = imediato
        self.raw = raw_text or self._generate_raw()
        self.id = id

        # Inferir tipo
        self.type = self._infer_type()

        # Estágios do Tomasulo
        self.stage = {
            'issue': None,
            'execute_start': None,
            'execute_end': None,
            'writeback': None,
            'commit': None
        }

        # Dependências
        self.src_registers = self._get_sources()
        self.dest_register = self._get_dest()
        self.tag = None
        self.rob_entry = None

        # Especulação
        self.branch = self.opcode in ['BEQ', 'BNE', 'BLT', 'BGT']
        self.predicted_taken = None
        self.actual_taken = None
        self.speculative = False

        # Execução
        self.result = None
        self.address = None
        self.exception = None

    def _infer_type(self):
        if self.opcode in ['J', 'JAL']:
            return 'J'
        elif self.opcode in ['BEQ', 'BNE', 'BLT', 'BGT', 'ADDI', 'LW', 'SW']:
            return 'I'
        elif self.opcode == 'NOP':
            return 'NOP'
        else:
            return 'R'

    def _get_sources(self):
        if self.opcode in ['ADD', 'SUB', 'MUL', 'DIV']:
            return [self.r1, self.r2]
        elif self.opcode in ['ADDI']:
            return [self.r1]
        elif self.opcode.startswith('L'):  # LW, etc.
            return [self.r1]
        elif self.opcode.startswith('S'):  # SW, etc.
            return [self.r1, self.r2]
        elif self.opcode in ['BEQ', 'BNE', 'BLT', 'BGT']:
            return [self.r1, self.r2]
        else:
            return []

    def _get_dest(self):
        if self.opcode in ['ADD', 'SUB', 'MUL', 'DIV', 'ADDI', 'LW']:
            return self.rd
        return None

    def _generate_raw(self):
        """Gera string raw caso não tenha sido fornecida"""
        if self.opcode in ['ADD', 'SUB', 'MUL', 'DIV']:
            return f"{self.opcode} {self.rd}, {self.r1}, {self.r2}"
        elif self.opcode in ['ADDI']:
            return f"{self.opcode} {self.rd}, {self.r1}, {self.imediato}"
        elif self.opcode in ['LW', 'SW']:
            return f"{self.opcode} {self.rd}, {self.imediato}({self.r1})"
        elif self.opcode in ['BEQ', 'BNE', 'BLT', 'BGT']:
            return f"{self.opcode} {self.r1}, {self.r2}, {self.imediato}"
        elif self.opcode == 'NOP':
            return 'NOP'
        else:
            return f"{self.opcode}"

    def get_latency(self):
        return self.LATENCIES.get(self.opcode, 1)

    def is_branch(self):
        return self.branch

    def is_memory_op(self):
        return self.opcode in ['LW', 'SW', 'LB', 'SB', 'LH', 'SH']

    def is_arithmetic(self):
        return self.opcode in {'ADD', 'SUB', 'MUL', 'DIV', 'ADDI', 'AND', 'OR'}

    def __str__(self):
        width = 58
        linha_horizontal = '─' * width
        instr_id = f"Instrução {self.id if self.id is not None else '-'}"
        padding = width - len(instr_id) - 2  # 2 for the spaces around the title
        header = f"┌─ {instr_id} {'─' * padding}┐"

        raw_line = f"│ Raw: {self.raw:<{width - 7}}│"  # 7 = len("│ Raw: ") + 1

        info_line_1 = f"│ Opcode: {self.opcode:<8} │ Type: {self.type:<4} │ Latency: {self.get_latency():<2} │"
        srcs = ', '.join(r for r in self.src_registers if r)
        info_line_2 = f"│ Dest: {self.dest_register or '-':<5} │ Src: {srcs or '-':<25}│"

        stage_line = (
            f"│ Estágios: issue:{self.stage['issue'] or '-':<2} | "
            f"execute_start:{self.stage['execute_start'] or '-':<2} | "
            f"execute_end:{self.stage['execute_end'] or '-':<2} | "
            f"writeback:{self.stage['writeback'] or '-':<2} | "
            f"commit:{self.stage['commit'] or '-':<2} │"
        )

        meta_line = (
            f"│ Tag: {str(self.tag) if self.tag else '-':<5} │ "
            f"ROB: {str(self.rob_entry) if self.rob_entry else '-':<5} │ "
            f"Branch: {'Sim' if self.branch else 'Não':<3} │"
        )

        return '\n'.join([
            header,
            raw_line,
            f"├{linha_horizontal}┤",
            info_line_1,
            info_line_2,
            f"├{linha_horizontal}┤",
            stage_line,
            meta_line,
            f"└{linha_horizontal}┘"
        ])
