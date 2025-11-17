import unittest
from datetime import datetime
from model.cartella import Cartella

class TestCartellaModel(unittest.TestCase):

    def test_creazione_cartella(self):
        data = datetime.now()
        c = Cartella(id=1, nome="Documenti", dataCreazione=data)

        self.assertEqual(c.id, 1)
        self.assertEqual(c.nome, "Documenti")
        self.assertEqual(c.dataCreazione, data)
        self.assertEqual(c.materiale_ids, [])

    def test_default_indipendente(self):
        c1 = Cartella(id=1, nome="A", dataCreazione=datetime.now())
        c2 = Cartella(id=2, nome="B", dataCreazione=datetime.now())

        c1.materiale_ids.append(10)

        self.assertEqual(c2.materiale_ids, [])
        self.assertNotEqual(c1.materiale_ids, c2.materiale_ids)

    def test_aggiunta_materiali(self):
        c = Cartella(id=3, nome="Test", dataCreazione=datetime.now())
        c.materiale_ids.append(5)
        c.materiale_ids.append(12)

        self.assertEqual(c.materiale_ids, [5, 12])
        self.assertIn(12, c.materiale_ids)

    def test_tipi_campi(self):
        c = Cartella(id=4, nome="Note", dataCreazione=datetime(2024, 1, 1))

        self.assertIsInstance(c.id, int)
        self.assertIsInstance(c.nome, str)
        self.assertIsInstance(c.dataCreazione, datetime)
        self.assertIsInstance(c.materiale_ids, list)

    def test_tipo_valori_materiale_ids(self):
        c = Cartella(id=5, nome="Immagini", dataCreazione=datetime.now())
        c.materiale_ids.extend([1, 2, 3])

        for elemento in c.materiale_ids:
            self.assertIsInstance(elemento, int)


if __name__ == "__main__":
    unittest.main()
