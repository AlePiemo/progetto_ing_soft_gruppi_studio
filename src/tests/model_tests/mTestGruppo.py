import unittest
from datetime import datetime
from model.gruppo import Gruppo

class TestGruppoModel(unittest.TestCase):

    def test_creazione_gruppo(self):
        g = Gruppo(id=1, nomeGruppo="Studio", descrizione="Gruppo studio")

        self.assertEqual(g.id, 1)
        self.assertEqual(g.nomeGruppo, "Studio")
        self.assertEqual(g.descrizione, "Gruppo studio")

        # set vuoti all'inizio
        self.assertEqual(g.listaUtenti, set())
        self.assertEqual(g.amministratori, set())
        self.assertEqual(g.materiali, set())
        self.assertEqual(g.incontri, set())
        self.assertEqual(g.messaggi, set())

        # data creazione automaticamente settata
        self.assertIsInstance(g.dataCreazione, datetime)

    def test_default_indipendente(self):
        g1 = Gruppo(id=1, nomeGruppo="A", descrizione="desc")
        g2 = Gruppo(id=2, nomeGruppo="B", descrizione="desc")

        g1.listaUtenti.add("u1")
        g1.amministratori.add("admin1")
        g1.materiali.add("m1")
        g1.incontri.add("i1")
        g1.messaggi.add("msg1")

        self.assertEqual(g2.listaUtenti, set())
        self.assertEqual(g2.amministratori, set())
        self.assertEqual(g2.materiali, set())
        self.assertEqual(g2.incontri, set())
        self.assertEqual(g2.messaggi, set())

    def test_aggiunta_utenti(self):
        g = Gruppo(id=10, nomeGruppo="Test", descrizione="desc")
        g.listaUtenti.add("user1")
        g.listaUtenti.add("user2")

        self.assertEqual(g.listaUtenti, {"user1", "user2"})
        self.assertIn("user2", g.listaUtenti)

    def test_aggiunta_amministratori(self):
        g = Gruppo(id=11, nomeGruppo="Test", descrizione="desc")
        g.amministratori.add("admin1")

        self.assertIn("admin1", g.amministratori)

    def test_aggiunta_materiali(self):
        g = Gruppo(id=12, nomeGruppo="Test", descrizione="desc")
        g.materiali.add("mat1")

        self.assertIn("mat1", g.materiali)

    def test_tipo_campi(self):
        g = Gruppo(id=20, nomeGruppo="ABC", descrizione="desc")

        self.assertIsInstance(g.listaUtenti, set)
        self.assertIsInstance(g.amministratori, set)
        self.assertIsInstance(g.materiali, set)
        self.assertIsInstance(g.incontri, set)
        self.assertIsInstance(g.messaggi, set)

    def test_tipo_valori(self):
        g = Gruppo(id=30, nomeGruppo="Test", descrizione="desc")

        g.listaUtenti.update(["u1", "u2"])
        g.materiali.update(["m1"])
        g.incontri.update(["i1"])
        g.messaggi.update(["msg1"])

        for val in g.listaUtenti:
            self.assertIsInstance(val, str)

        for val in g.materiali:
            self.assertIsInstance(val, str)

        for val in g.incontri:
            self.assertIsInstance(val, str)

        for val in g.messaggi:
            self.assertIsInstance(val, str)


if __name__ == "__main__":
    unittest.main()
