(function() {
    'use strict';
    
    // Prevent double injection
    if (document.querySelector('.float-btn-container')) return;
    
    var container = document.createElement('div');
    container.className = 'float-btn-container';
    container.setAttribute('aria-label', '快速操作');
    container.innerHTML = 
        '<a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener" aria-label="立即遊玩">' +
        '<span class="float-icon">🎮</span>' +
        '<span class="float-text">立即遊玩</span>' +
        '</a>' +
        '<a href="https://lin.ee/Mc1pb7z" class="float-service" target="_blank" aria-label="專人服務">' +
        '<span class="float-icon">💬</span>' +
        '<span class="float-text">專人服務</span>' +
        '</a>';
    
    document.body.appendChild(container);
})();