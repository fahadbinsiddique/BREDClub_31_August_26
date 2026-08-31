/**
 * BREDClub - Main JavaScript (অপটিমাইজড)
 * প্রতিটি ফাংশনে বাংলায় কমেন্ট
 */

document.addEventListener('DOMContentLoaded', function() {

    // ==========================================
    // ১. লোডার - DOMContentLoaded তেই সরে যাবে
    //    আর জোর করে অপেক্ষা করবে না, তাই দ্রুত সরে যাবে
    // ==========================================
    (function() {
        var loader = document.getElementById('pageLoader');
        if (loader) {
            loader.classList.add('hidden');
        }
    })();

    // ==========================================
    // ২. স্টিকি হেডার ও টপবার হাইড
    // ==========================================
    (function() {
        var navbar = document.getElementById('navbar');
        var topbar = document.getElementById('topbar');
        if (!navbar) return;

        var ticking = false; // পারফরম্যান্সের জন্য

        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(function() {
                    var y = window.scrollY;
                    if (y > 100) {
                        navbar.classList.add('scrolled');
                    } else {
                        navbar.classList.remove('scrolled');
                    }
                    if (topbar) {
                        if (y > 50) topbar.classList.add('hidden');
                        else topbar.classList.remove('hidden');
                    }
                    ticking = false;
                });
                ticking = true;
            }
        });
    })();

    // ==========================================
    // ৩. মোবাইল মেনু
    // ==========================================
    (function() {
        var toggle = document.getElementById('navToggle');
        var menu = document.getElementById('mobileMenu');
        if (!toggle || !menu) return;

        toggle.addEventListener('click', function() {
            toggle.classList.toggle('active');
            menu.classList.toggle('open');
        });

                // মোবাইল ড্রপডাউন টগল
        document.querySelectorAll('.mobile-dropdown > .mobile-nav-link').forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                // অন্য সব ড্রপডাউন বন্ধ করুন
                document.querySelectorAll('.mobile-dropdown.open').forEach(function(openDrop) {
                    if (openDrop !== btn.parentElement) openDrop.classList.remove('open');
                });
                // ক্লিক করা ড্রপডাউন টগল করুন
                btn.parentElement.classList.toggle('open');
            });
        });

        // মেনুর লিংকে ক্লিকে মেনু বন্ধ
        menu.querySelectorAll('.mobile-nav-link').forEach(function(link) {
            link.addEventListener('click', function() {
                if (link.parentElement && link.parentElement.classList.contains('mobile-dropdown')) return;
                toggle.classList.remove('active');
                menu.classList.remove('open');
            });
        });

        // বাইরে ক্লিকে মেনু বন্ধ
        document.addEventListener('click', function(e) {
            if (!toggle.contains(e.target) && !menu.contains(e.target)) {
                toggle.classList.remove('active');
                menu.classList.remove('open');
            }
        });
    })();

    // ==========================================
    // ৪. স্ক্রল টু টপ
    // ==========================================
    (function() {
        var btn = document.getElementById('scrollTop');
        if (!btn) return;

        window.addEventListener('scroll', function() {
            if (window.scrollY > 400) btn.classList.add('visible');
            else btn.classList.remove('visible');
        });

        btn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    })();

    // ==========================================
    // ৫. স্ক্রল ফেড-ইন অ্যানিমেশন
    // ==========================================
    (function() {
        var els = document.querySelectorAll('.fade-in');
        if (!els.length) return;

        // পারফরম্যান্সের জন্য শুধু ভিউপোর্টের কাছের এলিমেন্ট চেক
        if ('IntersectionObserver' in window) {
            var obs = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        obs.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '0px 0px -40px 0px', threshold: 0.1 });

            els.forEach(function(el) { obs.observe(el); });
        } else {
            // পুরনো ব্রাউজারে সব দেখানো
            els.forEach(function(el) { el.classList.add('visible'); });
        }
    })();

    // ==========================================
    // ৬. কাউন্টার অ্যানিমেশন
    // ==========================================
    (function() {
        var counters = document.querySelectorAll('.counter-number');
        if (!counters.length) return;

        var started = false;

        function countUp() {
            if (started) return;
            started = true;
            counters.forEach(function(el) {
                var target = parseInt(el.getAttribute('data-target'), 10);
                var duration = 2000;
                var step = 30;
                var steps = duration / step;
                var inc = target / steps;
                var cur = 0;
                var timer = setInterval(function() {
                    cur += inc;
                    if (cur >= target) { cur = target; clearInterval(timer); }
                    el.textContent = Math.floor(cur).toLocaleString('en-BD');
                }, step);
            });
        }

        var section = document.querySelector('.counter-section');
        if (section && 'IntersectionObserver' in window) {
            new IntersectionObserver(function(entries) {
                if (entries[0].isIntersecting) { countUp(); this.unobserve(section); }
            }, { threshold: 0.3 }).observe(section);
        }
    })();

    // ==========================================
    // ৭. নিউজলেটার ভ্যালিডেশন
    // ==========================================
    (function() {
        var form = document.getElementById('newsletterForm');
        var input = document.getElementById('newsletterEmail');
        var msg = document.getElementById('newsletterMsg');
        if (!form || !input || !msg) return;

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var val = input.value.trim();
            if (!val) { showMsg('Please enter your email address.', 'error'); return; }
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) { showMsg('Please enter a valid email address.', 'error'); return; }
            showMsg('Subscription successful! Thank you.', 'success');
            input.value = '';
        });

        function showMsg(text, type) {
            msg.textContent = text;
            msg.className = 'newsletter-msg ' + type;
            setTimeout(function() { msg.textContent = ''; msg.className = 'newsletter-msg'; }, 4000);
        }
    })();

    // ==========================================
    // ৮. ভলান্টিয়ার ও কন্টাক্ট ফর্ম হ্যান্ডলিং
    // ==========================================
    (function() {
        var forms = [
            { id: 'volunteerForm', msgId: 'volFormMsg' },
            { id: 'contactForm', msgId: 'contactFormMsg' }
        ];

        forms.forEach(function(f) {
            var form = document.getElementById(f.id);
            var msgEl = document.getElementById(f.msgId);
            if (!form || !msgEl) return;

            form.addEventListener('submit', function(e) {
                e.preventDefault();
                // সাধারণ সাবমিশন মেসেজ (ব্যাকএন্ড ছাড়া)
                showFormMsg(msgEl, 'Your submission has been received. Thank you!', 'success');
                form.reset();
            });
        });

        function showFormMsg(el, text, type) {
            el.textContent = text;
            el.className = 'form-msg ' + type;
            setTimeout(function() { el.textContent = ''; el.className = 'form-msg'; }, 5000);
        }
    })();

    // ==========================================
    // ৯. স্মুথ স্ক্রল (শুধু হ্যাশ লিংক)
    // ==========================================
    (function() {
        document.querySelectorAll('a[href^="#"]').forEach(function(link) {
            link.addEventListener('click', function(e) {
                var href = this.getAttribute('href');
                if (href === '#') return;
                var target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    })();

});
