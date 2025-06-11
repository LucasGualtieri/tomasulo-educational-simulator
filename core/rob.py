class ROBEntry:
    def __init__(self, entry_id, instr_type, dest, value=None, ready=False, instr=None):
        self.id = entry_id
        self.type = instr_type  # Tipo da instrução (ex: 'ADD', 'LW', ...)
        self.dest = dest        # Registrador destino ou None
        self.value = value      # Valor a ser escrito
        self.ready = ready      # Pronto para commit?
        self.instr = instr      # Referência para a instrução

    def __repr__(self):
        return f"<ROBEntry id={self.id} type={self.type} dest={self.dest} value={self.value} ready={self.ready}>"

class ReorderBuffer:
    def __init__(self, size=16):
        self.size = size
        self.buffer = [None] * size
        self.head = 0  # Posição de commit
        self.tail = 0  # Posição de escrita
        self.count = 0
        self.next_id = 0

    def is_full(self):
        return self.count == self.size

    def is_empty(self):
        return self.count == 0

    def insert(self, instr_type, dest, instr=None):
        if self.is_full():
            raise Exception("ROB cheio!")
        entry = ROBEntry(self.next_id, instr_type, dest, ready=False, instr=instr)
        self.buffer[self.tail] = entry
        self.tail = (self.tail + 1) % self.size
        self.count += 1
        self.next_id += 1
        return entry

    def mark_ready(self, entry_id, value):
        # Marca a entrada como pronta e armazena o valor
        for entry in self.buffer:
            if entry and entry.id == entry_id:
                entry.value = value
                entry.ready = True
                return True
        return False

    def commit(self):
        # Commita a entrada na cabeça do buffer se estiver pronta
        if self.is_empty():
            return None
        entry = self.buffer[self.head]
        if entry and entry.ready:
            self.buffer[self.head] = None
            self.head = (self.head + 1) % self.size
            self.count -= 1
            return entry
        return None

    def peek_commit(self):
        # Olha a entrada pronta para commit (sem remover)
        if self.is_empty():
            return None
        return self.buffer[self.head]

    def __repr__(self):
        return f"<ROB head={self.head} tail={self.tail} count={self.count} buffer={self.buffer}>"
