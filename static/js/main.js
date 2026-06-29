/**
 * 乐享 — 音乐分享与推荐网站
 * 轻量特效脚本
 */
(function () {
    'use strict';

    // ===== 1. Flash 消息自动消失 =====
    document.querySelectorAll('.alert').forEach(function (el) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getInstance(el);
            if (bsAlert) bsAlert.close();
        }, 4000);
    });

    // ===== 2. 浮动音符（仅5个，纯CSS动画，JS只负责创建DOM） =====
    (function () {
        var notes = ['♪', '♫', '♬', '♩', '🎵'];
        var frag = document.createDocumentFragment();
        var container = document.createElement('div');
        container.className = 'floating-notes';

        notes.forEach(function (note, i) {
            var span = document.createElement('span');
            span.className = 'floating-note';
            span.textContent = note;
            span.style.left = (i * 20 + 8) + '%';
            span.style.animationDelay = (i * 2) + 's';
            span.style.animationDuration = (8 + i * 1.5) + 's';
            container.appendChild(span);
        });

        document.body.appendChild(container);
    })();

    // ===== 3. 收藏 AJAX =====
    window.toggleFavorite = function (songId) {
        fetch('/song/' + songId + '/favorite', {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            var btn = document.getElementById('fav-btn');
            var count = document.getElementById('fav-count');
            if (data.status === 'favorited') {
                btn.innerHTML = '<i class="fas fa-heart me-1"></i>已收藏';
                btn.classList.remove('btn-outline-light');
                btn.classList.add('btn-danger', 'btn-favorited');
                burstParticles();
            } else {
                btn.innerHTML = '<i class="far fa-heart me-1"></i>收藏';
                btn.classList.remove('btn-danger', 'btn-favorited');
                btn.classList.add('btn-outline-light');
            }
            if (count) count.textContent = data.count;
        });
    };

    // ===== 4. 粒子爆发（收藏时触发，瞬时动画） =====
    function burstParticles() {
        var colors = ['#8b5cf6', '#a78bfa', '#f472b6', '#60a5fa'];
        var frag = document.createDocumentFragment();
        for (var i = 0; i < 12; i++) {
            var p = document.createElement('div');
            p.className = 'particle';
            p.style.left = '50%';
            p.style.top = '50%';
            p.style.width = (Math.random() * 5 + 2) + 'px';
            p.style.height = p.style.width;
            p.style.background = colors[Math.floor(Math.random() * colors.length)];
            p.style.setProperty('--tx', (Math.random() * 100 - 50) + 'px');
            p.style.setProperty('--ty', (Math.random() * -90 - 20) + 'px');
            frag.appendChild(p);
        }
        document.body.appendChild(frag);
        setTimeout(function () {
            var particles = document.querySelectorAll('.particle');
            particles.forEach(function (el) { el.remove(); });
        }, 650);
    }

    // ===== 5. 图片预览 =====
    window.previewCover = function (input) {
        var container = document.getElementById('cover-preview-container');
        var preview = document.getElementById('cover-preview');
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                if (container) container.style.display = 'block';
            };
            reader.readAsDataURL(input.files[0]);
        } else {
            if (container) container.style.display = 'none';
        }
    };

    // ===== 4. 全局主题恢复 =====
    window.applyThemeUI = function() {
        var color = localStorage.getItem('music-color') || 'default';
        var bgMode = localStorage.getItem('music-bgmode') || 'dark';
        if (color !== 'default') {
            document.documentElement.setAttribute('data-color', color);
        } else {
            document.documentElement.removeAttribute('data-color');
        }
        if (bgMode !== 'dark') {
            document.documentElement.setAttribute('data-bg', bgMode);
        } else {
            document.documentElement.removeAttribute('data-bg');
        }
        var bg = localStorage.getItem('music-bg');
        var blur = localStorage.getItem('music-blur') || '0';
        if (bg) {
            document.documentElement.style.setProperty('--custom-bg-image', 'url(' + bg + ')');
            document.documentElement.style.setProperty('--custom-bg-blur', blur + 'px');
        }
    };

    // ===== 5. 自定义背景管理 =====
    window.saveBackground = function(url) {
        localStorage.setItem('music-bg', url);
        var blurVal = localStorage.getItem('music-blur') || '0';
        document.documentElement.style.setProperty('--custom-bg-image', 'url(' + url + ')');
        document.documentElement.style.setProperty('--custom-bg-blur', blurVal + 'px');
    };

    window.clearBackground = function() {
        localStorage.removeItem('music-bg');
        localStorage.setItem('music-blur', '0');
        document.documentElement.style.setProperty('--custom-bg-image', 'none');
        document.documentElement.style.setProperty('--custom-bg-blur', '0px');
    };

})();
