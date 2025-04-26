from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QCheckBox, QFrame, QGridLayout,
                           QStackedWidget, QApplication, QDesktopWidget)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, pyqtProperty, QSize
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QBrush, QIcon, QPixmap, QCursor
from styles.styles_dark import LOGIN_DARK_STYLES
from styles.styles_light import LOGIN_LIGHT_STYLES
from utils import get_icon_path


class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(45)
        self.setFont(QFont('Segoe UI', 10))

class StyledToggle(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.setCursor(Qt.PointingHandCursor)
        self._slide_pos = 0
        self._animation = QPropertyAnimation(self, b"slide_pos")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.InOutCubic)

    @pyqtProperty(float)
    def slide_pos(self):
        return self._slide_pos

    @slide_pos.setter
    def slide_pos(self, pos):
        self._slide_pos = pos
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bg_rect = self.rect()
        bg_color = QColor('#4a4a4a') if not self.isChecked() else QColor('#4CAF50')
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(bg_rect, 15, 15)

        slider_width = 26
        slider_height = 26
        margin = 2
        x = margin + self._slide_pos * (self.width() - slider_width - 2 * margin)
        slider_rect = QRect(int(x), margin, slider_width, slider_height)
        
        painter.setBrush(QBrush(QColor('white')))
        painter.drawEllipse(slider_rect)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.toggle()
        
        start_value = 1 if not self.isChecked() else 0
        end_value = 0 if not self.isChecked() else 1
        
        self._animation.setStartValue(start_value)
        self._animation.setEndValue(end_value)
        self._animation.start()

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = 'dark'
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Afet Yönetim Sistemi - Giriş")
        
        # Ekran boyutlarına göre uygun pencere boyutunu ayarla
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()
        
        # Ekranın %75'ini kaplayan boyut hesapla (giriş ekranı ana uygulamadan biraz daha küçük)
        window_width = min(int(screen_width * 0.75), 1400)
        window_height = min(int(screen_height * 0.75), 900)
        
        # Pencere boyutunu ayarla
        self.setGeometry(
            (screen_width - window_width) // 2,  # Ekranın ortasına hizalamak için X konumu
            (screen_height - window_height) // 2,  # Ekranın ortasına hizalamak için Y konumu
            window_width,
            window_height
        )
        
        # Minimum pencere boyutu ayarla (çok küçük ekranlarda bile içerik görünür olsun)
        self.setMinimumSize(800, 600)
        
        self.setStyleSheet(LOGIN_DARK_STYLES)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)
        
        # Logo Container
        logo_container = QFrame()
        logo_container.setFixedHeight(120)
        logo_container.setObjectName("logoContainer")
        
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        
        # Logo Label
        logo_label = QLabel("AFET-LINK")
        logo_label.setFont(QFont('Segoe UI', 36, QFont.Bold))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setObjectName("logoLabel")
        
        # Title Label
        title_label = QLabel("Afet Yönetim Sistemi")
        title_label.setFont(QFont('Segoe UI', 14))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("titleLabel")
        
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(title_label)
        logo_container.setLayout(logo_layout)
        main_layout.addWidget(logo_container)
        
        # Login Form Page
        login_page = QWidget()
        login_layout = QVBoxLayout()
        
        # Header Container (Back Button + Title)
        header_container = QFrame()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 20)
        
        # Title Container
        title_container = QFrame()
        title_container.setFixedWidth(400)  # Sabit genişlik
        title_layout = QVBoxLayout(title_container)
        title_layout.setAlignment(Qt.AlignCenter)
        
        self.login_label = QLabel()
        self.login_label.setFont(QFont('Segoe UI', 22, QFont.Bold))  # Biraz daha küçük
        self.login_label.setAlignment(Qt.AlignCenter)
        self.login_label.setText("Giriş")
        title_layout.addWidget(self.login_label)
        
        # Header layout düzenleme
        header_layout.addWidget(title_container)     
        header_layout.setAlignment(Qt.AlignCenter)   
        
        header_container.setLayout(header_layout)
        
        # Input Container
        input_container = QFrame()
        input_container.setObjectName("inputContainer")
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)
        
        self.username_input = StyledLineEdit("Kullanıcı Adı")
        self.username_input.setObjectName("usernameInput")
        
        self.password_input = StyledLineEdit("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("passwordInput")
        
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_input)
        input_container.setLayout(input_layout)
        
        # Theme Toggle
        theme_container = QFrame()
        theme_container.setObjectName("themeContainer")
        theme_layout = QHBoxLayout()
        
        theme_label = QLabel("Tema:")
        theme_label.setFont(QFont('Segoe UI', 10))
        
        self.theme_toggle = StyledToggle()
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_toggle)
        theme_layout.addStretch()
        theme_container.setLayout(theme_layout)
        
        # Login Button
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setFixedHeight(45)
        self.login_button.setFont(QFont('Segoe UI', 11))
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setObjectName("loginButton")
        
        # Add components to login layout
        login_layout.addWidget(header_container)
        login_layout.addWidget(input_container)
        login_layout.addWidget(theme_container)
        login_layout.addWidget(self.login_button)
        login_layout.addStretch()
        
        # Add NGO section to login page
        login_layout.addWidget(self.create_ngo_section())
        
        login_page.setLayout(login_layout)
        
        # Add login page to main layout
        main_layout.addWidget(login_page)
        
        self.setLayout(main_layout)

    def create_ngo_section(self):
        """STK bölümünü oluştur"""
        ngo_section = QFrame()
        ngo_section.setObjectName("ngoSection")
        ngo_layout = QGridLayout()
        
        ngos = [
            {"name": "AKUT", "logo": "akut.png", "color": "#e74c3c"},
            {"name": "Kızılay", "logo": "kizilay.png", "color": "#c0392b"},
            {"name": "UMKE", "logo": "umke.png", "color": "#2ecc71"},
            {"name": "İHH", "logo": "ihh.png", "color": "#3498db"},
            {"name": "Beşir Derneği", "logo": "besir.png", "color": "#9b59b6"},
            {"name": "Ahbap", "logo": "ahbap.png", "color": "#f1c40f"}
        ]
        
        for i, ngo in enumerate(ngos):
            row = i // 3
            col = i % 3
            
            ngo_container = QFrame()
            ngo_container.setObjectName(f"ngoContainer_{i}")
            ngo_container_layout = QVBoxLayout()
            
            logo_label = QLabel()
            logo_label.setFixedSize(80, 80)
            logo_label.setScaledContents(True)
            logo_label.setObjectName(f"ngoLogo_{i}")
            
            logo_path = get_icon_path(ngo["logo"])
            logo_pixmap = QPixmap(logo_path)
            if not logo_pixmap.isNull():
                logo_label.setPixmap(logo_pixmap)
            else:
                logo_label.setStyleSheet(f"background-color: {ngo['color']}; border-radius: 10px;")
                letter_label = QLabel(ngo["name"][0])
                letter_label.setFont(QFont('Segoe UI', 24, QFont.Bold))
                letter_label.setAlignment(Qt.AlignCenter)
                letter_label.setStyleSheet("color: white;")
                logo_label.setLayout(QVBoxLayout())
                logo_label.layout().addWidget(letter_label)
            
            name_label = QLabel(ngo["name"])
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
            name_label.setObjectName(f"ngoLabel_{i}")
            
            ngo_container_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
            ngo_container_layout.addWidget(name_label, alignment=Qt.AlignCenter)
            ngo_container.setLayout(ngo_container_layout)
            
            ngo_layout.addWidget(ngo_container, row, col)
        
        ngo_section.setLayout(ngo_layout)
        return ngo_section

    def toggle_theme(self):
        self.theme = 'light' if self.theme_toggle.isChecked() else 'dark'
        if self.theme == 'dark':
            self.setStyleSheet(LOGIN_DARK_STYLES)
        else:
            self.setStyleSheet(LOGIN_LIGHT_STYLES) 

def adjust_window_to_screen(window):
    """Pencereyi ekrana sığdırmak için boyutları ayarlar"""
    screen = QDesktopWidget().availableGeometry()
    
    # Ekran boyutlarını al
    screen_width = screen.width()
    screen_height = screen.height()
    
    # Pencerenin mevcut boyutlarını al
    window_width = window.width()
    window_height = window.height()
    
    # Ekrana sığacak şekilde ayarla (ekranın %90'ı kadar)
    if window_width > screen_width * 0.9:
        window_width = int(screen_width * 0.9)
    
    if window_height > screen_height * 0.9:
        window_height = int(screen_height * 0.9)
    
    # Pencere boyutunu güncelle
    window.resize(window_width, window_height)
    
    # Ekranın ortasına yerleştir
    window.move((screen_width - window_width) // 2, 
                (screen_height - window_height) // 2) 