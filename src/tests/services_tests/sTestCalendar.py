import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, date

from services.calendarioService import CalendarioService
from model.incontro import Incontro, IncontroStatus


class TestCalendarioService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()

        patch_utenti = patch("services.calendarioService.UtenteRepository")
        patch_gruppi = patch("services.calendarioService.GruppoRepository")
        patch_incontri = patch("services.calendarioService.IncontroRepository")
        patch_calendari = patch("services.calendarioService.CalendarioRepository")

        self.addCleanup(patch_utenti.stop)
        self.addCleanup(patch_gruppi.stop)
        self.addCleanup(patch_incontri.stop)
        self.addCleanup(patch_calendari.stop)

        self.mock_utenti_repo = patch_utenti.start()(self.mock_datastore)
        self.mock_gruppi_repo = patch_gruppi.start()(self.mock_datastore)
        self.mock_incontri_repo = patch_incontri.start()(self.mock_datastore)
        self.mock_calendari_repo = patch_calendari.start()(self.mock_datastore)

        self.service = CalendarioService(self.mock_datastore)

    def test_calendario_gruppo_gruppo_non_esiste(self):
        self.mock_gruppi_repo.get_by_id.return_value = None
        result = self.service.calendario_gruppo("g1")
        self.assertEqual(result, [])

    def test_calendario_gruppo_ordinamento(self):
        i1 = Incontro(1, "A", "desc",
                      datetime(2024, 5, 10), datetime(2024, 5, 10, 15, 0), "g1")
        i2 = Incontro(2, "B", "desc",
                      datetime(2024, 4, 1), datetime(2024, 4, 1, 10, 0), "g1")
        i3 = Incontro(3, "C", "desc",
                      datetime(2024, 4, 1), datetime(2024, 4, 1, 9, 0), "g1")

        gruppo_fake = MagicMock()
        gruppo_fake.incontri = ["1", "2", "3"]

        self.mock_gruppi_repo.get_by_id.return_value = gruppo_fake
        self.mock_incontri_repo.get_by_id.side_effect = lambda x: {
            "1": i1, "2": i2, "3": i3
        }.get(x)

        result = self.service.calendario_gruppo("g1")

        self.assertEqual([i.id for i in result], [3, 2, 1])

    def test_calendario_utente_utente_non_esiste(self):
        self.mock_utenti_repo.get_by_id.return_value = None
        result = self.service.calendario_utente("u1")
        self.assertEqual(result, [])

    def test_calendario_utente_aggregrato(self):
        ut = MagicMock()
        ut.gruppi = ["g1", "g2"]
        self.mock_utenti_repo.get_by_id.return_value = ut

        self.service.calendario_gruppo = MagicMock(side_effect=[
            [Incontro(1, "A", "d",
                    datetime(2024,4,1), datetime(2024,4,1,9), "g1")],
            [Incontro(2, "B", "d",
                    datetime(2024,4,1), datetime(2024,4,1,10), "g2")]
        ])

        res = self.service.calendario_utente("u1")
        self.assertEqual(len(res), 2)

    def test_incontri_futuri_filtrati(self):
        now = datetime.now()
        futuro = Incontro(1, "Futuro", "d", now + timedelta(days=2),
                          now + timedelta(days=2, hours=1), "g1")
        passato = Incontro(2, "Passato", "d", now - timedelta(days=2),
                           now - timedelta(days=2, hours=1), "g1")
        futuro.statoIncontro = IncontroStatus.PROGRAMMATO
        passato.statoIncontro = IncontroStatus.PROGRAMMATO

        self.service.calendario_gruppo = MagicMock(return_value=[futuro, passato])

        res = self.service.incontri_futuri_gruppo("g1")
        self.assertEqual([i.id for i in res], [1])

    def test_prossimo_incontro_esiste(self):
        inc1 = Incontro(1, "A", "d", datetime.now() + timedelta(days=1),
                        datetime.now(), "g1")
        self.service.incontri_futuri_gruppo = MagicMock(return_value=[inc1])
        res = self.service.prossimo_incontro_gruppo("g1")
        self.assertEqual(res, inc1)

    def test_prossimo_incontro_none(self):
        self.service.incontri_futuri_gruppo = MagicMock(return_value=[])
        res = self.service.prossimo_incontro_gruppo("g1")
        self.assertIsNone(res)

    def test_incontri_per_data(self):
        giorno = date(2024, 5, 1)

        inc1 = Incontro(1, "A", "d", datetime(2024, 5, 1), datetime(2024, 5, 1, 9), "g")
        inc1.statoIncontro = IncontroStatus.PROGRAMMATO

        inc2 = Incontro(2, "B", "d", datetime(2024, 5, 2), datetime(2024, 5, 2, 9), "g")
        inc2.statoIncontro = IncontroStatus.PROGRAMMATO

        self.service.calendario_utente = MagicMock(return_value=[inc1, inc2])

        res = self.service.incontri_per_data("u1", giorno)

        self.assertEqual([i.id for i in res], [1])


if __name__ == "__main__":
    unittest.main()
