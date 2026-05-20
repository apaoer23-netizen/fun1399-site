(function() {
    'use strict';
    
    // Only run on mobile (< 768px) or if hamburger doesn't exist
    var header = document.querySelector('.header .container');
    if (!header) return;
    if (header.querySelector('.mobile-menu-toggle')) return;
    
    // Create hamburger button
    var btn = document.createElement('button');
    btn.className = 'mobile-menu-toggle';
    btn.setAttribute('aria-label', '打開選單');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '<span></span><span></span><span></span>';
    header.appendChild(btn);
    
    // Create overlay
    var overlay = document.createElement('div');
    overlay.className = 'mobile-menu-overlay';
    document.body.appendChild(overlay);
    
    // Create slide-out menu
    var menu = document.createElement('nav');
    menu.className = 'mobile-nav';
    menu.setAttribute('aria-label', '手機版導覽');
    menu.innerHTML = 
        '<div class="mobile-nav-header">' +
            '<span class="mobile-nav-title">選單</span>' +
            '<button class="mobile-nav-close" aria-label="關閉選單">&#10005;</button>' +
        '</div>' +
        '<div class="mobile-nav-links">' +
            '<a href="/"><span class="m-icon">🏠</span>首頁</a>' +
            '<a href="/recommend/2026"><span class="m-icon">🏆</span>2026推薦</a>' +
            '<a href="/reviews/"><span class="m-icon">🔍</span>平台評測</a>' +
            '<a href="/articles/"><span class="m-icon">📚</span>攻略文章</a>' +
            '<a href="/articles/withdrawal-ranking"><span class="m-icon">💰</span>出金排行</a>' +
            '<a href="/promotions/2026-03"><span class="m-icon">🎁</span>優惠情報</a>' +
            '<a href="/about"><span class="m-icon">ℹ️</span>關於我們</a>' +
            '<div class="mobile-nav-divider"></div>' +
            '<a href="https://fun1399.ofa177.net/" target="_blank" rel="noopener" class="m-cta-play"><span class="m-icon">🎮</span>立即遊玩</a>' +
            '<a href="https://lin.ee/Mc1pb7z" target="_blank" class="m-cta-line"><span class="m-icon">💬</span>專人服務</a>' +
        '</div>';
    document.body.appendChild(menu);
    
    var closeBtn = menu.querySelector('.mobile-nav-close');
    
    function openMenu() {
        menu.classList.add('open');
        overlay.classList.add('show');
        btn.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
    }
    
    function closeMenu() {
        menu.classList.remove('open');
        overlay.classList.remove('show');
        btn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }
    
    btn.addEventListener('click', openMenu);
    closeBtn.addEventListener('click', closeMenu);
    overlay.addEventListener('click', closeMenu);
    
    // Close on link click
    menu.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', closeMenu);
    });
    
    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && menu.classList.contains('open')) {
            closeMenu();
        }
    });
})();