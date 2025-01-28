// Video verileri
const videos = {
    Uzaydan_Gelirem: {
        tr: {
            url: '../static/videos/uzaydan_gelirem_tr.mp4',
            title: 'Uzaydan Gelirem (Türkçe)',
            duration: '0.0',
            size: '0.3'
        },
        en: {
            url: '../static/videos/uzaydan_gelirem_en.mp4',
            title: 'Uzaydan Gelirem (English)',
            duration: '0.0',
            size: '0.3'
        },
        ar: {
            url: '../static/videos/uzaydan_gelirem_ar.mp4',
            title: 'Uzaydan Gelirem (العربية)',
            duration: '0.0',
            size: '0.3'
        },
        es: {
            url: '../static/videos/uzaydan_gelirem_es.mp4',
            title: 'Uzaydan Gelirem (Español)',
            duration: '0.0',
            size: '0.3'
        },
        hi: {
            url: '../static/videos/uzaydan_gelirem_hi.mp4',
            title: 'Uzaydan Gelirem (हिन्दी)',
            duration: '0.0',
            size: '0.3'
        },
        pt: {
            url: '../static/videos/uzaydan_gelirem_pt.mp4',
            title: 'Uzaydan Gelirem (Português)',
            duration: '0.0',
            size: '0.3'
        },
        ru: {
            url: '../static/videos/uzaydan_gelirem_ru.mp4',
            title: 'Uzaydan Gelirem (Русский)',
            duration: '0.0',
            size: '0.3'
        },
        zh: {
            url: '../static/videos/uzaydan_gelirem_zh.mp4',
            title: 'Uzaydan Gelirem (中文)',
            duration: '0.0',
            size: '0.3'
        }
    }
};

// Sayfa yüklendiğinde videoları göster
document.addEventListener('DOMContentLoaded', () => {
    filterVideos();
});

// Seçilen dile göre videoları filtrele
function filterVideos() {
    const selectedLanguage = document.getElementById('language').value;
    const videoGallery = document.getElementById('video-gallery');
    videoGallery.innerHTML = '';

    for (const videoName in videos) {
        const video = videos[videoName][selectedLanguage];
        if (video) {
            const videoCard = createVideoCard(video);
            videoGallery.appendChild(videoCard);
        }
    }
}

// Video kartı oluştur
function createVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'video-card';

    const videoContainer = document.createElement('div');
    videoContainer.className = 'video-container';

    const videoElement = document.createElement('video');
    videoElement.controls = true;
    videoElement.preload = 'metadata';
    videoElement.crossOrigin = 'anonymous';
    videoElement.playsInline = true;
    
    // Video yükleme durumunu kontrol et
    videoElement.addEventListener('loadedmetadata', () => {
        console.log('Video metadata yüklendi:', video.url);
    });

    videoElement.addEventListener('error', (e) => {
        console.error('Video yükleme hatası:', e.target.error);
    });
    
    const source = document.createElement('source');
    source.src = video.url;
    source.type = 'video/mp4';
    
    // Hata ayıklama için
    console.log('Video yükleniyor:', video.url);
    
    videoElement.appendChild(source);
    videoContainer.appendChild(videoElement);

    const info = document.createElement('div');
    info.className = 'video-info';
    
    const title = document.createElement('h3');
    title.textContent = video.title;
    
    const details = document.createElement('p');
    details.textContent = `${video.duration} dakika • ${video.size} MB`;

    info.appendChild(title);
    info.appendChild(details);

    card.appendChild(videoContainer);
    card.appendChild(info);

    // Video yüklenemezse hata mesajı göster
    videoElement.onerror = () => {
        console.error('Video yüklenemedi:', video.url, videoElement.error);
        videoContainer.innerHTML = `
            <div style="padding: 20px; text-align: center; color: #d93025;">
                <p>Video yüklenemedi.</p>
                <p>Hata: ${videoElement.error ? videoElement.error.message : 'Bilinmeyen hata'}</p>
                <p>URL: ${video.url}</p>
            </div>
        `;
    };

    return card;
}

// Sayfa yüklenirken varsayılan dili seç
window.onload = () => {
    const userLang = navigator.language || navigator.userLanguage;
    const langSelect = document.getElementById('language');
    const shortLang = userLang.split('-')[0];
    
    if (Array.from(langSelect.options).some(opt => opt.value === shortLang)) {
        langSelect.value = shortLang;
    }
    
    filterVideos();
}; 