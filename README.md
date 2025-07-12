# 📦 Afet Koordinasyon Depo

---

## 📖 Abstract

**Afet Koordinasyon Depo**, TÜBİTAK destekli Afet-Link platformunun bir alt bileşeni olarak geliştirilmiştir. Bu proje, afet durumlarında **depo yönetimi**, **malzeme takibi** ve **kaynak yönlendirme** gibi kritik görevleri üstlenen sorumlu kullanıcılar için özel olarak tasarlanmıştır.

Afet-Link sistemine entegre çalışan bu masaüstü uygulama, afet öncesi hazırlık ve afet sonrası kaynak dağıtımı gibi önemli süreçlerde görev alan **depo sorumluları, STK temsilcileri ve süper admin** kullanıcıları için sade, hızlı ve etkin bir yönetim arayüzü sunar.

Proje, sahadaki geri bildirimler doğrultusunda şekillendirilmiş ve gerçek ihtiyaçlara odaklanarak geliştirilmiştir.

---

## 🚀 Özellikler

### 📅 Afet Öncesi

- 📊 **Depo Takibi ve Stok Yönetimi**  
  Yardım malzemelerinin, ekipmanların ve kritik kaynakların giriş-çıkış takibi.

- 📁 **Kritik Malzeme Grupları Oluşturma**  
  Belirli afet türlerine veya acil durumlara özel hızlı erişim için kategori bazlı gruplama.

- 📌 **Güncel Envanter Görüntüleme**  
  Tüm depo içeriğine tek ekran üzerinden erişim.

- 📋 **Raporlama**  
  Depo hareketleri, stok durumları ve gönderim geçmişine dair detaylı raporlar oluşturma.

### ⚡ Afet Sırası

- 🆘 **Acil Talep Sistemi**  
  Saha ekiplerinden gelen ihtiyaç taleplerine göre malzeme hazırlığı ve yönlendirmesi.

- 🧾 **Malzeme Gönderim Kaydı**  
  Gönderilen yardım paketlerinin kayıt altına alınması ve takip edilmesi.

- 👥 **Kullanıcı Yetkilendirme**  
  Hangi personelin hangi depoya erişebileceğini kontrol eden kullanıcı bazlı yetkilendirme sistemi.

- 💬 **Entegre Geri Bildirim Okuma**  
  Saha ekiplerinin talep ve geri bildirimlerini anlık olarak görüntüleyebilme.

### 📦 Afet Sonrası

- 🏕️ **İhtiyaçların Dağılımına Göre Planlama**  
  Bölgelere göre ihtiyaç yoğunluğu analizine dayalı kaynak yönlendirmesi.

- 🗂️ **Geçmiş Hareket Günlüğü**  
  Yardım gönderim geçmişiyle denetim ve analiz kolaylığı.

- 🧭 **Gerçek Zamanlı Karar Takibi**  
  Depo yöneticilerinin aldığı kararların sistemsel takibi ve kayıt altına alınması.

---

## 💻 Teknolojiler

| Katman          | Kullanılan Teknolojiler                     |
|-----------------|----------------------------------------------|
| 🖥️ **Frontend**   | React Native, PyQt                         |
| 🗄️ **Veritabanı** | NoSql                                      |
| ☁️ **Bulut**      | Google Cloud, Firebase                      |
| 🔒 **Güvenlik**   | AES (Advanced Encryption Standard)         |

---

## 📄 Lisans

Bu proje [GNU General Public License v3.0 (GPL-3.0)](https://www.gnu.org/licenses/gpl-3.0.html) kapsamında lisanslanmıştır.

- ✅ Projeyi kullanabilir, dağıtabilir ve değiştirebilirsiniz.  
- ✅ Türev çalışmalar yapabilirsiniz.  
- ⚖️ Ancak tüm türev projelerde de **GPL-3.0** lisansı kullanılmalıdır.  
- ❌ Projeyi kapalı kaynaklı bir sistemde kullanamazsınız.  

---

## 🤝 Geliştiriciler İçin Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen ilgili repoyu fork edin, değişikliklerinizi yapın ve bir pull request gönderin. Her türlü geri bildirime açığız! 🚀

📂 İlgili Repolar

- Ana Platform: [Afet-Link](https://github.com/mamitheprofessional/afet_koordinasyon)  
- Mobil Uygulama: [Afet Koordinasyon Mobil](https://github.com/orucfatih/afet_koordinasyon_mobil)  
- **Bu Depo:** [Afet Koordinasyon Depo](https://github.com/hiphop4eva/afet_koordinasyon_depo)

☕ Destek Olmak İsterseniz  
[Buy Me a Coffee](https://buymeacoffee.com/mamitheprofessional)

---

## 🛠️ Kurulum Rehberi

### 1. 📦 Gereksinimlerin Kurulumu

Proje klasörüne terminal üzerinden girerek aşağıdaki komutu çalıştırın:

```bash
pip install -r requirements.txt
```

> 💡 Python 3.10+ kullanmanız önerilir. Gerekirse `venv` ile sanal ortam oluşturabilirsiniz.

---

### 2. 🔑 Giriş Sistemi

İlk çalıştırmada giriş ekranı açılacaktır. Aşağıdaki örnek kullanıcı bilgileriyle sisteme giriş yapabilirsiniz:

| Rol             | Kullanıcı Adı | Şifre |
|------------------|---------------|-------|
| **Admin**        | `a`           | `a`   |
| **Süper Admin**  | `b`           | `b`   |
| **STK - AKUT**   | `c`           | `c`   |

---

### 3. 🔐 Firebase Kimlik Bilgilerini `.env` Dosyasına Girme

- [Firebase Console](https://console.firebase.google.com/) üzerinden kendi projenize girin.
- Menüden:  
  **Project Settings → Service Accounts → Generate New Private Key**  
  adımlarını takip ederek bir `.json` dosyası indirin.
- Bu `.json` dosyasını açın ve içindeki bilgileri uygun şekilde `.env` dosyasına **kopyalayın**.

```env
FIREBASE_ADMIN_PROJECT_ID=your_project_id
FIREBASE_ADMIN_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_ADMIN_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n
FIREBASE_ADMIN_CLIENT_EMAIL=your_client_email@your_project_id.iam.gserviceaccount.com
FIREBASE_ADMIN_CLIENT_ID=your_client_id
FIREBASE_DATABASE_URL=https://your_project_id-default-rtdb.europe-west1.firebasedatabase.app
FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
```

---

🎉 **Tebrikler!** Depo modülünüz artık kullanıma hazır.

---

## 🙏 Teşekkür

Afet-Link projesinin geliştirilmesi sürecinde verdikleri değerli desteklerden dolayı;

- Projemizi destekleyen **TÜBİTAK**'a,  
- Akademik bilgi ve yol göstericilikleri ile katkı sağlayan **İzmir Bakırçay Üniversitesi Dr. Öğr. Üyesi Murat UÇAR** ve **Arş. Gör. Emre TURAN**'a,  
- Sahadan sağladıkları tecrübe ve önerilerle projemizin ihtiyaçlara uygun şekilde şekillenmesine yardımcı olan **İzmir AFAD ekibine**, özellikle de **Sayın Demirkan Sarıkaya**'ya

en içten teşekkürlerimizi sunarız.

Afet yönetiminde daha etkin ve hızlı çözümler üretebilme hedefimize katkı sağlayan tüm kişi ve kurumlara şükranlarımızı sunarız.

---

## 📬 İletişim

Herhangi bir sorunuz veya öneriniz varsa bizimle iletişime geçebilirsiniz:  
**✉️ Email:** mpolat7635@gmail.com  
**🌐 Web:** [Afet-Link](https://github.com/kullaniciAdi/afet-link)