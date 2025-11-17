import unittest
from datetime import datetime
from model.segnalazione import Segnalazione, StatoSegnalazione

class TestSegnalazioneModel(unittest.TestCase):

    def test_creazione_segnalazione(self):
        data = datetime(2024, 6, 1)

        s = Segnalazione(
            id=1,
            motivo="Contenuto inappropriato",
            autore=10,
            destinatario=20,
            stato=StatoSegnalazione.Inviata,
            data=data
        )

        self.assertEqual(s.id, 1)
        self.assertEqual(s.motivo, "Contenuto inappropriato")
        self.assertEqual(s.autore, 10)
        self.assertEqual(s.destinatario, 20)
        self.assertEqual(s.stato, StatoSegnalazione.Inviata)
        self.assertEqual(s.data, data)
        self.assertIsNone(s.sanzione_tipo)
        self.assertIsNone(s.sanzione_note)

    def test_enum_valori(self):
        self.assertIn(StatoSegnalazione.Inviata, StatoSegnalazione)
        self.assertIn(StatoSegnalazione.Valutata, StatoSegnalazione)
        self.assertIn(StatoSegnalazione.Archiviata, StatoSegnalazione)

    def test_data_default(self):
        s = Segnalazione(
            id=2,
            motivo="Spam",
            autore=5,
            destinatario=10,
            stato=StatoSegnalazione.Inviata
        )
        self.assertIsInstance(s.data, datetime)

    def test_modifica_stato(self):
        s = Segnalazione(
            id=3,
            motivo="Insulti",
            autore=1,
            destinatario=2,
            stato=StatoSegnalazione.Inviata
        )

        s.stato = StatoSegnalazione.Valutata
        self.assertEqual(s.stato, StatoSegnalazione.Valutata)

    def test_tipi_campi(self):
        s = Segnalazione(
            id=5,
            motivo="Test",
            autore=9,
            destinatario=8,
            stato=StatoSegnalazione.Archiviata
        )

        self.assertIsInstance(s.id, int)
        self.assertIsInstance(s.motivo, str)
        self.assertIsInstance(s.autore, int)
        self.assertIsInstance(s.destinatario, int)
        self.assertIsInstance(s.stato, StatoSegnalazione)
        self.assertIsInstance(s.data, datetime)


if __name__ == "__main__":
    unittest.main()
