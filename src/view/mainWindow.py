from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt

from view.profiloView import ProfiloView
from view.gruppiView import GruppiView
from view.chatView import ChatView
from view.materialiView import MaterialiView
from view.incontriView import IncontriView
from view.calendarioView import CalendarioView
from view.segnalazioneView import SegnalazioniView
from view.notificaView import NotificheView
from view.backupView import BackupView


class MainWindow(QMainWindow):

    def __init__(
        self,
        utente_ctrl,
        gruppo_ctrl,
        messaggio_ctrl,
        materiale_ctrl,
        incontro_ctrl,
        calendario_ctrl,
        segnalazione_ctrl,
        notifica_ctrl,
        backup_ctrl
    ):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.gruppo_ctrl = gruppo_ctrl
        self.messaggio_ctrl = messaggio_ctrl
        self.materiale_ctrl = materiale_ctrl
        self.incontro_ctrl = incontro_ctrl
        self.calendario_ctrl = calendario_ctrl
        self.segnalazione_ctrl = segnalazione_ctrl
        self.notifica_ctrl = notifica_ctrl
        self.backup_ctrl = backup_ctrl

        # Memorizza il gruppo selezionato da GruppiView
        self.gruppo_selezionato = None

        self.setWindowTitle("Piattaforma di Studio - Ing. Software")
        self.setMinimumSize(1200, 700)

        centrale = QWidget()
        layout = QHBoxLayout(centrale)

        # menu laterale
        menu = QVBoxLayout()
        menu.setSpacing(12)

        btn_profilo = QPushButton("Profilo")
        btn_gruppi = QPushButton("Gruppi")
        btn_chat = QPushButton("Chat")
        btn_materiali = QPushButton("Materiali")
        btn_incontri = QPushButton("Incontri")
        btn_calendario = QPushButton("Calendario")
        btn_segnalazioni = QPushButton("Segnalazioni")
        btn_notifiche = QPushButton("Notifiche")
        btn_backup = QPushButton("Backup")
        btn_logout = QPushButton("Logout")

        # aggiunta bottoni al menu
        for b in [
            btn_profilo, btn_gruppi, btn_chat, btn_materiali,
            btn_incontri, btn_calendario, btn_segnalazioni,
            btn_notifiche, btn_backup, btn_logout
        ]:
            menu.addWidget(b)

        self.stacked = QStackedWidget()

        # crea tutte le pagine reali
        self.view_profilo = ProfiloView(self.utente_ctrl)
        self.view_gruppi = GruppiView(self.gruppo_ctrl, self.utente_ctrl)
        self.view_chat = ChatView(self.utente_ctrl, self.gruppo_ctrl, self.messaggio_ctrl)
        self.view_materiali = MaterialiView(self.utente_ctrl, self.gruppo_ctrl, self.materiale_ctrl)
        self.view_incontri = IncontriView(self.utente_ctrl, self.gruppo_ctrl, self.incontro_ctrl)
        self.view_calendario = CalendarioView(self.utente_ctrl, self.calendario_ctrl, self.gruppo_ctrl)
        self.view_segnalazioni = SegnalazioniView(self.utente_ctrl, self.segnalazione_ctrl, self.gruppo_ctrl, self.messaggio_ctrl)
        self.view_notifiche = NotificheView(self.utente_ctrl, self.notifica_ctrl)
        self.view_backup = BackupView(self.backup_ctrl)

        # aggiungi pagine allo stacked
        self.stacked.addWidget(self.view_profilo)
        self.stacked.addWidget(self.view_gruppi)
        self.stacked.addWidget(self.view_chat)
        self.stacked.addWidget(self.view_materiali)
        self.stacked.addWidget(self.view_incontri)
        self.stacked.addWidget(self.view_calendario)
        self.stacked.addWidget(self.view_segnalazioni)
        self.stacked.addWidget(self.view_notifiche)
        self.stacked.addWidget(self.view_backup)

        btn_profilo.clicked.connect(lambda: self.stacked.setCurrentWidget(self.view_profilo))
        btn_gruppi.clicked.connect(lambda: self.apri_gruppi())
        btn_chat.clicked.connect(lambda: self.apri_chat())
        btn_materiali.clicked.connect(lambda: self.apri_materiali())
        btn_incontri.clicked.connect(lambda: self.apri_incontri())
        btn_calendario.clicked.connect(lambda: self.apri_calendario())
        btn_segnalazioni.clicked.connect(lambda: self.apri_segnalazioni())
        btn_notifiche.clicked.connect(lambda: self.apri_notifiche())
        btn_backup.clicked.connect(lambda: self.apri_backup())
        btn_logout.clicked.connect(self.logout)

        layout.addLayout(menu, 1)
        layout.addWidget(self.stacked, 4)

        self.setCentralWidget(centrale)

        self.view_gruppi.lista_gruppi.itemClicked.connect(self._on_group_selected)


    def _on_group_selected(self, item):
        """Memorizza il gruppo selezionato da GruppiView."""
        self.gruppo_selezionato = item.data(Qt.ItemDataRole.UserRole)

    def apri_gruppi(self):
        self.view_gruppi.refresh_gruppi()
        self.stacked.setCurrentWidget(self.view_gruppi)

    def apri_chat(self):
        if not self.gruppo_selezionato:
            QMessageBox.warning(self, "Errore", "Seleziona prima un gruppo.")
            return
        self.view_chat.apri_chat(self.gruppo_selezionato)
        self.stacked.setCurrentWidget(self.view_chat)

    def apri_materiali(self):
        if not self.gruppo_selezionato:
            QMessageBox.warning(self, "Errore", "Seleziona prima un gruppo.")
            return
        self.view_materiali.apri_gruppo(self.gruppo_selezionato)
        self.stacked.setCurrentWidget(self.view_materiali)

    def apri_incontri(self):
        if not self.gruppo_selezionato:
            QMessageBox.warning(self, "Errore", "Seleziona prima un gruppo.")
            return
        self.view_incontri.apri_gruppo(self.gruppo_selezionato)
        self.stacked.setCurrentWidget(self.view_incontri)

    def apri_calendario(self):
        self.view_calendario.refresh_tutto()
        self.stacked.setCurrentWidget(self.view_calendario)

    def apri_segnalazioni(self):
        self.view_segnalazioni.refresh()
        self.stacked.setCurrentWidget(self.view_segnalazioni)

    def apri_notifiche(self):
        self.view_notifiche.refresh()
        self.stacked.setCurrentWidget(self.view_notifiche)

    def apri_backup(self):
        self.view_backup.refresh()
        self.stacked.setCurrentWidget(self.view_backup)

    def logout(self):
        self.utente_ctrl.logout()
        self.close()
