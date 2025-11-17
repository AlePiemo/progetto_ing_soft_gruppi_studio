import unittest
from datetime import datetime
from model.incontro import Incontro, IncontroStatus

class TestIncontroModel(unittest.TestCase):

    def test_creazione_incontro(self):
        data = datetime(2024, 5, 1)
        ora = datetime(2024, 5, 1, 15, 30)

        i = Incontro(
            id=1,
            titolo="Riunione",
            descrizione="Discussione progetto",
            dataIncontro=data,
            oraIncontro=ora,
            gruppo_id=10
        )

        self.assertEqual(i.id, 1)
        self.assertEqual(i.titolo, "Riunione")
        self.assertEqual(i.descrizione, "Discussione progetto")
        self.assertEqual(i.dataIncontro, data)
        self.assertEqual(i.oraIncontro, ora)
        self.assertEqual(i.gruppo_id, 10)

        # valore di default
        self.assertEqual(i.statoIncontro, IncontroStatus.PROGRAMMATO)

    def test_enum_valori(self):
        self.assertIn(IncontroStatus.PROGRAMMATO, IncontroStatus)
        self.assertIn(IncontroStatus.ANNULLATO, IncontroStatus)

    def test_modifica_stato(self):
        i = Incontro(
            id=2,
            titolo="Test",
            descrizione="desc",
            dataIncontro=datetime.now(),
            oraIncontro=datetime.now(),
            gruppo_id=20
        )

        i.statoIncontro = IncontroStatus.ANNULLATO
        self.assertEqual(i.statoIncontro, IncontroStatus.ANNULLATO)

    def test_tipi_campi(self):
        i = Incontro(
            id=3,
            titolo="ABC",
            descrizione="XYZ",
            dataIncontro=datetime.now(),
            oraIncontro=datetime.now(),
            gruppo_id=30
        )

        self.assertIsInstance(i.id, int)
        self.assertIsInstance(i.titolo, str)
        self.assertIsInstance(i.descrizione, str)
        self.assertIsInstance(i.dataIncontro, datetime)
        self.assertIsInstance(i.oraIncontro, datetime)
        self.assertIsInstance(i.gruppo_id, int)
        self.assertIsInstance(i.statoIncontro, IncontroStatus)


if __name__ == "__main__":
    unittest.main()
