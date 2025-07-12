import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                           QTableWidgetItem, QPushButton, QSplitter, QTextEdit, 
                           QLineEdit, QHeaderView, QFrame, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

# Ana dizini sys.path'e ekleyerek modülleri bulmasını sağlıyoruz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_icon_path
from styles.styles_dark import *

from sample_data import CITIZEN_FEEDBACK_DATA, FEEDBACK_REPLIES, FEEDBACK_STATISTICS
from .data_manager import FeedbackDataManager

class CitizenFeedbackTab(QWidget):
    """Vatandaş Feedback Sistemi için sekme"""
    
    def __init__(self):
        super().__init__()
        self.data_manager = FeedbackDataManager()
        self.setStyleSheet(DARK_THEME_STYLE)
        self.initUI()
        self.load_feedbacks()
        
    def initUI(self):
        """UI bileşenlerini oluştur"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık ve bilgi alanı için container
        header_container = QFrame()
        header_container.setStyleSheet("""
            QFrame {
                background-color: #201c2b;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_container)
        
        # Başlık
        header_label = QLabel("Vatandaş Geri Bildirim Sistemi")
        header_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #E1E1E6;
            margin-bottom: 10px;
        """)
        header_layout.addWidget(header_label)
        
        # Info text
        info_label = QLabel("Bu modül, mobil uygulama üzerinden vatandaşların gönderdiği geri bildirimleri görüntüler ve yönetir.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #6c6a7c; font-size: 14px;")
        header_layout.addWidget(info_label)
        
        main_layout.addWidget(header_container)
        
        # Ana içerik splitter'ı (tablo ve detay görünümü için)
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2d2b38;
                width: 2px;
            }
        """)
        
        # Sol panel (filtreleme ve feedback listesi)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        
        # Filtre araçları
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: #201c2b;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: #E1E1E6;
            }
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setSpacing(10)
        
        # Durum filtresi
        filter_layout.addWidget(QLabel("Durum:"))
        self.status_combo = QComboBox()
        self.status_combo.setStyleSheet(COMBO_BOX_STYLE)
        self.status_combo.addItems(["Tümü", "Yeni", "Okundu"])
        self.status_combo.currentTextChanged.connect(self.filter_feedbacks)
        filter_layout.addWidget(self.status_combo)
        
        # Arama alanı
        filter_layout.addWidget(QLabel("Ara:"))
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet(SEARCH_BOX_STYLE)
        self.search_input.setPlaceholderText("Feedback içinde ara...")
        self.search_input.textChanged.connect(self.filter_feedbacks)
        filter_layout.addWidget(self.search_input)
        
        # Yenile butonu
        refresh_button = QPushButton()
        refresh_button.setIcon(QIcon(get_icon_path('refresh.png')))
        refresh_button.setToolTip("Listeyi Yenile")
        refresh_button.setFixedSize(QSize(30, 30))
        refresh_button.setStyleSheet(REFRESH_BUTTON_STYLE)
        refresh_button.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_button)
        
        left_layout.addWidget(filter_frame)
        
        # Feedback tablosu
        self.feedback_table = QTableWidget()
        self.feedback_table.setStyleSheet(TABLE_STYLE)
        self.feedback_table.setColumnCount(4)
        self.feedback_table.setHorizontalHeaderLabels(["ID", "Başlık", "Tarih", "Durum"])
        self.feedback_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.feedback_table.horizontalHeader().setStretchLastSection(False)
        self.feedback_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.feedback_table.setSelectionMode(QTableWidget.SingleSelection)
        self.feedback_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.feedback_table.setAlternatingRowColors(True)
        self.feedback_table.verticalHeader().setVisible(False)
        self.feedback_table.itemSelectionChanged.connect(self.show_feedback_details)
        
        left_layout.addWidget(self.feedback_table)
        
        # Sağ panel (feedback detayları)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 0, 0, 0)
        right_layout.setSpacing(15)
        
        # Detay görünümü için frame
        detail_frame = QFrame()
        detail_frame.setStyleSheet("""
            QFrame {
                background-color: #201c2b;
                border-radius: 8px;
                padding: 20px;
                min-width: 400px;
            }
            QLabel {
                color: #E1E1E6;
                font-weight: bold;
            }
            QLabel#detailTitle {
                color: #E1E1E6;
                font-size: 20px;
                font-weight: bold;
                padding: 5px 0;
                border-bottom: 2px solid #500073;
                margin-bottom: 15px;
            }
        """)
        detail_layout = QVBoxLayout(detail_frame)
        detail_layout.setSpacing(15)
        
        # Başlık
        detail_title = QLabel("Feedback Detayları")
        detail_title.setStyleSheet("font-size: 18px; margin-bottom: 100px; margin-top: 100px;")
        detail_layout.addWidget(detail_title)
        
        # Feedback bilgileri
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #191622;
                border-radius: 6px;
                padding: 15px;
            }
            QLabel {
                color: #6c6a7c;
                font-weight: normal;
                font-size: 13px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(10)
        
        # Bilgi etiketlerini yatay gruplar halinde düzenle
        id_date_layout = QHBoxLayout()
        self.detail_id_label = QLabel("ID: -")
        self.detail_date_label = QLabel("Tarih: -")
        id_date_layout.addWidget(self.detail_id_label)
        id_date_layout.addWidget(self.detail_date_label)
        info_layout.addLayout(id_date_layout)
        
        self.detail_email_label = QLabel("E-posta: -")
        info_layout.addWidget(self.detail_email_label)
        
        detail_layout.addWidget(info_frame)
        
        # Feedback başlığı
        title_label = QLabel("Başlık:")
        title_label.setStyleSheet("color: #E1E1E6; font-weight: bold; margin-top: 10px;")
        detail_layout.addWidget(title_label)
        
        self.detail_title = QLineEdit()
        self.detail_title.setStyleSheet("""
            QLineEdit {
                background-color: #191622;
                border: none;
                border-radius: 4px;
                padding: 8px;
                color: #E1E1E6;
                font-size: 14px;
            }
        """)
        self.detail_title.setReadOnly(True)
        detail_layout.addWidget(self.detail_title)
        
        # Feedback içeriği
        content_label = QLabel("İçerik:")
        content_label.setStyleSheet("color: #E1E1E6; font-weight: bold; margin-top: 10px;")
        detail_layout.addWidget(content_label)
        
        self.detail_content = QTextEdit()
        self.detail_content.setStyleSheet("""
            QTextEdit {
                background-color: #191622;
                border: none;
                border-radius: 4px;
                padding: 10px;
                color: #E1E1E6;
                font-size: 14px;
            }
        """)
        self.detail_content.setReadOnly(True)
        self.detail_content.setMinimumHeight(100)
        detail_layout.addWidget(self.detail_content)
        
        # Durum değiştirme
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #191622;
                border-radius: 6px;
                padding: 15px;
                margin-top: 10px;
            }
            QLabel {
                color: #E1E1E6;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setSpacing(10)
        
        status_label = QLabel("Durum:")
        status_layout.addWidget(status_label)
        
        self.detail_status = QComboBox()
        self.detail_status.setStyleSheet("""
            QComboBox {
                background-color: #201c2b;
                border: 1px solid #500073;
                border-radius: 4px;
                padding: 5px 10px;
                color: #E1E1E6;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(icons/down-arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.detail_status.addItems(["Yeni", "Okundu"])
        status_layout.addWidget(self.detail_status)
        
        save_button = QPushButton("Kaydet")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #500073;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3f005a;
            }
        """)
        save_button.clicked.connect(self.save_status_change)
        status_layout.addWidget(save_button)
        status_layout.addStretch()
        
        detail_layout.addWidget(status_frame)
        
        # Yanıt yazma alanı
        reply_label = QLabel("Yanıt:")
        reply_label.setStyleSheet("color: #E1E1E6; font-weight: bold; margin-top: 10px;")
        detail_layout.addWidget(reply_label)
        
        self.reply_text = QTextEdit()
        self.reply_text.setStyleSheet("""
            QTextEdit {
                background-color: #191622;
                border: none;
                border-radius: 4px;
                padding: 10px;
                color: #E1E1E6;
                font-size: 14px;
            }
        """)
        self.reply_text.setMinimumHeight(100)
        detail_layout.addWidget(self.reply_text)
        
        # Butonlar
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        send_reply_btn = QPushButton("Yanıt Gönder")
        send_reply_btn.setStyleSheet("""
            QPushButton {
                background-color: #500073;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3f005a;
            }
        """)
        send_reply_btn.clicked.connect(self.send_reply)
        button_layout.addWidget(send_reply_btn)
        
        mark_read_btn = QPushButton("Okundu Olarak İşaretle")
        mark_read_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        mark_read_btn.clicked.connect(self.mark_as_read)
        button_layout.addWidget(mark_read_btn)
        
        detail_layout.addLayout(button_layout)
        right_layout.addWidget(detail_frame)
        
        # Splitter'a panelleri ekle
        content_splitter.addWidget(left_panel)
        content_splitter.addWidget(right_panel)
        content_splitter.setSizes([400, 600])  # Başlangıç boyutları
        
        main_layout.addWidget(content_splitter)
        
        # İstatistik bilgisi
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: #201c2b;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: #E1E1E6;
                font-size: 14px;
                margin: 0 15px;
            }
        """)
        stats_layout = QHBoxLayout(stats_frame)
        self.total_label = QLabel("Toplam: 0")
        self.new_label = QLabel("Yeni: 0")
        self.read_label = QLabel("Okundu: 0")
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.new_label)
        stats_layout.addWidget(self.read_label)
        stats_layout.addStretch()
        main_layout.addWidget(stats_frame)
    
    def load_feedbacks(self):
        """Firebase'den geri bildirimleri yükle"""
        try:
            self.feedbacks = self.data_manager.get_all_feedbacks()
            self.update_table()
            self.update_statistics()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veriler yüklenirken hata oluştu: {str(e)}")
    
    def update_table(self):
        """Tablo verilerini güncelle"""
        self.feedback_table.setRowCount(0)
        
        # Filtrelenmiş verileri tabloya ekle
        row = 0
        for feedback in self.feedbacks:
            # Filtre uygula
            status_filter = self.status_combo.currentText()
            search_text = self.search_input.text().lower()
            
            # Duruma göre filtrele
            if status_filter != "Tümü" and feedback.get("status") != status_filter:
                continue
                
            # Arama metnine göre filtrele
            if search_text and search_text not in feedback.get("title", "").lower() and search_text not in feedback.get("description", "").lower():
                continue
                
            # Filtreyi geçen satırları ekle
            self.feedback_table.insertRow(row)
            self.feedback_table.setItem(row, 0, QTableWidgetItem(str(feedback.get("id"))))
            self.feedback_table.setItem(row, 1, QTableWidgetItem(feedback.get("title")))
            self.feedback_table.setItem(row, 2, QTableWidgetItem(str(feedback.get("timestamp"))))
            
            status_item = QTableWidgetItem(feedback.get("status"))
            if feedback.get("status") == "Yeni":
                status_item.setBackground(Qt.red)
                status_item.setForeground(Qt.white)
            elif feedback.get("status") == "Okundu":
                status_item.setBackground(Qt.green)
                status_item.setForeground(Qt.white)
            
            self.feedback_table.setItem(row, 3, status_item)
            row += 1
    
    def show_feedback_details(self):
        """Seçilen feedback'in detaylarını göster"""
        selected_items = self.feedback_table.selectedItems()
        if not selected_items:
            return
            
        selected_row = selected_items[0].row()
        feedback_id = self.feedback_table.item(selected_row, 0).text()
        
        # Seçilen feedback'i bul
        selected_feedback = None
        for feedback in self.feedbacks:
            if feedback.get("id") == feedback_id:
                selected_feedback = feedback
                break
                
        if selected_feedback:
            # Detay alanlarını doldur
            self.detail_id_label.setText(f"ID: {selected_feedback.get('id')}")
            self.detail_date_label.setText(f"Tarih: {selected_feedback.get('timestamp')}")
            self.detail_email_label.setText(f"E-posta: {selected_feedback.get('userEmail')}")
            self.detail_title.setText(selected_feedback.get("title"))
            self.detail_content.setText(selected_feedback.get("description"))
            
            # Durumu seç
            status = selected_feedback.get("status", "Yeni")
            index = self.detail_status.findText(status)
            if index >= 0:
                self.detail_status.setCurrentIndex(index)
            
            # Yanıtları göster
            try:
                replies = self.data_manager.get_feedback_replies(feedback_id)
                if hasattr(self, 'replies_text'):
                    self.replies_text.clear()
                    replies_text = ""
                    for reply in replies:
                        timestamp = reply['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                        replies_text += f"[{timestamp}] {reply['sender']}:\n{reply['content']}\n\n"
                    self.replies_text.setText(replies_text)
            except Exception as e:
                print(f"Yanıtlar yüklenirken hata: {str(e)}")
    
    def filter_feedbacks(self):
        """Feedback'leri filtrele"""
        self.update_table()
    
    def refresh_data(self):
        """Verileri yeniden yükle"""
        self.load_feedbacks()
    
    def save_status_change(self):
        """Durum değişikliğini kaydet"""
        selected_items = self.feedback_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir feedback seçin.")
            return
            
        selected_row = selected_items[0].row()
        feedback_id = self.feedback_table.item(selected_row, 0).text()
        new_status = self.detail_status.currentText()
        
        try:
            self.data_manager.update_feedback_status(feedback_id, new_status)
            
            # Yerel listeyi güncelle
            for feedback in self.feedbacks:
                if feedback.get("id") == feedback_id:
                    feedback["status"] = new_status
                    break
            
            self.update_table()
            self.update_statistics()
            
            QMessageBox.information(self, "Bilgi", "Durum değişikliği kaydedildi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Durum güncellenirken hata oluştu: {str(e)}")
    
    def send_reply(self):
        """Yanıt gönder"""
        reply_text = self.reply_text.toPlainText().strip()
        if not reply_text:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir yanıt yazın.")
            return
            
        selected_items = self.feedback_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir feedback seçin.")
            return
        
        selected_row = selected_items[0].row()
        feedback_id = self.feedback_table.item(selected_row, 0).text()
        
        try:
            # Yanıtı Firebase'e kaydet
            self.data_manager.add_reply(feedback_id, reply_text)
            
            # Yerel durumu güncelle
            for feedback in self.feedbacks:
                if feedback.get("id") == feedback_id:
                    feedback["status"] = "Okundu"
                    break
            
            self.reply_text.clear()
            self.update_table()
            self.update_statistics()
            self.show_feedback_details()  # Yanıtları yeniden yükle
            
            QMessageBox.information(self, "Bilgi", "Yanıt başarıyla gönderildi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Yanıt gönderilirken hata oluştu: {str(e)}")
    
    def mark_as_read(self):
        """Seçili feedback'i okundu olarak işaretle"""
        selected_items = self.feedback_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir feedback seçin.")
            return
            
        selected_row = selected_items[0].row()
        feedback_id = self.feedback_table.item(selected_row, 0).text()
        
        try:
            self.data_manager.update_feedback_status(feedback_id, "Okundu")
            
            # Yerel listeyi güncelle
            for feedback in self.feedbacks:
                if feedback.get("id") == feedback_id:
                    feedback["status"] = "Okundu"
                    break
            
            self.update_table()
            self.update_statistics()
            
            QMessageBox.information(self, "Bilgi", "Feedback okundu olarak işaretlendi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Durum güncellenirken hata oluştu: {str(e)}")
    
    def update_statistics(self):
        """İstatistik bilgilerini güncelle"""
        total = len(self.feedbacks)
        new_count = sum(1 for f in self.feedbacks if f.get("status") == "Yeni")
        read_count = sum(1 for f in self.feedbacks if f.get("status") == "Okundu")
        
        self.total_label.setText(f"Toplam: {total}")
        self.new_label.setText(f"Yeni: {new_count}")
        self.read_label.setText(f"Okundu: {read_count}")

        