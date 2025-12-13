import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

from services.gruppoService import GruppoService
from model.gruppo import Gruppo

class TestGruppoService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        # Patch repository, Gruppo class e salva
        patch_gruppi = patch("services.gruppoService.GruppoRepository")
        patch_utenti = patch("services.gruppoService.UtenteRepository")
        patch_salva = patch("services.gruppoService.salva_datastore")
        patch_gruppo_class = patch("services.gruppoService.Gruppo")

        # Patch UUID
        patch_uuid = patch("services.gruppoService.uuid.uuid4", return_value="g123")

        self.addCleanup(patch_gruppi.stop)
        self.addCleanup(patch_utenti.stop)
        self.addCleanup(patch_salva.stop)
        self.addCleanup(patch_gruppo_class.stop)
        self.addCleanup(patch_uuid.stop)

        self.mock_gruppi_repo = patch_gruppi.start()(self.mock_datastore)
        self.mock_utenti_repo = patch_utenti.start()(self.mock_datastore)
        self.mock_salva = patch_salva.start()
        self.mock_gruppo_class = patch_gruppo_class.start()
        self.mock_uuid = patch_uuid.start()

        self.service = GruppoService(self.mock_datastore)


    def test_crea_gruppo_successo(self):
        fake_group = MagicMock(listaUtenti=set(), amministratori=set())
        fake_group.id = "g123"  
        self.mock_gruppo_class.return_value = fake_group

        fake_user = MagicMock(gruppi=set())
        self.mock_utenti_repo.get_by_id.return_value = fake_user

        result = self.service.crea_gruppo("Test", "Descrizione", "u1")

        self.assertEqual(result, fake_group)
        self.mock_gruppi_repo.add.assert_called_once_with(fake_group)
        self.assertIn("u1", fake_group.listaUtenti)
        self.assertIn("u1", fake_group.amministratori)

        self.assertIn("g123", fake_user.gruppi)       

        self.mock_salva.assert_called_once()


    def test_modifica_gruppo_successo(self):
        group = MagicMock(amministratori={"u1"})
        self.mock_gruppi_repo.get_by_id.return_value = group

        ok = self.service.modifica_gruppo("g1", "u1", nomeGruppo="NuovoNome")

        self.assertTrue(ok)
        self.assertEqual(group.nomeGruppo, "NuovoNome")
        self.mock_salva.assert_called_once()

    def test_modifica_gruppo_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        ok = self.service.modifica_gruppo("g1", "u1", nomeGruppo="x")
        self.assertFalse(ok)

    def test_modifica_gruppo_non_admin(self):
        group = MagicMock(amministratori={"admin"})
        self.mock_gruppi_repo.get_by_id.return_value = group
        ok = self.service.modifica_gruppo("g1", "not_admin", nomeGruppo="x")
        self.assertFalse(ok)

    def test_elimina_gruppo_successo(self):
        group = MagicMock(amministratori={"u1"}, listaUtenti={"a", "b"})
        userA = MagicMock(gruppi={"g1"})
        userB = MagicMock(gruppi={"g1"})

        self.mock_gruppi_repo.get_by_id.return_value = group
        self.mock_utenti_repo.get_by_id.side_effect = lambda x: {"a": userA, "b": userB}.get(x)

        ok = self.service.elimina_gruppo("g1", "u1")

        self.assertTrue(ok)
        self.mock_gruppi_repo.remove.assert_called_once_with("g1")
        self.assertNotIn("g1", userA.gruppi)
        self.assertNotIn("g1", userB.gruppi)
        self.mock_salva.assert_called_once()

    def test_elimina_gruppo_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        ok = self.service.elimina_gruppo("g1", "u1")
        self.assertFalse(ok)

    def test_elimina_gruppo_non_admin(self):
        group = MagicMock(amministratori={"admin"})
        self.mock_gruppi_repo.get_by_id.return_value = group
        ok = self.service.elimina_gruppo("g1", "u2")
        self.assertFalse(ok)

    def test_aggiungi_membro_successo(self):
        group = MagicMock(amministratori={"admin"}, listaUtenti=set())
        user = MagicMock(gruppi=set())

        self.mock_gruppi_repo.get_by_id.return_value = group
        self.mock_utenti_repo.get_by_id.return_value = user

        ok = self.service.aggiungi_membro("g", "admin", "u1")

        self.assertTrue(ok)
        self.assertIn("u1", group.listaUtenti)
        self.assertIn("g", user.gruppi)
        self.mock_salva.assert_called_once()

    def test_aggiungi_membro_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        ok = self.service.aggiungi_membro("g", "admin", "u1")
        self.assertFalse(ok)

    def test_aggiungi_membro_non_admin(self):
        group = MagicMock(amministratori={"admin"})
        self.mock_gruppi_repo.get_by_id.return_value = group
        ok = self.service.aggiungi_membro("g", "u2", "u1")
        self.assertFalse(ok)

    def test_rimuovi_membro_successo(self):
        group = MagicMock(amministratori={"admin"}, listaUtenti={"u1"})
        user = MagicMock(gruppi={"g"})

        self.mock_gruppi_repo.get_by_id.return_value = group
        self.mock_utenti_repo.get_by_id.return_value = user

        ok = self.service.rimuovi_membro("g", "admin", "u1")

        self.assertTrue(ok)
        self.assertNotIn("u1", group.listaUtenti)
        self.assertNotIn("g", user.gruppi)
        self.mock_salva.assert_called_once()

    def test_rimuovi_membro_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        ok = self.service.rimuovi_membro("g", "admin", "x")
        self.assertFalse(ok)

    def test_rimuovi_membro_non_admin(self):
        group = MagicMock(amministratori={"admin"})
        self.mock_gruppi_repo.get_by_id.return_value = group
        ok = self.service.rimuovi_membro("g", "u2", "x")
        self.assertFalse(ok)

    def test_nomina_admin_successo(self):
        group = MagicMock(amministratori={"admin"}, listaUtenti={"u1"})
        self.mock_gruppi_repo.get_by_id.return_value = group

        ok = self.service.nomina_admin("g", "admin", "u1")

        self.assertTrue(ok)
        self.assertIn("u1", group.amministratori)
        self.mock_salva.assert_called_once()

    def test_nomina_admin_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        self.assertFalse(self.service.nomina_admin("g", "admin", "u1"))

    def test_nomina_admin_non_admin(self):
        group = MagicMock(amministratori={"adm"})
        self.mock_gruppi_repo.get_by_id.return_value = group
        self.assertFalse(self.service.nomina_admin("g", "u2", "u1"))

    def test_nomina_admin_non_membro(self):
        group = MagicMock(amministratori={"admin"}, listaUtenti=set())
        self.mock_gruppi_repo.get_by_id.return_value = group
        self.assertFalse(self.service.nomina_admin("g", "admin", "u1"))

    def test_revoca_admin_successo(self):
        group = MagicMock(amministratori={"admin", "u1"})
        self.mock_gruppi_repo.get_by_id.return_value = group

        ok = self.service.revoca_admin("g", "admin", "u1")

        self.assertTrue(ok)
        self.assertNotIn("u1", group.amministratori)
        self.mock_salva.assert_called_once()

    def test_revoca_admin_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        self.assertFalse(self.service.revoca_admin("g", "admin", "u1"))

    def test_revoca_admin_non_admin(self):
        group = MagicMock(amministratori={"adm"})
        self.mock_gruppi_repo.get_by_id.return_value = group
        self.assertFalse(self.service.revoca_admin("g", "u2", "u1"))

    def test_lista_gruppi(self):
        self.mock_gruppi_repo.get_all.return_value = ["a", "b"]
        result = self.service.lista_gruppi()
        self.assertEqual(result, ["a", "b"])

    def test_cerca_gruppi(self):
        g1 = MagicMock(nomeGruppo="Studio matematica")
        g2 = MagicMock(nomeGruppo="Studio algoritmi")
        g3 = MagicMock(nomeGruppo="Sport")

        self.mock_gruppi_repo.get_all.return_value = [g1, g2, g3]

        result = self.service.cerca_gruppi("studio")
        self.assertEqual(set(result), {g1, g2})


if __name__ == "__main__":
    unittest.main()
