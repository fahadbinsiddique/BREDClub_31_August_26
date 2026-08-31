/**
 * BREDClub - Hero Slider (অপটিমাইজড)
 * অটো স্লাইড, প্রেভ/নেক্সট, ডট, টাচ সুইপ
 */

document.addEventListener('DOMContentLoaded', function() {

    (function() {
        var slides = document.querySelectorAll('.hero-slide');
        var dots = document.querySelectorAll('.hero-dot');
        var prevBtn = document.getElementById('heroPrev');
        var nextBtn = document.getElementById('heroNext');
        if (!slides.length) return;

        var current = 0;
        var interval = null;
        var delay = 6000;

        // নির্দিষ্ট স্লাইডে যাওয়া
        function goTo(index) {
            slides[current].classList.remove('active');
            if (dots[current]) dots[current].classList.remove('active');
            current = (index + slides.length) % slides.length;
            slides[current].classList.add('active');
            if (dots[current]) dots[current].classList.add('active');
        }

        // অটো স্লাইড কন্ট্রোল
        function startAuto() { stopAuto(); interval = setInterval(function() { goTo(current + 1); }, delay); }
        function stopAuto() { if (interval) { clearInterval(interval); interval = null; } }

        // বাটন ইভেন্ট
        if (nextBtn) nextBtn.addEventListener('click', function() { goTo(current + 1); startAuto(); });
        if (prevBtn) prevBtn.addEventListener('click', function() { goTo(current - 1); startAuto(); });

        // ডট ইভেন্ট
        dots.forEach(function(dot) {
            dot.addEventListener('click', function() {
                goTo(parseInt(this.getAttribute('data-dot'), 10));
                startAuto();
            });
        });

        // হোভারে পজ
        var wrapper = document.querySelector('.hero-slides-wrapper');
        if (wrapper) {
            wrapper.addEventListener('mouseenter', stopAuto);
            wrapper.addEventListener('mouseleave', startAuto);

            // টাচ সুইপ
            var startX = 0;
            wrapper.addEventListener('touchstart', function(e) { startX = e.changedTouches[0].screenX; }, { passive: true });
            wrapper.addEventListener('touchend', function(e) {
                var diff = startX - e.changedTouches[0].screenX;
                if (diff > 50) { goTo(current + 1); startAuto(); }
                else if (diff < -50) { goTo(current - 1); startAuto(); }
            }, { passive: true });
        }

        startAuto();
    })();

});