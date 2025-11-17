import unittest
from datetime import datetime
from model.notifica import Notifica, TipoNotifica

class TestNotificaModel(unittest.TestCase):

    def test_creazione_notifica(self):
        data = datetime(2024, 1, 1)

        n = Notifica(
            id=1,
            descrizione="Nuovo materiale caricato",
            destinatario=20,
            tipo=TipoNotifica.MATERIALE,
            dataInvio=data
        )

        self.assertEqual(n.id, 1)
        self.assertEqual(n.descrizione, "Nuovo materiale caricato")
        self.assertEqual(n.destinatario, 20)
        self.assertEqual(n.tipo, TipoNotifica.MATERIALE)
        self.assertEqual(n.dataInvio, data)

    def test_enum_valori(self):
        self.assertIn(TipoNotifica.SISTEMA, TipoNotifica)
        self.assertIn(TipoNotifica.INCONTRO, TipoNotifica)
        self.assertIn(TipoNotifica.MATERIALE, TipoNotifica)
        self.assertIn(TipoNotifica.SEGNALAZIONE, TipoNotifica)
        self.assertIn(TipoNotifica.SANZIONE, TipoNotifica)

    def test_data_default(self):
        n = Notifica(
            id=2,
            descrizione="Test",
            destinatario=5,
            tipo=TipoNotifica.SISTEMA
        )
        self.assertIsInstance(n.dataInvio, datetime)

    def test_tipi_campi(self):
        n = Notifica(
            id=3,
            descrizione="ABC",
            destinatario=10,
            tipo=TipoNotifica.SANZIONE
        )

        self.assertIsInstance(n.id, int)
        self.assertIsInstance(n.descrizione, str)
        self.assertIsInstance(n.destinatario, int)
        self.assertIsInstance(n.tipo, TipoNotifica)
        self.assertIsInstance(n.dataInvio, datetime)

    def test_modifica_descrizione(self):
        n = Notifica(
            id=4,
            descrizione="Vecchio",
            destinatario=1,
            tipo=TipoNotifica.MATERIALE
        )
        n.descrizione = "Nuova descrizione"

        self.assertEqual(n.descrizione, "Nuova descrizione")

if __name__ == "__main__":
    unittest.main()
