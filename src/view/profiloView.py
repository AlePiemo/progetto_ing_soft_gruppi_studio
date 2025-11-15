from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt

class ProfiloView(QWidget):

    def __init__(self, utente_ctrl):
        super().__init__()

        self.utente_ctrl = utente_ctrl

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Profilo Utente")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        self.lbl_nome = QLabel()
        self.lbl_cognome = QLabel()
        self.lbl_email = QLabel()
        self.lbl_ruolo = QLabel()
        self.lbl_ultimo = QLabel()
        self.lbl_sospeso = QLabel()

        for w in [
            self.lbl_nome, self.lbl_cognome, self.lbl_email,
            self.lbl_ruolo, self.lbl_ultimo, self.lbl_sospeso
        ]:
            layout.addWidget(w)

        layout.addSpacing(20)
        self.setLayout(layout)

        self.refresh()

    # MOSTRA DATI UTENTE
    def refresh(self):
        u = self.utente_ctrl.get_utente_attivo()
        if not u:
            return

        self.lbl_nome.setText(f"Nome: {u.nome}")
        self.lbl_cognome.setText(f"Cognome: {u.cognome}")
        self.lbl_email.setText(f"Email: {u.email}")
        self.lbl_ruolo.setText(f"Ruolo: {u.ruoloPiattaforma.value}")
        self.lbl_ultimo.setText(f"Ultimo accesso: {u.ultimoAccesso}")
        self.lbl_sospeso.setText(f"Sospeso: SI" if u.sospeso else "Sospeso: NO")

        