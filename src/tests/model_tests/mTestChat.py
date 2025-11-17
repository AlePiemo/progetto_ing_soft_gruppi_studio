import unittest
from model.chat import Chat

class TestChatModel(unittest.TestCase):

    def test_creazione_chat(self):
        c = Chat(id=1)
        self.assertEqual(c.id, 1)
        self.assertEqual(c.messaggi, [])
        self.assertEqual(c.partecipanti, [])

    def test_default_indipendente(self):
        c1 = Chat(id=10)
        c2 = Chat(id=20)

        c1.messaggi.append(5)
        c1.partecipanti.append(100)

        self.assertEqual(c2.messaggi, [])
        self.assertEqual(c2.partecipanti, [])
        self.assertNotEqual(c1.messaggi, c2.messaggi)
        self.assertNotEqual(c1.partecipanti, c2.partecipanti)

    def test_aggiunta_messaggi(self):
        c = Chat(id=2)
        c.messaggi.append(10)
        c.messaggi.append(20)

        self.assertEqual(c.messaggi, [10, 20])
        self.assertIn(20, c.messaggi)

    def test_aggiunta_partecipanti(self):
        c = Chat(id=3)
        c.partecipanti.append(1)
        c.partecipanti.append(2)

        self.assertEqual(c.partecipanti, [1, 2])
        self.assertIn(2, c.partecipanti)

    def test_tipologia_valori(self):
        c = Chat(id=4)
        c.messaggi.extend([1, 2, 3])
        c.partecipanti.extend([10, 20])

        for msg in c.messaggi:
            self.assertIsInstance(msg, int)

        for p in c.partecipanti:
            self.assertIsInstance(p, int)


if __name__ == "__main__":
    unittest.main()
