from __future__ import annotations
import sys
from PyQt6.QtWidgets import QApplication

from persistence.datastore import carica_datastore, salva_datastore
from controller.utenteController import UtenteController
from controller.gruppoController import GruppoController
from controller.messaggioController import MessaggioController
from controller.materialeController import MaterialeController
from controller.incontroController import IncontroController
from controller.calendarioController import CalendarioController
from controller.segnalazioneController import SegnalazioneController
from controller.notificaController import NotificaController
from controller.backupController import BackupController

from view.mainWindow import MainWindow
from view.loginView import LoginView
from view.registerView import RegisterView

def main():
    app = QApplication(sys.argv)

    # carica datastore
    ds = carica_datastore()

    # controller
    utente_ctrl = UtenteController(ds)
    gruppo_ctrl = GruppoController(ds)
    messaggio_ctrl = MessaggioController(ds)
    materiale_ctrl = MaterialeController(ds)
    incontro_ctrl = IncontroController(ds)
    calendario_ctrl = CalendarioController(ds)
    segnalazione_ctrl = SegnalazioneController(ds)
    notifica_ctrl = NotificaController(ds)
    backup_ctrl = BackupController(ds)

    win_login = None
    win_register = None
    win_main = None

    # finestra principale
    def apri_mainWindow(utente):
        nonlocal win_main,win_login
        win_main = MainWindow(
            utente_ctrl,
            gruppo_ctrl,
            messaggio_ctrl,
            materiale_ctrl,
            incontro_ctrl,
            calendario_ctrl,
            segnalazione_ctrl,
            notifica_ctrl,
            backup_ctrl
        )
        win_main.show()
        win_login.close()
    
    def apri_register():
        nonlocal win_register, win_login
        win_register = RegisterView(
            utente_ctrl,
            on_register_success=torna_a_login,
            on_back_login=torna_a_login
        )
        win_register.show()
        win_login.close()
    
    def torna_a_login():
        nonlocal win_register, win_login
        win_register.close()
        win_login.show()

    win_login = LoginView(
        utente_ctrl,
        on_login_success=apri_mainWindow,
        on_open_register=apri_register
    )

    win_login.show()

    exit=app.exec()

    salva_datastore(ds)

    sys.exit(exit)

if __name__ == "__main__":
    main()
