# Çok Dilli Video Galerisi 🎥

Modern ve kullanıcı dostu bir video galerisi uygulaması. Farklı dillerdeki videoları kolayca yönetmenizi ve izlemenizi sağlar.

## ✨ Özellikler

- 🌐 8 farklı dil desteği (TR, EN, RU, ZH, HI, AR, ES, PT)
- 🎨 Modern ve şık arayüz tasarımı
- 🌓 Koyu tema
- 📱 Tam responsive tasarım
- ⚡ Hızlı video yükleme ve önbellek sistemi
- 🔄 Otomatik dil algılama
- 🎬 Video kontrolleri ve bilgi gösterimi
- 🔍 Detaylı video bilgileri (süre, boyut)
- 🚀 Vercel ile kolay deployment

## 🛠️ Teknolojiler

- Python 3.9+
- Flask 3.0.0
- OpenCV 4.9.0
- Bootstrap 5
- Font Awesome 6
- Vercel (deployment)

## 📋 Gereksinimler

```bash
flask==3.0.0
python-dotenv==1.0.0
opencv-python==4.9.0.80
gunicorn==21.2.0
Werkzeug==3.0.1
```

## 🚀 Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/kullaniciadi/video-galeri.git
cd video-galeri
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Video dosyalarını yükleyin:
   - `static/videos` klasörü oluşturun
   - Video dosyalarını aşağıdaki formatta yükleyin:
     ```
     uzaydan_gelirem_tr.mp4  (Türkçe versiyon)
     uzaydan_gelirem_en.mp4  (İngilizce versiyon)
     uzaydan_gelirem_es.mp4  (İspanyolca versiyon)
     ...
     ```

4. Uygulamayı çalıştırın:
```bash
python app.py
```

## 🌐 Vercel Deployment

1. GitHub'a push yapın:
```bash
git add .
git commit -m "İlk sürüm"
git push
```

2. Vercel'de yeni proje oluşturun:
   - GitHub reponuzu seçin
   - Framework Preset: Python
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `static`

3. Environment Variables:
   ```
   PYTHONPATH=.
   FLASK_ENV=production
   FLASK_APP=app.py
   ```

## 📝 Notlar

- Video dosya boyutu sınırı: 50MB
- Desteklenen video formatları: MP4, WEBM, MKV
- Vercel ücretsiz plan limitleri:
  - Toplam depolama: 100MB
  - Deployment başına dosya sayısı: 1000
- OpenCV gereksinimleri:
  - Windows: Visual C++ 2019 Redistributable
  - Linux: libgl1-mesa-glx

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: XYZ'`)
4. Branch'inizi push edin (`git push origin yeni-ozellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın. 