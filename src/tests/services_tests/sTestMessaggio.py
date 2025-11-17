import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from services.messaggioService import ServizioMessaggio
from model.messaggio import Messaggio

class TestServizioMessaggio(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        patch_msg_repo = patch("services.messaggioService.MessaggioRepository")
        patch_user_repo = patch("services.messaggioService.UtenteRepository")
        patch_group_repo = patch("services.messaggioService.GruppoRepository")
        patch_salva = patch("services.messaggioService.salva_datastore")
        patch_uuid = patch("services.messaggioService.uuid.uuid4", return_value="msg123")

        patch_msg_class = patch("services.messaggioService.Messaggio")

        self.addCleanup(patch_msg_repo.stop)
        self.addCleanup(patch_user_repo.stop)
        self.addCleanup(patch_group_repo.stop)
        self.addCleanup(patch_salva.stop)
        self.addCleanup(patch_uuid.stop)
        self.addCleanup(patch_msg_class.stop)

        self.mock_msg_repo = patch_msg_repo.start()(self.mock_datastore)
        self.mock_user_repo = patch_user_repo.start()(self.mock_datastore)
        self.mock_group_repo = patch_group_repo.start()(self.mock_datastore)
        self.mock_salva = patch_salva.start()
        self.mock_uuid = patch_uuid.start()
        self.mock_msg_class = patch_msg_class.start()

        self.service = ServizioMessaggio(self.mock_datastore)

    def test_invia_messaggio_gruppo_successo(self):
        gruppo = MagicMock(membri={10}, messaggi=set())
        self.mock_group_repo.get_by_id.return_value = gruppo

        fake_msg = MagicMock(id="msg123")
        self.mock_msg_class.return_value = fake_msg

        result = self.service.invia_messaggio_gruppo(1, 10, "ciao")

        self.assertTrue(result)
        self.mock_msg_repo.add.assert_called_once_with(fake_msg)
        self.assertIn("msg123", gruppo.messaggi)
        self.mock_salva.assert_called_once()

    def test_invia_messaggio_gruppo_gruppo_non_esiste(self):
        self.mock_group_repo.get_by_id.return_value = None
        result = self.service.invia_messaggio_gruppo(1, 10, "ciao")
        self.assertFalse(result)

    def test_invia_messaggio_gruppo_non_membro(self):
        gruppo = MagicMock(membri=set())
        self.mock_group_repo.get_by_id.return_value = gruppo
        result = self.service.invia_messaggio_gruppo(1, 10, "ciao")
        self.assertFalse(result)

    def test_chat_gruppo_ordinata(self):
        gruppo = MagicMock(messaggi={"1", "2"})
        self.mock_group_repo.get_by_id.return_value = gruppo

        m1 = MagicMock(id=1, data=datetime.now() + timedelta(seconds=10))
        m2 = MagicMock(id=2, data=datetime.now())

        self.mock_msg_repo.get_by_id.side_effect = lambda x: {"1": m1, "2": m2}[x]

        res = self.service.chat_gruppo(1)

        self.assertEqual([m.id for m in res], [2, 1])

    def test_chat_gruppo_non_esiste(self):
        self.mock_group_repo.get_by_id.return_value = None
        res = self.service.chat_gruppo(1)
        self.assertEqual(res, [])

    def test_messaggi_di_utente(self):
        f1 = MagicMock()
        f2 = MagicMock()

        self.mock_msg_repo.get_by_user.return_value = [f1, f2]

        res = self.service.messaggi_di_utente(10)

        self.assertEqual(res, [f1, f2])
        self.mock_msg_repo.get_by_user.assert_called_once_with(10)


if __name__ == "__main__":
    unittest.main()
