from core.instruction import Instruction

class ReservationStationEntry:
    def __init__(self, name):
        self.name = name  # Nome da estação (ex: 'Add1', 'Mul2')
        self.busy = False
        self.op = None  # Operação (ex: 'ADD', 'MUL')
        self.Vj = None  # Valor do operando j (se disponível)
        self.Vk = None  # Valor do operando k (se disponível)
        self.Qj = None  # Tag da estação produtora de j (se aguardando)
        self.Qk = None  # Tag da estação produtora de k (se aguardando)
        self.A = None   # Endereço efetivo (para LOAD/STORE)
        self.instr = None  # Referência para a instrução
        self.rob_entry = None  # Entrada correspondente no ROB
        self.done = False  # Se a execução terminou

    def clear(self):
        self.busy = False
        self.op = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None
        self.instr = None
        self.rob_entry = None
        self.done = False

    def __repr__(self):
        return (f"<RS {self.name} busy={self.busy} op={self.op} Vj={self.Vj} Vk={self.Vk} "
                f"Qj={self.Qj} Qk={self.Qk} A={self.A} done={self.done}>")

class ReservationStation:
    def __init__(self, name, size):
        self.name = name
        self.entries = [ReservationStationEntry(f"{name}{i+1}") for i in range(size)]

    def has_free(self):
        return any(not entry.busy for entry in self.entries)

    def get_free(self):
        for entry in self.entries:
            if not entry.busy:
                return entry
        return None

    def __iter__(self):
        return iter(self.entries)

    def __repr__(self):
        return f"<ReservationStation {self.name}: {[str(e) for e in self.entries]}>"
