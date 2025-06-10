import unittest
from core.reservation_station import ReservationStation, ReservationStationEntry

class TestReservationStation(unittest.TestCase):
    def test_create_and_free(self):
        rs = ReservationStation('Add', 3)
        self.assertEqual(len(rs.entries), 3)
        self.assertTrue(rs.has_free())
        free_entry = rs.get_free()
        self.assertIsInstance(free_entry, ReservationStationEntry)
        self.assertFalse(free_entry.busy)

    def test_occupy_and_clear(self):
        rs = ReservationStation('Mul', 2)
        entry = rs.get_free()
        entry.busy = True
        entry.op = 'MUL'
        entry.Vj = 10
        entry.Vk = 20
        self.assertFalse(rs.has_free()) if all(e.busy for e in rs.entries) else self.assertTrue(rs.has_free())
        entry.clear()
        self.assertFalse(entry.busy)
        self.assertIsNone(entry.op)
        self.assertIsNone(entry.Vj)
        self.assertIsNone(entry.Vk)

    def test_repr(self):
        rs = ReservationStation('Load', 1)
        s = repr(rs)
        self.assertIn('ReservationStation', s)
        self.assertIn('Load', s)

if __name__ == "__main__":
    unittest.main()
