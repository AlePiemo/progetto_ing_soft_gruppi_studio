from __future__ import annotations
import sys
import uuid
from model.utente import Utente, RolePlatform
from persistence.datastore import salva_datastore
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
    ADMIN_EMAIL = "admin@piattaforma.it"
    ADMIN_PASSWORD = "admin"

    esiste_admin = any(
        (u.ruoloPiattaforma == RolePlatform.ADMIN_PIATTAFORMA)
        for u in utente_ctrl.repo_utenti.get_all()
    )

    if not esiste_admin:
        admin = Utente(
            id=str(uuid.uuid4()),
            nome="Admin",
            cognome="Piattaforma",
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            ruoloPiattaforma=RolePlatform.ADMIN_PIATTAFORMA,
            sospeso=False,
            fineSospensione=None,
            ultimoAccesso=None,
        )
        utente_ctrl.repo_utenti.add(admin)
        salva_datastore(ds)

    gruppo_ctrl = GruppoController(ds)
    messaggio_ctrl = MessaggioController(ds)
    materiale_ctrl = MaterialeController(ds)
    incontro_ctrl = IncontroController(ds)
    calendario_ctrl = CalendarioController(ds)
    segnalazione_ctrl = SegnalazioneController(ds)
    notifica_ctrl = NotificaController(ds)
    backup_ctrl = BackupController(ds, utente_ctrl)

    win_login = None
    win_register = None
    win_main = None

    def torna_a_login():
        nonlocal win_register, win_main, win_login
        utente_ctrl.logout()
        if win_main:
            win_main.close()
        if win_register:
            win_register.close()
        if win_login is None:
            win_login = LoginView(
                utente_ctrl,
                on_login_success=apri_mainWindow,
                on_open_register=apri_register
            )
        win_login.show()

    # finestra principale
    def apri_mainWindow(utente):
        nonlocal win_main,win_login, win_register

        if win_login:
            win_login.close()
        if win_register:
            win_register.close()

        win_main = MainWindow(
            utente_ctrl,
            gruppo_ctrl,
            messaggio_ctrl,
            materiale_ctrl,
            incontro_ctrl,
            calendario_ctrl,
            segnalazione_ctrl,
            notifica_ctrl,
            backup_ctrl,
            on_logout=torna_a_login,
        )
        win_main.show()
    
    def apri_register():
        nonlocal win_register, win_login

        if win_login:
            win_login.close()

        win_register = RegisterView(
            utente_ctrl,
            on_register_success=torna_a_login,
            on_back_login=torna_a_login
        )
        win_register.show()

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
