import unittest
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime

from services.materialeService import MaterialeService
from model.materiale import Materiale

class TestMaterialeService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        patch_mat = patch("services.materialeService.MaterialeRepository")
        patch_gruppo = patch("services.materialeService.GruppoRepository")
        patch_utente = patch("services.materialeService.UtenteRepository")

        patch_uuid = patch("services.materialeService.uuid.uuid4", return_value="mat123")
        patch_exists = patch("services.materialeService.os.path.exists")
        patch_getsize = patch("services.materialeService.os.path.getsize")
        patch_remove = patch("services.materialeService.os.remove")
        patch_makedirs = patch("services.materialeService.os.makedirs")
        patch_salva = patch("services.materialeService.salva_datastore")
        patch_materiale_class = patch("services.materialeService.Materiale")

        self.addCleanup(patch_mat.stop)
        self.addCleanup(patch_gruppo.stop)
        self.addCleanup(patch_utente.stop)
        self.addCleanup(patch_uuid.stop)
        self.addCleanup(patch_exists.stop)
        self.addCleanup(patch_getsize.stop)
        self.addCleanup(patch_remove.stop)
        self.addCleanup(patch_makedirs.stop)
        self.addCleanup(patch_salva.stop)
        self.addCleanup(patch_materiale_class.stop)

        self.mock_mat_repo = patch_mat.start()(self.mock_datastore)
        self.mock_gruppo_repo = patch_gruppo.start()(self.mock_datastore)
        self.mock_utente_repo = patch_utente.start()(self.mock_datastore)

        self.mock_uuid = patch_uuid.start()
        self.mock_exists = patch_exists.start()
        self.mock_getsize = patch_getsize.start()
        self.mock_remove = patch_remove.start()
        self.mock_makedirs = patch_makedirs.start()
        self.mock_salva = patch_salva.start()
        self.mock_materiale_class = patch_materiale_class.start()

        self.service = MaterialeService(self.mock_datastore)

    @patch("builtins.open", new_callable=mock_open, read_data=b"filedata")
    def test_carica_materiale_successo(self, mock_file):
        gruppo = MagicMock(listaUtenti={"u1"}, materiali=set())
        self.mock_gruppo_repo.get_by_id.return_value = gruppo

        self.mock_exists.return_value = True
        self.mock_getsize.return_value = 100

        fake_materiale = MagicMock(id="mat123")
        self.mock_materiale_class.return_value = fake_materiale

        result = self.service.carica_materiale(
            "g1",
            "Titolo",
            "Contenuto",
            "u1",
            "file.pdf",
            100,
            "/path/file.pdf"
        )

        self.assertEqual(result, fake_materiale)
        self.mock_mat_repo.add.assert_called_once_with(fake_materiale)
        self.assertIn("mat123", gruppo.materiali)
        self.mock_salva.assert_called_once()

    def test_carica_materiale_gruppo_non_esiste(self):
        self.mock_gruppo_repo.get_by_id.return_value = None
        self.assertIsNone(
            self.service.carica_materiale("g1", "Titolo", "Contenuto", "u1", "f", 0, "p")
        )

    def test_carica_materiale_non_membro(self):
        gruppo = MagicMock(listaUtenti=set())
        self.mock_gruppo_repo.get_by_id.return_value = gruppo
        self.assertIsNone(
            self.service.carica_materiale("g1", "Titolo", "Contenuto", "u1", "f", 0, "p")
        )

    def test_carica_materiale_file_non_esiste(self):
        gruppo = MagicMock(listaUtenti={"u1"})
        self.mock_gruppo_repo.get_by_id.return_value = gruppo

        self.mock_exists.return_value = False

        self.assertIsNone(
            self.service.carica_materiale("g1", "Titolo", "Contenuto", "u1", "f", 0, "p")
        )

    def test_lista_materiali_gruppo(self):
        gruppo = MagicMock(materiali={"a", "b"})
        self.mock_gruppo_repo.get_by_id.return_value = gruppo

        m1 = MagicMock(id="a")
        m2 = MagicMock(id="b")

        self.mock_mat_repo.get_by_id.side_effect = lambda x: {"a": m1, "b": m2}[x]

        res = self.service.lista_materiali_gruppo("g1")
        self.assertEqual(set(res), {m1, m2})

    def test_lista_materiali_gruppo_non_esiste(self):
        self.mock_gruppo_repo.get_by_id.return_value = None
        self.assertEqual(self.service.lista_materiali_gruppo("g1"), [])

    def test_dettaglio_materiale(self):
        fake_mat = MagicMock()
        self.mock_mat_repo.get_by_id.return_value = fake_mat

        res = self.service.dettaglio_materiale("mat1")
        self.assertEqual(res, fake_mat)

    @patch("builtins.open", new_callable=mock_open, read_data=b"abc")
    def test_scarica_materiale_successo(self, mock_file):
        m = MagicMock(path_file="/path/file.pdf")
        self.mock_mat_repo.get_by_id.return_value = m
        self.mock_exists.return_value = True

        ok = self.service.scarica_materiale("mat1", "/dest/file.pdf")
        self.assertTrue(ok)

    def test_scarica_materiale_non_esiste(self):
        self.mock_mat_repo.get_by_id.return_value = None
        ok = self.service.scarica_materiale("mat1", "/dest/file.pdf")
        self.assertFalse(ok)

    def test_elimina_materiale_successo(self):
        gruppo = MagicMock(amministratori={"admin"}, materiali={"mat1"})
        self.mock_gruppo_repo.get_by_id.return_value = gruppo

        m = MagicMock(path_file="/path/file.pdf")
        self.mock_mat_repo.get_by_id.return_value = m

        self.mock_exists.return_value = True

        ok = self.service.elimina_materiale("mat1", "g1", "admin")

        self.assertTrue(ok)
        self.mock_remove.assert_called_once_with("/path/file.pdf")
        self.mock_mat_repo.remove.assert_called_once_with("mat1")
        self.assertNotIn("mat1", gruppo.materiali)
        self.mock_salva.assert_called_once()

    def test_elimina_materiale_non_admin(self):
        gruppo = MagicMock(amministratori=set())
        self.mock_gruppo_repo.get_by_id.return_value = gruppo
        ok = self.service.elimina_materiale("m", "g1", "admin")
        self.assertFalse(ok)

    def test_elimina_materiale_gruppo_non_esiste(self):
        self.mock_gruppo_repo.get_by_id.return_value = None
        ok = self.service.elimina_materiale("mat1", "g1", "admin")
        self.assertFalse(ok)

    def test_elimina_materiale_non_esiste(self):
        gruppo = MagicMock(amministratori={"admin"})
        self.mock_gruppo_repo.get_by_id.return_value = gruppo

        self.mock_mat_repo.get_by_id.return_value = None

        ok = self.service.elimina_materiale("mat1", "g1", "admin")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
