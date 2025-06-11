import unittest
from core.simulator import TomasuloSimulator
from core.reservation_station import ReservationStation

class DummyROB:
    pass

class DummyRegisters:
    pass

class DummyMemory:
    pass

class TestTomasuloSimulator(unittest.TestCase):
    def setUp(self):
        # Cria estruturas mínimas para o simulador
        self.instructions = []
        self.reservation_stations = {
            'ADD': ReservationStation('ADD', 2),
            'MUL': ReservationStation('MUL', 1)
        }
        self.rob = DummyROB()
        self.registers = DummyRegisters()
        self.memory = DummyMemory()
        self.sim = TomasuloSimulator(
            self.instructions,
            self.reservation_stations,
            self.rob,
            self.registers,
            self.memory
        )

    def test_cycle_count_increments(self):
        initial = self.sim.get_cycle_count()
        self.sim.next_cycle()
        self.assertEqual(self.sim.get_cycle_count(), initial + 1)
        self.sim.next_cycle()
        self.assertEqual(self.sim.get_cycle_count(), initial + 2)

    def test_finished_flag(self):
        self.sim.finished = True
        count = self.sim.get_cycle_count()
        self.sim.next_cycle()
        self.assertEqual(self.sim.get_cycle_count(), count)  # Não deve incrementar

    def test_methods_called(self):
        # Testa se os métodos existem e podem ser chamados sem erro
        self.sim.issue()
        self.sim.execute()
        self.sim.write_back()
        self.sim.commit()
        self.sim.update_structures()
        self.sim.check_finished()

if __name__ == "__main__":
    unittest.main()
