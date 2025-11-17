import unittest
from datetime import datetime
from model.messaggio import Messaggio

class TestMessaggioModel(unittest.TestCase):

    def test_creazione_messaggio(self):
        data = datetime(2024, 5, 1)

        m = Messaggio(
            id=1,
            mittente=10,
            testo="Ciao",
            data=data
        )

        self.assertEqual(m.id, 1)
        self.assertEqual(m.mittente, 10)
        self.assertEqual(m.testo, "Ciao")
        self.assertEqual(m.data, data)

    def test_data_default(self):
        m = Messaggio(id=2, mittente=20, testo="Messaggio di test")
        self.assertIsInstance(m.data, datetime)

    def test_tipi_campi(self):
        m = Messaggio(id=3, mittente=30, testo="Hello")

        self.assertIsInstance(m.id, int)
        self.assertIsInstance(m.mittente, int)
        self.assertIsInstance(m.testo, str)
        self.assertIsInstance(m.data, datetime)

    def test_modifica_testo(self):
        m = Messaggio(id=4, mittente=5, testo="Vecchio")
        m.testo = "Nuovo messaggio"

        self.assertEqual(m.testo, "Nuovo messaggio")

if __name__ == "__main__":
    unittest.main()
