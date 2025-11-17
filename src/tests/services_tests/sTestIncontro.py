import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from services.incontroService import IncontroService
from model.incontro import Incontro, IncontroStatus

class TestIncontroService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        patch_incontri = patch("services.incontroService.IncontroRepository")
        patch_gruppi = patch("services.incontroService.GruppoRepository")
        patch_salva = patch("services.incontroService.salva_datastore")
        patch_uuid = patch("services.incontroService.uuid.uuid4", return_value="inc123")
        patch_incontro_class = patch("services.incontroService.Incontro")

        self.addCleanup(patch_incontri.stop)
        self.addCleanup(patch_gruppi.stop)
        self.addCleanup(patch_salva.stop)
        self.addCleanup(patch_uuid.stop)
        self.addCleanup(patch_incontro_class.stop)

        self.mock_incontri_repo = patch_incontri.start()(self.mock_datastore)
        self.mock_gruppi_repo = patch_gruppi.start()(self.mock_datastore)
        self.mock_salva = patch_salva.start()
        self.mock_uuid = patch_uuid.start()
        self.mock_incontro_class = patch_incontro_class.start()

        self.service = IncontroService(self.mock_datastore)

    def test_crea_incontro_successo(self):
        gruppo = MagicMock(amministratori={"admin"}, incontri=set())
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        fake_inc = MagicMock(id="inc123")
        self.mock_incontro_class.return_value = fake_inc

        data = datetime.now()
        ora = datetime.now()

        result = self.service.crea_incontro("g1", "admin", "Titolo", "Desc", data, ora)

        self.assertEqual(result, fake_inc)
        self.mock_incontri_repo.add.assert_called_once_with(fake_inc)
        self.assertIn("inc123", gruppo.incontri)
        self.mock_salva.assert_called_once()

    def test_crea_incontro_gruppo_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        result = self.service.crea_incontro("g1", "admin", "Titolo", "Desc", datetime.now(), datetime.now())
        self.assertIsNone(result)

    def test_crea_incontro_non_admin(self):
        gruppo = MagicMock(amministratori={"other"})
        self.mock_gruppi_repo.get_by_id.return_value = gruppo
        result = self.service.crea_incontro("g1", "admin", "Titolo", "Desc", datetime.now(), datetime.now())
        self.assertIsNone(result)

    def test_modifica_incontro_successo(self):
        inc = MagicMock(gruppo_id="g1")
        gruppo = MagicMock(amministratori={"admin"})

        self.mock_incontri_repo.get_by_id.return_value = inc
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        ok = self.service.modifica_incontro("inc1", "admin", titolo="NuovoTitolo")

        self.assertTrue(ok)
        self.assertEqual(inc.titolo, "NuovoTitolo")
        self.mock_salva.assert_called_once()

    def test_modifica_incontro_non_esiste(self):
        self.mock_incontri_repo.get_by_id.return_value = None
        ok = self.service.modifica_incontro("inc1", "admin", titolo="x")
        self.assertFalse(ok)

    def test_modifica_incontro_non_admin(self):
        inc = MagicMock(gruppo_id="g1")
        gruppo = MagicMock(amministratori={"altro"})

        self.mock_incontri_repo.get_by_id.return_value = inc
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        ok = self.service.modifica_incontro("inc1", "admin", titolo="x")
        self.assertFalse(ok)

    def test_annulla_successo(self):
        inc = MagicMock(gruppo_id="g1")
        gruppo = MagicMock(amministratori={"admin"})

        self.mock_incontri_repo.get_by_id.return_value = inc
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        ok = self.service.annulla_incontro("inc1", "admin")

        self.assertTrue(ok)
        self.assertEqual(inc.statoIncontro, IncontroStatus.ANNULLATO)
        self.mock_salva.assert_called_once()

    def test_annulla_incontro_non_esiste(self):
        self.mock_incontri_repo.get_by_id.return_value = None
        ok = self.service.annulla_incontro("inc1", "admin")
        self.assertFalse(ok)

    def test_annulla_incontro_non_admin(self):
        inc = MagicMock(gruppo_id="g1")
        gruppo = MagicMock(amministratori={"altro"})

        self.mock_incontri_repo.get_by_id.return_value = inc
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        ok = self.service.annulla_incontro("inc1", "admin")
        self.assertFalse(ok)

    def test_elimina_incontro_successo(self):
        inc = MagicMock(gruppo_id="g1")
        gruppo = MagicMock(amministratori={"admin"}, incontri={"inc1"})

        self.mock_incontri_repo.get_by_id.return_value = inc
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        ok = self.service.elimina_incontro("inc1", "admin")

        self.assertTrue(ok)
        self.assertNotIn("inc1", gruppo.incontri)
        self.mock_incontri_repo.remove.assert_called_once_with("inc1")
        self.mock_salva.assert_called_once()

    def test_elimina_incontro_non_esiste(self):
        self.mock_incontri_repo.get_by_id.return_value = None
        ok = self.service.elimina_incontro("inc1", "admin")
        self.assertFalse(ok)

    def test_elimina_incontro_non_admin(self):
        inc = MagicMock(gruppo_id="g1")
        gruppo = MagicMock(amministratori={"altro"})

        self.mock_incontri_repo.get_by_id.return_value = inc
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        ok = self.service.elimina_incontro("inc1", "admin")
        self.assertFalse(ok)

    def test_incontri_di_gruppo(self):
        gruppo = MagicMock(incontri={"i1", "i2"})
        self.mock_gruppi_repo.get_by_id.return_value = gruppo

        i1 = MagicMock(id="i1", dataIncontro=datetime(2024, 5, 1),
                       oraIncontro=datetime(2024, 5, 1, 9))
        i2 = MagicMock(id="i2", dataIncontro=datetime(2024, 5, 1),
                       oraIncontro=datetime(2024, 5, 1, 8))

        self.mock_incontri_repo.get_by_id.side_effect = lambda x: {"i1": i1, "i2": i2}[x]

        res = self.service.incontri_di_gruppo("g1")
        self.assertEqual([i.id for i in res], ["i2", "i1"])

    def test_incontri_di_gruppo_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        res = self.service.incontri_di_gruppo("g1")
        self.assertEqual(res, [])


if __name__ == "__main__":
    unittest.main()
