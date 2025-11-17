import unittest
from datetime import datetime
from model.promemoria import Promemoria

class TestPromemoriaModel(unittest.TestCase):

    def test_creazione_promemoria(self):
        data = datetime(2024, 5, 1)

        p = Promemoria(
            id=1,
            testo="Ricordati dell'incontro",
            data=data
        )

        self.assertEqual(p.id, 1)
        self.assertEqual(p.testo, "Ricordati dell'incontro")
        self.assertEqual(p.data, data)

    def test_data_default(self):
        p = Promemoria(id=2, testo="Test")
        self.assertIsInstance(p.data, datetime)

    def test_tipi_campi(self):
        p = Promemoria(id=3, testo="Promemoria")

        self.assertIsInstance(p.id, int)
        self.assertIsInstance(p.testo, str)
        self.assertIsInstance(p.data, datetime)

    def test_modifica_testo(self):
        p = Promemoria(id=4, testo="Vecchio testo")
        p.testo = "Nuovo testo"

        self.assertEqual(p.testo, "Nuovo testo")

if __name__ == "__main__":
    unittest.main()
