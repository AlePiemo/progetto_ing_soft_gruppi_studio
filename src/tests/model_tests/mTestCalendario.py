import unittest
from model.calendario import Calendario

class TestCalendarioModel(unittest.TestCase):

    def test_creazione_calendario(self):
        c = Calendario(id=1)
        self.assertEqual(c.id, 1)
        self.assertEqual(c.incontri, [])
        self.assertEqual(c.promemoria, [])

    def test_default_indipendente(self):
        c1 = Calendario(id=1)
        c2 = Calendario(id=2)

        c1.incontri.append(10)

        # c2 NON deve ereditare gli incontri di c1
        self.assertEqual(c2.incontri, [])
        self.assertNotEqual(c1.incontri, c2.incontri)

    def test_aggiunta_incontri(self):
        c = Calendario(id=3)
        c.incontri.append(5)
        c.incontri.append(7)

        self.assertEqual(c.incontri, [5, 7])
        self.assertIn(5, c.incontri)

    def test_aggiunta_promemoria(self):
        c = Calendario(id=4)
        c.promemoria.append(100)

        self.assertEqual(c.promemoria, [100])
        self.assertIn(100, c.promemoria)

    def test_tipi_campi(self):
        c = Calendario(id=5)
        self.assertIsInstance(c.incontri, list)
        self.assertIsInstance(c.promemoria, list)

        # Aggiungo un valore e verifico il tipo
        c.incontri.append(123)
        for x in c.incontri:
            self.assertIsInstance(x, int)


if __name__ == "__main__":
    unittest.main()
