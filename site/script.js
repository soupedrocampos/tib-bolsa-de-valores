/* TIB — script.js — Landing Page
   Sem Lenis, sem preloader pesado.
   Scroll nativo. Animações leves via IntersectionObserver.
*/

document.addEventListener('DOMContentLoaded', () => {

    // ─── 1. BODY VISÍVEL IMEDIATAMENTE ───────────────
    document.body.style.opacity = '1';

    // ─── 2. ESCONDE LOADER RÁPIDO ────────────────────
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(() => { loader.style.display = 'none'; }, 100);
    }

    // ─── 3. NAV visível ──────────────────────────────
    const nav = document.getElementById('siteNav');
    if (nav) nav.classList.add('visible');

    // ─── 4. SCROLL REVEAL LEVE ───────────────────────
    // Só faz fade+slide — sem blur, sem delay agressivo
    const saEls = document.querySelectorAll('.sa');
    const saObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in');
                saObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
    saEls.forEach(el => saObserver.observe(el));

    // ─── 5. RAMP-UP CHART ────────────────────────────
    const rampCard  = document.getElementById('rampCard');
    const rampPath  = document.getElementById('rampPath');
    const clipRect  = document.getElementById('clipRect');
    const peakPulse = document.getElementById('peakPulse');

    if (rampCard && rampPath) {
        // Polyline length via SVG API
        const pathLen = rampPath.getTotalLength ? rampPath.getTotalLength() : 700;
        rampPath.style.strokeDasharray  = pathLen;
        rampPath.style.strokeDashoffset = pathLen;

        new IntersectionObserver((entries) => {
            if (!entries[0].isIntersecting) return;

            // Animate stroke draw
            rampPath.style.transition = `stroke-dashoffset 1.6s cubic-bezier(0.22,1,0.36,1) 0.2s`;
            rampPath.style.strokeDashoffset = '0';

            // Animate clip rect (area fill)
            if (clipRect) {
                let w = 0;
                const clipAnim = setInterval(() => {
                    w = Math.min(w + 8, 480);
                    clipRect.setAttribute('width', w);
                    if (w >= 480) clearInterval(clipAnim);
                }, 12);
            }

            // Dots appear
            rampCard.classList.add('active');

            // Peak pulse ring
            if (peakPulse) {
                setTimeout(() => {
                    peakPulse.style.transition = 'none';
                    peakPulse.style.opacity = '0.6';
                    peakPulse.setAttribute('r', '12');
                    setTimeout(() => {
                        peakPulse.style.transition = 'opacity 0.8s ease';
                        peakPulse.style.opacity = '0';
                        peakPulse.setAttribute('r', '22');
                    }, 60);
                }, 1700);
            }

        }, { threshold: 0.3 }).observe(rampCard);
    }

    // ─── 6. CONTADORES ───────────────────────────────
    function animateCounter(el, target) {
        let startTime = null;
        const duration = 1400;
        function step(ts) {
            if (!startTime) startTime = ts;
            const pct = Math.min((ts - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - pct, 3);
            el.textContent = Math.floor(eased * target);
            if (pct < 1) requestAnimationFrame(step);
            else el.textContent = target;
        }
        requestAnimationFrame(step);
    }

    const counterEls = document.querySelectorAll('.stat-n[data-target]');
    if (counterEls.length) {
        new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    counterEls.forEach(el => {
                        animateCounter(el, parseInt(el.dataset.target, 10));
                    });
                }
            });
        }, { threshold: 0.5, once: true }).observe(counterEls[0]);
    }

    // ─── 7. PHASE SLIDES + CHART DOT SYNC ───────────
    const phaseEls   = document.querySelectorAll('.phase-hot');
    const slideEls   = document.querySelectorAll('.phase-slide');
    const dotBtns    = document.querySelectorAll('.ps-dot');
    let activeSlide  = 0;
    let slideTimer   = null;

    function goToSlide(idx) {
        slideEls.forEach((s, i) => s.classList.toggle('active', i === idx));
        dotBtns.forEach((d, i) => d.classList.toggle('active', i === idx));
        phaseEls.forEach((g, i) => g.classList.toggle('active', i === idx));
        activeSlide = idx;
    }

    function startAutoSlide() {
        clearInterval(slideTimer);
        slideTimer = setInterval(() => {
            goToSlide((activeSlide + 1) % 4);
        }, 3500);
    }

    if (slideEls.length) {
        goToSlide(0);
        startAutoSlide();

        // Chart dots → slide
        phaseEls.forEach((g, i) => {
            g.addEventListener('click', (e) => {
                e.stopPropagation();
                goToSlide(i);
                startAutoSlide();
            });
        });

        // Slide dots → slide
        dotBtns.forEach((btn) => {
            btn.addEventListener('click', () => {
                goToSlide(parseInt(btn.dataset.dot, 10));
                startAutoSlide();
            });
        });
    }

    // ─── 9. NAV SHADOW ON SCROLL (nativo, passivo) ───
    if (nav) {
        window.addEventListener('scroll', () => {
            nav.style.boxShadow = window.scrollY > 60
                ? '0 8px 40px rgba(0,0,0,0.6)'
                : 'none';
        }, { passive: true });
    }

    // ─── 10. HERO PARALLAX LEVE (CSS transform) ──────
    const heroImg = document.querySelector('.hero-img');
    if (heroImg && window.innerWidth > 768) {
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    const y = window.scrollY;
                    if (y < window.innerHeight) {
                        heroImg.style.transform = `scale(1.06) translateY(${y * 0.15}px)`;
                    }
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }

});
