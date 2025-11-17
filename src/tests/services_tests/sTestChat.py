import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from services.chatService import ChatService

class TestChatService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        patch_gruppi = patch("services.chatService.GruppoRepository")
        patch_utenti = patch("services.chatService.UtenteRepository")
        patch_messaggi = patch("services.chatService.MessaggioRepository")
        patch_salva = patch("services.chatService.salva_datastore")
        patch_messaggio_class = patch("services.chatService.Messaggio")

        self.addCleanup(patch_gruppi.stop)
        self.addCleanup(patch_utenti.stop)
        self.addCleanup(patch_messaggi.stop)
        self.addCleanup(patch_salva.stop)
        self.addCleanup(patch_messaggio_class.stop)

        self.mock_gruppi_repo = patch_gruppi.start()(self.mock_datastore)
        self.mock_utenti_repo = patch_utenti.start()(self.mock_datastore)
        self.mock_messaggi_repo = patch_messaggi.start()(self.mock_datastore)
        self.mock_salva = patch_salva.start()
        self.mock_message_class = patch_messaggio_class.start()

        self.service = ChatService(self.mock_datastore)

    def test_invia_gruppo_successo(self):
        gruppo = MagicMock()
        gruppo.membri = {10}
        gruppo.messaggi = set()
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        fake_msg = MagicMock(id=123)
        self.mock_message_class.return_value = fake_msg

        result = self.service.invia_gruppo(1, 10, "ciao")

        self.assertTrue(result)
        self.mock_messaggi_repo.add.assert_called_once_with(fake_msg)
        self.assertEqual(len(gruppo.messaggi), 1)
        self.mock_salva.assert_called_once()

    def test_invia_gruppo_gruppo_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        self.assertFalse(self.service.invia_gruppo(1, 10, "ciao"))

    def test_invia_gruppo_non_membro(self):
        gruppo = MagicMock()
        gruppo.membri = {99}
        self.mock_gruppi_repo.get_by_id.return_value = gruppo
        self.assertFalse(self.service.invia_gruppo(1, 10, "ciao"))

    def test_chat_gruppo(self):
        gruppo = MagicMock()
        gruppo.messaggi = {"1", "2"}
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        m1 = MagicMock(id=1, timestamp=datetime.now() + timedelta(seconds=10))
        m2 = MagicMock(id=2, timestamp=datetime.now())

        self.mock_messaggi_repo.get_by_id.side_effect = lambda x: {"1": m1, "2": m2}[x]

        result = self.service.chat_gruppo(1)
        self.assertEqual([m.id for m in result], [2, 1])

    def test_non_letti(self):
        utente = MagicMock()
        utente.gruppi = {"g1"}
        self.mock_utenti_repo.get_by_id.return_value = utente

        gruppo = MagicMock()
        gruppo.messaggi = {1, 2, 3}
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        m1 = MagicMock(id=1, mittente_id=20, timestamp=datetime.now(), letto=False)
        m2 = MagicMock(id=2, mittente_id=10, timestamp=datetime.now(), letto=False)
        m3 = MagicMock(id=3, mittente_id=30, timestamp=datetime.now(), letto=True)

        self.mock_messaggi_repo.get_by_id.side_effect = lambda x: {1: m1, 2: m2, 3: m3}[x]

        result = self.service.non_letti(10)

        self.assertEqual([m.id for m in result], [1])

    def test_segna_letto(self):
        m = MagicMock(letto=False)
        self.mock_messaggi_repo.get_by_id.return_value = m

        self.assertTrue(self.service.segna_letto(1))
        self.assertTrue(m.letto)
        self.mock_salva.assert_called_once()

    def test_segna_letto_fail(self):
        self.mock_messaggi_repo.get_by_id.return_value = None
        self.assertFalse(self.service.segna_letto(1))

    def test_ultimo_messaggio(self):
        m1 = MagicMock(id=1)
        m2 = MagicMock(id=2)

        self.service.chat_gruppo = MagicMock(return_value=[m1, m2])
        self.assertEqual(self.service.ultimo_messaggio_gruppo(1), m2)

    def test_ultimo_messaggio_none(self):
        self.service.chat_gruppo = MagicMock(return_value=[])
        self.assertIsNone(self.service.ultimo_messaggio_gruppo(1))


if __name__ == "__main__":
    unittest.main()
