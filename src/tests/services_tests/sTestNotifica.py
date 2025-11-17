import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from services.notificaService import NotificaService
from model.notifica import Notifica, TipoNotifica

class TestNotificaService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        patch_utenti = patch("services.notificaService.UtenteRepository")
        patch_notifiche = patch("services.notificaService.NotificaRepository")
        patch_salva = patch("services.notificaService.salva_datastore")
        patch_uuid = patch("services.notificaService.uuid.uuid4", return_value="notif123")
        patch_notifica_class = patch("services.notificaService.Notifica")

        self.addCleanup(patch_utenti.stop)
        self.addCleanup(patch_notifiche.stop)
        self.addCleanup(patch_salva.stop)
        self.addCleanup(patch_uuid.stop)
        self.addCleanup(patch_notifica_class.stop)

        self.mock_utenti_repo = patch_utenti.start()(self.mock_datastore)
        self.mock_notifiche_repo = patch_notifiche.start()(self.mock_datastore)
        self.mock_salva = patch_salva.start()
        self.mock_uuid = patch_uuid.start()
        self.mock_notifica_class = patch_notifica_class.start()

        self.service = NotificaService(self.mock_datastore)

    def test_invia_notifica_successo(self):
        fake_user = MagicMock()
        self.mock_utenti_repo.get_by_id.return_value = fake_user

        fake_notifica = MagicMock(id="notif123")
        self.mock_notifica_class.return_value = fake_notifica

        result = self.service.invia_notifica(
            "user1",
            TipoNotifica.SEGNALAZIONE,
            "Hai ricevuto una segnalazione"
        )

        self.assertEqual(result, fake_notifica)
        self.mock_notifiche_repo.add.assert_called_once_with(fake_notifica)
        self.mock_salva.assert_called_once()

    def test_invia_notifica_destinatario_non_esiste(self):
        self.mock_utenti_repo.get_by_id.return_value = None

        with self.assertRaises(ValueError):
            self.service.invia_notifica(
                "userX",
                TipoNotifica.SEGNALAZIONE,
                "Errore"
            )

    def test_notifiche_utente(self):
        n1 = MagicMock(destinatario="u1")
        n2 = MagicMock(destinatario="u2")
        n3 = MagicMock(destinatario="u1")

        self.mock_notifiche_repo.get_all.return_value = [n1, n2, n3]

        res = self.service.notifiche_utente("u1")
        self.assertEqual(res, [n1, n3])

    def test_notifiche_per_tipo(self):
        n1 = MagicMock(destinatario="u1", tipo=TipoNotifica.SEGNALAZIONE)
        n2 = MagicMock(destinatario="u1", tipo=TipoNotifica.SISTEMA)
        n3 = MagicMock(destinatario="u1", tipo=TipoNotifica.SEGNALAZIONE)

        self.service.notifiche_utente = MagicMock(return_value=[n1, n2, n3])

        res = self.service.notifiche_per_tipo("u1", TipoNotifica.SEGNALAZIONE)
        self.assertEqual(res, [n1, n3])

    def test_elimina_notifica_successo(self):
        fake_notifica = MagicMock()
        self.mock_notifiche_repo.get_by_id.return_value = fake_notifica

        ok = self.service.elimina_notifica("n1")

        self.assertTrue(ok)
        self.mock_notifiche_repo.remove.assert_called_once_with("n1")
        self.mock_salva.assert_called_once()

    def test_elimina_notifica_non_esiste(self):
        self.mock_notifiche_repo.get_by_id.return_value = None

        ok = self.service.elimina_notifica("n1")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
