import unittest
from datetime import datetime, date
from model.utente import Utente, RolePlatform

class TestUtenteModel(unittest.TestCase):

    def test_creazione_utente(self):
        u = Utente(
            id=1,
            nome="Test",
            cognome="user",
            email="test@example.com",
            password="12345"
        )

        self.assertEqual(u.id, 1)
        self.assertEqual(u.nome, "Test")
        self.assertEqual(u.cognome, "user")
        self.assertEqual(u.email, "test@example.com")
        self.assertEqual(u.password, "12345")
        self.assertFalse(u.sospeso)
        self.assertIsNone(u.fineSospensione)
        self.assertIsNone(u.ultimoAccesso)
        self.assertEqual(u.ruoloPiattaforma, RolePlatform.UTENTE)
        self.assertEqual(u.gruppi, set())
        self.assertIsInstance(u.dataRegistrazione, datetime)

    def test_enum_ruoli(self):
        self.assertIn(RolePlatform.UTENTE, RolePlatform)
        self.assertIn(RolePlatform.ADMIN_GRUPPO, RolePlatform)
        self.assertIn(RolePlatform.ADMIN_PIATTAFORMA, RolePlatform)

    def test_ultimo_accesso(self):
        u = Utente(
            id=3,
            nome="Test",
            cognome="User",
            email="test@example.com",
            password="pw"
        )

        now = datetime.now()
        u.ultimoAccesso = now

        self.assertEqual(u.ultimoAccesso, now)

    def test_aggiunta_gruppi(self):
        u = Utente(
            id=4,
            nome="A",
            cognome="B",
            email="a@b.it",
            password="pw"
        )

        u.gruppi.add("gruppo1")
        u.gruppi.add("gruppo2")

        self.assertIn("gruppo1", u.gruppi)
        self.assertIn("gruppo2", u.gruppi)

    def test_default_indipendente(self):
        u1 = Utente(id=10, nome="X", cognome="Y", email="x@y.it", password="pw")
        u2 = Utente(id=11, nome="Z", cognome="K", email="z@k.it", password="pw")

        u1.gruppi.add("g1")

        self.assertEqual(u2.gruppi, set()) 
        self.assertNotEqual(u1.gruppi, u2.gruppi)

    def test_tipi_campi(self):
        u = Utente(id=20, nome="Test", cognome="User", email="t@t.it", password="pw")

        self.assertIsInstance(u.id, int)
        self.assertIsInstance(u.nome, str)
        self.assertIsInstance(u.cognome, str)
        self.assertIsInstance(u.email, str)
        self.assertIsInstance(u.password, str)
        self.assertIsInstance(u.sospeso, bool)
        self.assertIsInstance(u.ruoloPiattaforma, RolePlatform)
        self.assertIsInstance(u.gruppi, set)
        self.assertIsInstance(u.dataRegistrazione, datetime)


if __name__ == "__main__":
    unittest.main()
