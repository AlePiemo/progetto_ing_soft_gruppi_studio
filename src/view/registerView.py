from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

class RegisterView(QWidget):

    def __init__(self, utente_ctrl, on_register_success, on_back_login):
        super().__init__()

        self.utente_ctrl = utente_ctrl
        self.on_register_success = on_register_success
        self.on_back_login = on_back_login

        self.setWindowTitle("Registrazione - Piattaforma di Gruppi Studio")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        titolo = QLabel("Registrati")
        titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titolo)

        # Nome
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")
        layout.addWidget(self.nome_input)

        # Cognome
        self.cognome_input = QLineEdit()
        self.cognome_input.setPlaceholderText("Cognome")
        layout.addWidget(self.cognome_input)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Conferma password
        self.password2_input = QLineEdit()
        self.password2_input.setPlaceholderText("Conferma password")
        self.password2_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password2_input)

        btn_registra = QPushButton("Crea account")
        btn_registra.clicked.connect(self.registra)
        layout.addWidget(btn_registra)

        # backTo login
        btn_back = QPushButton("Torna al login")
        btn_back.clicked.connect(self.on_back_login)
        layout.addWidget(btn_back)

        self.setLayout(layout)

    # REGISTRAZIONE
    def registra(self):
        nome = self.nome_input.text()
        cognome = self.cognome_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        password2 = self.password2_input.text()

        if password != password2:
            QMessageBox.warning(self, "Errore", "Le password non coincidono.")
            return

        if not nome or not cognome or not email or not password:
            QMessageBox.warning(self, "Errore", "Compila tutti i campi.")
            return

        nuovo = self.utente_ctrl.registra_utente(
            nome=nome,
            cognome=cognome,
            email=email,
            password=password
        )

        if not nuovo:
            QMessageBox.warning(self, "Errore", "Email già utilizzata.")
            return

        QMessageBox.information(self, "Registrato", "Registrazione completata!")

        self.on_register_success()
