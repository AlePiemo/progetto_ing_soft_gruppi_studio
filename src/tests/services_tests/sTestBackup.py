import unittest
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime
from services.backupService import BackupService
from model.backup import BackupStatus, Backup

class TestBackupService(unittest.TestCase):

    def setUp(self):
        self.mock_datastore = MagicMock()
        self.mock_repo = MagicMock()
        
        patcher_repo = patch('services.backupService.BackupRepository', return_value=self.mock_repo)
        self.addCleanup(patcher_repo.stop)
        self.mock_repo_class = patcher_repo.start()

        patcher_salva = patch('services.backupService.salva_datastore')
        self.addCleanup(patcher_salva.stop)
        self.mock_salva = patcher_salva.start()

        self.service = BackupService(self.mock_datastore)

    @patch("builtins.open", new_callable=mock_open)
    @patch("pickle.dump")
    def test_backup_automatico(self, mock_pickle_dump, mock_file):
        result: Backup = self.service.backup_automatico()

        self.assertIsInstance(result, Backup)

        self.assertEqual(result.statoBackup, BackupStatus.Completato)
        self.assertIsInstance(result.dataBackup, datetime)

        mock_pickle_dump.assert_called_once()

        self.mock_repo.add.assert_called_once_with(result)

        self.mock_salva.assert_called_once()

        self.assertTrue(result.esito)

    @patch("builtins.open", new_callable=mock_open)
    @patch("pickle.dump")
    def test_backup_manuale(self, mock_pickle_dump, mock_file):
        result: Backup = self.service.backup_manuale()

        self.assertIsInstance(result, Backup)
        self.assertEqual(result.statoBackup, BackupStatus.Completato)
        self.assertIsInstance(result.dataBackup, datetime)
        
        mock_pickle_dump.assert_called_once()
        self.mock_repo.add.assert_called_once_with(result)
        self.mock_salva.assert_called_once()
        self.assertTrue(result.esito)

    def test_lista_backup(self):
        self.mock_repo.get_all.return_value = ["a", "b", "c"]

        result = self.service.lista_backup()

        self.mock_repo.get_all.assert_called_once()
        self.assertEqual(result, ["a", "b", "c"])

if __name__ == "__main__":
    unittest.main()
