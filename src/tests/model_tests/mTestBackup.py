import unittest
from datetime import datetime
from model.backup import Backup, BackupStatus

class TestBackupModel(unittest.TestCase):

    def test_creazione_backup(self):
        data = datetime.now()
        b = Backup(id=1, dataBackup=data, esito=True, statoBackup=BackupStatus.Completato)

        self.assertEqual(b.id, 1)
        self.assertEqual(b.dataBackup, data)
        self.assertTrue(b.esito)
        self.assertEqual(b.statoBackup, BackupStatus.Completato)

    def test_valori_enum(self):
        self.assertIn(BackupStatus.In_corso, BackupStatus)
        self.assertIn(BackupStatus.Completato, BackupStatus)

    def test_tipo_campi(self):
        b = Backup(id=5,
                   dataBackup=datetime(2024, 1, 1),
                   esito=False,
                   statoBackup=BackupStatus.In_corso)

        self.assertIsInstance(b.id, int)
        self.assertIsInstance(b.dataBackup, datetime)
        self.assertIsInstance(b.esito, bool)
        self.assertIsInstance(b.statoBackup, BackupStatus)

    def test_coerenza_esito_stato(self):
        b_ok = Backup(id=10,
                      dataBackup=datetime.now(),
                      esito=True,
                      statoBackup=BackupStatus.Completato)

        self.assertTrue(b_ok.esito)
        self.assertEqual(b_ok.statoBackup, BackupStatus.Completato)

        b_fail = Backup(id=11,
                        dataBackup=datetime.now(),
                        esito=False,
                        statoBackup=BackupStatus.In_corso)

        self.assertFalse(b_fail.esito)
        self.assertEqual(b_fail.statoBackup, BackupStatus.In_corso)


if __name__ == "__main__":
    unittest.main()
