from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMessageBox,
                            QToolButton, QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
import os
import sys
from PyQt5.QtWidgets import QApplication

# Ana dizini sys.path'e ekleyerek modülleri bulmasını sağlıyoruz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resources_management.kaynak_yonetimi import KaynakYonetimTab
from styles.styles_dark import *
from styles.styles_light import *
from utils import get_icon_path
from equipment_management.equipment_management import EquipmentManagementTab
from feedbacks.citizen_feedbacks import CitizenFeedbackTab
from message.message import MessageManager
# Ana dizini sys.path'e ekleyerek modülleri bulmasını sağlıyoruz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AfetYonetimAdmin(QMainWindow):
    """Ana Uygulama Penceresi"""
    def __init__(self, initial_theme='dark'):
        super().__init__()
        self.current_theme = initial_theme
        self.message_manager = MessageManager(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Afet Yönetim Sistemi - Afet-Link")
        
        # Ekran boyutlarına göre uygun pencere boyutunu ayarla
        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()
        
        # Ekranın %85'ini kaplayan boyut hesapla
        window_width = int(screen_width * 0.65)
        window_height = int(screen_height * 0.65)
        
        # Pencere boyutunu ayarla
        self.setGeometry(
            (screen_width - window_width) // 2,  # Ekranın ortasına hizalamak için X konumu
            (screen_height - window_height) // 2,  # Ekranın ortasına hizalamak için Y konumu
            window_width,
            window_height
        )
        
        # Minimum pencere boyutu ayarla (çok küçük ekranlarda bile içerik görünür olsun)
        self.setMinimumSize(800, 600)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        self.equipment_management = EquipmentManagementTab(self)

        main_layout.addWidget(self.equipment_management)
        
        # İlk başta seçilen temayı uygula
        self.setStyleSheet(DARK_THEME_STYLE if self.current_theme == 'dark' else LIGHT_THEME_STYLE)

    def closeEvent(self, event):
        """Kapatma butonu (çarpı) tıklanınca uyarı verir."""
        reply = QMessageBox.question(
            self,
            "Çıkış Onayı",
            "Uygulamayı kapatmak istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            event.ignore()  # Kapatma işlemini iptal et
        else:
            event.accept()  # Kapatma işlemini onayla