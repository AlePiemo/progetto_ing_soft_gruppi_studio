import unittest
from datetime import datetime
from model.materiale import Materiale

class TestMaterialeModel(unittest.TestCase):

    def test_creazione_materiale(self):
        data = datetime(2024, 1, 1)

        m = Materiale(
            id=1,
            titolo="Appunti lezione",
            contenuto="Contenuto del file",
            autore=10,
            nome_file="appunti.pdf",
            dimensione=2048,
            path_file="/files/appunti.pdf",
            dataCaricamento=data
        )

        self.assertEqual(m.id, 1)
        self.assertEqual(m.titolo, "Appunti lezione")
        self.assertEqual(m.contenuto, "Contenuto del file")
        self.assertEqual(m.autore, 10)
        self.assertEqual(m.nome_file, "appunti.pdf")
        self.assertEqual(m.dimensione, 2048)
        self.assertEqual(m.path_file, "/files/appunti.pdf")
        self.assertEqual(m.dataCaricamento, data)

    def test_data_caricamento_default(self):
        m = Materiale(
            id=2,
            titolo="Test",
            contenuto="desc",
            autore=20,
            nome_file="doc.txt",
            dimensione=100,
            path_file="/files/doc.txt"
        )

        self.assertIsInstance(m.dataCaricamento, datetime)

    def test_tipi_campi(self):
        m = Materiale(
            id=3,
            titolo="Titolo",
            contenuto="Testo",
            autore=5,
            nome_file="file.png",
            dimensione=500,
            path_file="/path/file.png"
        )

        self.assertIsInstance(m.id, int)
        self.assertIsInstance(m.titolo, str)
        self.assertIsInstance(m.contenuto, str)
        self.assertIsInstance(m.autore, int)
        self.assertIsInstance(m.nome_file, str)
        self.assertIsInstance(m.dimensione, int)
        self.assertIsInstance(m.path_file, str)
        self.assertIsInstance(m.dataCaricamento, datetime)

    def test_dimensione_non_negativa(self):
        m = Materiale(
            id=4,
            titolo="Titolo",
            contenuto="Contenuto",
            autore=2,
            nome_file="file.txt",
            dimensione=0,
            path_file="/test"
        )
        self.assertGreaterEqual(m.dimensione, 0)

    def test_modifica_campi(self):
        m = Materiale(
            id=5,
            titolo="A",
            contenuto="B",
            autore=1,
            nome_file="f.txt",
            dimensione=10,
            path_file="/p"
        )

        m.titolo = "Nuovo titolo"
        m.dimensione = 999

        self.assertEqual(m.titolo, "Nuovo titolo")
        self.assertEqual(m.dimensione, 999)


if __name__ == "__main__":
    unittest.main()
