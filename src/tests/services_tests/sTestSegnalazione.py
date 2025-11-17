import unittest
from unittest.mock import MagicMock, patch
from model.segnalazione import Segnalazione, StatoSegnalazione
from model.utente import Utente, RolePlatform
from services.segnalazioneService import SegnalazioneService

class TestSegnalazioneService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        patch_utenti = patch("services.segnalazioneService.UtenteRepository")
        patch_gruppi = patch("services.segnalazioneService.GruppoRepository")
        patch_segn = patch("services.segnalazioneService.SegnalazioneRepository")
        patch_msg = patch("services.segnalazioneService.MessaggioRepository")

        patch_uuid = patch("services.segnalazioneService.uuid.uuid4", return_value="seg123")
        patch_salva = patch("services.segnalazioneService.salva_datastore")
        patch_seg_class = patch("services.segnalazioneService.Segnalazione")

        self.addCleanup(patch_utenti.stop)
        self.addCleanup(patch_gruppi.stop)
        self.addCleanup(patch_segn.stop)
        self.addCleanup(patch_msg.stop)
        self.addCleanup(patch_uuid.stop)
        self.addCleanup(patch_salva.stop)
        self.addCleanup(patch_seg_class.stop)

        self.mock_utenti_repo = patch_utenti.start()(self.mock_datastore)
        self.mock_gruppi_repo = patch_gruppi.start()(self.mock_datastore)
        self.mock_segn_repo = patch_segn.start()(self.mock_datastore)
        self.mock_msg_repo = patch_msg.start()(self.mock_datastore)
        self.mock_uuid = patch_uuid.start()
        self.mock_salva = patch_salva.start()
        self.mock_seg_class = patch_seg_class.start()

        self.service = SegnalazioneService(self.mock_datastore)

    def test_segnala_utente_successo(self):
        self.mock_utenti_repo.get_by_id.return_value = MagicMock()

        fake_seg = MagicMock(id="seg123")
        self.mock_seg_class.return_value = fake_seg

        res = self.service.segnala_utente("a", "b", "spam")

        self.assertEqual(res, fake_seg)
        self.mock_segn_repo.add.assert_called_once_with(fake_seg)
        self.mock_salva.assert_called_once()

    def test_segnala_utente_autore_non_esiste(self):
        self.mock_utenti_repo.get_by_id.side_effect = [None]
        res = self.service.segnala_utente("a", "b", "spam")
        self.assertIsNone(res)

    def test_segnala_utente_dest_non_esiste(self):
        self.mock_utenti_repo.get_by_id.side_effect = [
            MagicMock(),  
            None,         
        ]
        res = self.service.segnala_utente("a", "b", "spam")
        self.assertIsNone(res)

    def test_segnala_messaggio_successo(self):
        self.mock_utenti_repo.get_by_id.return_value = MagicMock()
        self.mock_msg_repo.get_by_id.return_value = MagicMock()

        fake_seg = MagicMock(id="seg123")
        self.mock_seg_class.return_value = fake_seg

        res = self.service.segnala_messaggio("a", "msg1", "spam")
        self.assertEqual(res, fake_seg)
        self.mock_segn_repo.add.assert_called_once_with(fake_seg)
        self.mock_salva.assert_called_once()

    def test_segnala_messaggio_autore_non_esiste(self):
        self.mock_utenti_repo.get_by_id.return_value = None
        res = self.service.segnala_messaggio("a", "msg1", "spam")
        self.assertIsNone(res)

    def test_segnala_messaggio_msg_non_esiste(self):
        self.mock_utenti_repo.get_by_id.return_value = MagicMock()
        self.mock_msg_repo.get_by_id.return_value = None
        res = self.service.segnala_messaggio("a", "msg1", "spam")
        self.assertIsNone(res)

    def test_cambia_stato_successo(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        seg = MagicMock()
        self.mock_segn_repo.get_by_id.return_value = seg

        ok = self.service.cambia_stato(admin, "seg1", StatoSegnalazione.Valutata)

        self.assertTrue(ok)
        self.assertEqual(seg.stato, StatoSegnalazione.Valutata)
        self.mock_salva.assert_called_once()

    def test_cambia_stato_non_admin(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.UTENTE)
        ok = self.service.cambia_stato(admin, "seg1", StatoSegnalazione.Valutata)
        self.assertFalse(ok)

    def test_cambia_stato_non_esiste(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        self.mock_segn_repo.get_by_id.return_value = None

        ok = self.service.cambia_stato(admin, "seg1", StatoSegnalazione.Valutata)
        self.assertFalse(ok)

    def test_applica_sanzione_successo(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        seg = MagicMock()
        self.mock_segn_repo.get_by_id.return_value = seg

        ok = self.service.applica_sanzione(admin, "seg1", "BAN", "Violazione")

        self.assertTrue(ok)
        self.assertEqual(seg.sanzione_tipo, "BAN")
        self.assertEqual(seg.sanzione_note, "Violazione")
        self.assertEqual(seg.stato, StatoSegnalazione.Archiviata)
        self.mock_salva.assert_called_once()

    def test_applica_sanzione_non_admin(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.UTENTE)
        ok = self.service.applica_sanzione(admin, "seg1", "BAN", "Motivo")
        self.assertFalse(ok)

    def test_applica_sanzione_non_esiste(self):
        admin = MagicMock(ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA)
        self.mock_segn_repo.get_by_id.return_value = None
        ok = self.service.applica_sanzione(admin, "seg1", "BAN", "Motivo")
        self.assertFalse(ok)

    def test_segnalazioni_in_attesa(self):
        s1 = MagicMock(stato=StatoSegnalazione.Inviata)
        s2 = MagicMock(stato=StatoSegnalazione.Valutata)
        self.mock_segn_repo.get_all.return_value = [s1, s2]

        res = self.service.segnalazioni_in_attesa()
        self.assertEqual(res, [s1])

    def test_segnalazioni_valutate(self):
        s1 = MagicMock(stato=StatoSegnalazione.Valutata)
        s2 = MagicMock(stato=StatoSegnalazione.Archiviata)
        self.mock_segn_repo.get_all.return_value = [s1, s2]

        res = self.service.segnalazioni_valutate()
        self.assertEqual(res, [s1])

    def test_segnalazioni_archiviate(self):
        s1 = MagicMock(stato=StatoSegnalazione.Archiviata)
        s2 = MagicMock(stato=StatoSegnalazione.Inviata)
        self.mock_segn_repo.get_all.return_value = [s1, s2]

        res = self.service.segnalazioni_archiviate()
        self.assertEqual(res, [s1])


if __name__ == "__main__":
    unittest.main()
