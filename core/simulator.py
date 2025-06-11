class TomasuloSimulator:
    def __init__(self, instructions, reservation_stations, rob, registers, memory):
        self.instructions = instructions  # lista de Instruction
        self.reservation_stations = reservation_stations  # dict por tipo
        self.rob = rob
        self.registers = registers
        self.memory = memory
        self.cycle = 0
        self.finished = False

    # Executa um ciclo do simulador de Tomasulo.
    def next_cycle(self):
        if self.finished:
            return

        self.cycle += 1

        # 1. Commit (ordem inversa para evitar conflitos)
        self.commit()

        # 2. Write-back (escreve resultados no CDB)
        self.write_back()

        # 3. Execute (avança execução das instruções nas RS)
        self.execute()

        # 4. Issue (emite novas instruções para RS livres)
        self.issue()

        # 5. Atualizar estruturas auxiliares, se necessário
        self.update_structures()

        # 6. Verifica se terminou
        self.finished = self.check_finished()

    # Emite instruções para as estações de reserva livres.
    def issue(self):
        # TODO: Implementar lógica de emissão
        pass

    # Executa instruções nas estações de reserva.
    def execute(self):
        # TODO: Implementar lógica de execução
        pass

    # Faz o write-back dos resultados prontos no CDB.
    def write_back(self):
        # TODO: Implementar lógica de write-back
        pass

    # Commit das instruções prontas no ROB.
    def commit(self):
        # TODO: Implementar lógica de commit
        pass

    # Atualiza estruturas auxiliares (ex: flags, contadores, etc).
    def update_structures(self):
        # TODO: Implementar se necessário
        pass

    # Verifica se todas as instruções foram finalizadas.
    def check_finished(self):
        # TODO: Implementar condição de parada
        return False

    # Retorna o número total de ciclos simulados.
    def get_cycle_count(self):
        return self.cycle