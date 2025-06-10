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

        def format_val(val):
            return str(val) if val is not None else "-"

        stage_str = " | ".join([
            f"Issue: {format_val(self.stage['issue'])}",
            f"Exec: {format_val(self.stage['execute_start'])}-{format_val(self.stage['execute_end'])}",
            f"WB: {format_val(self.stage['writeback'])}",
            f"Commit: {format_val(self.stage['commit'])}"
        ])

        info = [
            f"[Instr ID: {format_val(self.id)}] {self.raw}",
            f"Type: {self.type:<4} | Opcode: {self.opcode:<5} | Latency: {self.get_latency()}",
            f"Dest: {format_val(self.dest_register):<4} | Src: {', '.join(r for r in self.src_registers if r) or '-'}",
            f"Tag: {format_val(self.tag):<5} | ROB: {format_val(self.rob_entry):<8} | Branch: {'Yes' if self.branch else 'No'}",
            f"Stages: {stage_str}",
            "-" * 60  # separador
        ]

        return "\n".join(info)

