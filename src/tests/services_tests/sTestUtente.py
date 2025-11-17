import unittest
from unittest.mock import MagicMock, patch
from services.utenteService import UtenteService
from model.utente import Utente, RolePlatform

class TestUtenteService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        patch_repo = patch("services.utenteService.UtenteRepository")
        patch_salva = patch("services.utenteService.salva_datastore")
        patch_user_class = patch("services.utenteService.Utente")

        self.addCleanup(patch_repo.stop)
        self.addCleanup(patch_salva.stop)
        self.addCleanup(patch_user_class.stop)

        self.mock_repo = patch_repo.start()(self.mock_datastore)
        self.mock_salva = patch_salva.start()
        self.mock_user_class = patch_user_class.start()

        self.service = UtenteService(self.mock_datastore)

    def test_registra_utente_successo(self):
        self.mock_repo.find_by_email.return_value = None

        fake_user = MagicMock()
        self.mock_user_class.return_value = fake_user

        ok = self.service.registra_utente(1, "A", "B", "a@mail", "pass")

        self.assertTrue(ok)
        self.mock_repo.add.assert_called_once_with(fake_user)
        self.mock_salva.assert_called_once()

    def test_registra_utente_email_esistente(self):
        self.mock_repo.find_by_email.return_value = MagicMock()
        ok = self.service.registra_utente(1, "A", "B", "a@mail", "pass")
        self.assertFalse(ok)

    def test_login_successo(self):
        user = MagicMock(password="123")
        self.mock_repo.find_by_email.return_value = user

        res = self.service.login("mail", "123")

        self.assertEqual(res, user)
        self.assertEqual(self.service.get_utente_loggato(), user)

    def test_login_email_non_esiste(self):
        self.mock_repo.find_by_email.return_value = None
        res = self.service.login("mail", "123")
        self.assertIsNone(res)

    def test_login_password_errata(self):
        user = MagicMock(password="pwd")
        self.mock_repo.find_by_email.return_value = user

        res = self.service.login("mail", "errata")
        self.assertIsNone(res)

    def test_logout(self):
        user = MagicMock()
        self.service._utente_loggato = user
        self.service.logout()
        self.assertIsNone(self.service.get_utente_loggato())

    def test_admin_crea_utente_successo(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        self.mock_repo.find_by_email.return_value = None

        fake_user = MagicMock()
        self.mock_user_class.return_value = fake_user

        ok = self.service.admin_crea_utente(admin, 2, "A", "B", "mail", "pwd")

        self.assertTrue(ok)
        self.mock_repo.add.assert_called_once_with(fake_user)
        self.mock_salva.assert_called_once()

    def test_admin_crea_utente_non_admin(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.UTENTE)
        ok = self.service.admin_crea_utente(admin, 2, "A", "B", "mail", "pwd")
        self.assertFalse(ok)

    def test_admin_crea_utente_email_esistente(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        self.mock_repo.find_by_email.return_value = MagicMock()
        ok = self.service.admin_crea_utente(admin, 2, "A", "B", "mail", "pwd")
        self.assertFalse(ok)

    def test_admin_modifica_utente_successo(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        user = MagicMock()
        self.mock_repo.get_by_id.return_value = user

        ok = self.service.admin_modifica_utente(admin, 10, nome="NuovoNome")

        self.assertTrue(ok)
        self.assertEqual(user.nome, "NuovoNome")
        self.mock_salva.assert_called_once()

    def test_admin_modifica_utente_non_admin(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.UTENTE)
        ok = self.service.admin_modifica_utente(admin, 10, nome="x")
        self.assertFalse(ok)

    def test_admin_modifica_utente_non_esiste(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        self.mock_repo.get_by_id.return_value = None

        ok = self.service.admin_modifica_utente(admin, 10, nome="x")
        self.assertFalse(ok)

    def test_admin_elimina_utente_successo(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        self.mock_repo.get_by_id.return_value = MagicMock()

        ok = self.service.admin_elimina_utente(admin, 10)
        self.assertTrue(ok)
        self.mock_repo.remove.assert_called_once_with(10)
        self.mock_salva.assert_called_once()

    def test_admin_elimina_utente_non_admin(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.UTENTE)
        ok = self.service.admin_elimina_utente(admin, 10)
        self.assertFalse(ok)

    def test_admin_elimina_utente_non_esiste(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        self.mock_repo.get_by_id.return_value = None

        ok = self.service.admin_elimina_utente(admin, 10)
        self.assertFalse(ok)

    def test_cerca_utenti(self):
        u1 = MagicMock(nome="Utente", cognome="uno", email="ut1@mail")
        u2 = MagicMock(nome="Utente", cognome="due", email="ut2@mail")
        u3 = MagicMock(nome="Utente", cognome="tre", email="ut3@mail")

        self.mock_repo.get_all.return_value = [u1, u2, u3]

        res = self.service.cerca_utenti(nome="ut")

        self.assertEqual(set(res), {u1, u2, u3})


if __name__ == "__main__":
    unittest.main()
