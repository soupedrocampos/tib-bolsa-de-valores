document.addEventListener('DOMContentLoaded', () => {

    // ── Secret Nav (triple-click on copyright) ─
    const trigger   = document.getElementById('copyright-trigger');
    const secretNav = document.getElementById('secret-nav');
    let clickCount = 0, clickTimer;
    trigger.addEventListener('click', () => {
        clickCount++;
        clearTimeout(clickTimer);
        clickTimer = setTimeout(() => { clickCount = 0; }, 600);
        if (clickCount >= 3) {
            clickCount = 0;
            secretNav.classList.toggle('visible');
        }
    });
    document.addEventListener('click', (e) => {
        if (!trigger.contains(e.target) && !secretNav.contains(e.target)) {
            secretNav.classList.remove('visible');
        }
    });

    // ── Hero Slideshow ────────────────────────
    const heroSlides = document.querySelectorAll('.hero-slide');
    const badgeText  = document.getElementById('badgeText');
    const heroPrev   = document.getElementById('heroPrev');
    const heroNext   = document.getElementById('heroNext');
    let currentSlide = 0;
    let slideTimer;

    const slideBadges = [
        'Valorização contínua · Litoral Catarinense',
        'Patrimônio sólido · Alto Padrão SC',
        'Maior retorno imobiliário do Brasil',
        'Invista na planta · Fase de maior deságio',
        'Segurança jurídica total · Permuta validada',
        'Litoral mais visitado do Brasil · Itapema',
        'Deságio real em imóveis de alto padrão',
        'Crescimento vertical acelerado · Meia Praia',
        'Permuta validada com liquidez real',
        'Exclusivo para investidores de grande visão',
        'Segurança jurídica · Meia Praia, Itapema',
        'Curadoria premium · Litoral Catarinense',
        'Destino número um do litoral sul do Brasil',
        'Imóveis que geram riqueza real · SC',
    ];

    function goToSlide(idx) {
        const prev = currentSlide;
        currentSlide = (idx + heroSlides.length) % heroSlides.length;

        heroSlides[prev].classList.remove('active');
        heroSlides[prev].classList.add('leaving');
        setTimeout(() => heroSlides[prev].classList.remove('leaving'), 1100);
        heroSlides[currentSlide].classList.add('active');

        if (badgeText) {
            badgeText.classList.add('fade-out');
            setTimeout(() => {
                badgeText.textContent = slideBadges[currentSlide] || '';
                badgeText.classList.remove('fade-out');
                badgeText.classList.add('fade-in');
                setTimeout(() => badgeText.classList.remove('fade-in'), 400);
            }, 300);
        }
    }

    function nextSlide() { goToSlide(currentSlide + 1); }
    function prevSlide() { goToSlide(currentSlide - 1); }

    function startTimer() {
        clearInterval(slideTimer);
        slideTimer = setInterval(nextSlide, 5000);
    }

    if (heroNext) heroNext.addEventListener('click', () => { nextSlide(); startTimer(); });
    if (heroPrev) heroPrev.addEventListener('click', () => { prevSlide(); startTimer(); });

    // startTimer(); — apresentação: hero fixo no slide 1

    // ── Parallax hero + sunset ────────────────
    const heroImg   = document.getElementById('heroImg');
    const sunsetImg = document.getElementById('sunsetImg');
    window.addEventListener('scroll', () => {
        const y = window.scrollY;
        if (heroImg)   heroImg.style.transform   = `translateY(${y * 0.25}px)`;
        if (sunsetImg) {
            const el   = sunsetImg.closest('.s-visual-cta');
            const rect = el ? el.getBoundingClientRect() : null;
            if (rect) {
                const offset = (window.innerHeight - rect.top) * 0.1;
                sunsetImg.style.transform = `translateY(${offset}px)`;
            }
        }
    }, { passive: true });

    // ── NAV visible + scrolled ───────────────
    const nav = document.getElementById('siteNav');
    const navCtaFixed = document.querySelector('.nav-cta-fixed');
    setTimeout(() => {
        nav.classList.add('visible');
        if (navCtaFixed) navCtaFixed.classList.add('visible');
    }, 80);
    window.addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });

    // ── Active nav links ─────────────────────
    const sections = document.querySelectorAll('section[id]');
    const links    = document.querySelectorAll('.nav-links li a');
    const secObs = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                links.forEach(l => l.classList.remove('active'));
                const a = document.querySelector(`.nav-links li a[href="#${e.target.id}"]`);
                if (a) a.classList.add('active');
            }
        });
    }, { threshold: 0.35 });
    sections.forEach(s => secObs.observe(s));

    // ── Scroll reveal ────────────────────────
    const obs = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target); }
        });
    }, { threshold: 0.07, rootMargin: '0px 0px -28px 0px' });
    document.querySelectorAll('.sa').forEach(el => obs.observe(el));

    // ── Counter animation ────────────────────
    function animCounter(el) {
        const target = +el.getAttribute('data-target');
        if (!target) return;
        let current = 0;
        const step = Math.ceil(target / 60);
        const timer = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current;
            if (current >= target) clearInterval(timer);
        }, 22);
    }
    const counterObs = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.querySelectorAll('[data-target]').forEach(animCounter);
                counterObs.unobserve(e.target);
            }
        });
    }, { threshold: 0.4 });
    document.querySelectorAll('.sobre-stats').forEach(el => counterObs.observe(el));
    document.querySelectorAll('.op-kpi-row').forEach(el => counterObs.observe(el));

    // ── Ramp-Up chart animation ──────────────
    const rampCard  = document.getElementById('rampCard');
    const clipRect  = document.getElementById('clipRect');
    const peakPulse = document.getElementById('peakPulse');

    const rampObs = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) {
            // Trigger CSS segment animations + dots + $ signs
            rampCard.classList.add('animate');

            // Animate area fill clip over 6.5s total
            let w = 0;
            const clipAnim = setInterval(() => {
                w = Math.min(w + 4, 480);
                clipRect.setAttribute('width', w);
                if (w >= 480) clearInterval(clipAnim);
            }, 54);

            // Peak pulse ring (after last segment completes ~6.1s)
            setTimeout(() => {
                if (!peakPulse) return;
                peakPulse.style.transition = 'none';
                peakPulse.style.opacity = '0.6';
                peakPulse.setAttribute('r', '12');
                setTimeout(() => {
                    peakPulse.style.transition = 'opacity 0.8s ease, r 0.8s ease';
                    peakPulse.style.opacity = '0';
                    peakPulse.setAttribute('r', '26');
                }, 50);
            }, 6300);

            rampObs.unobserve(rampCard);
        }
    }, { threshold: 0.3 });
    if (rampCard) rampObs.observe(rampCard);

    /* ── Op Pillars Carousel ── */
    (function() {
        const track   = document.getElementById('opTrack');
        const pillars = track ? Array.from(track.querySelectorAll('.op-pillar')) : [];
        const dots    = Array.from(document.querySelectorAll('.op-dot'));
        const btnPrev = document.getElementById('opPrev');
        const btnNext = document.getElementById('opNext');
        if (!pillars.length) return;

        let current = 0;
        let autoTimer;

        function goTo(idx) {
            pillars[current].classList.remove('active');
            dots[current].classList.remove('active');
            current = (idx + pillars.length) % pillars.length;
            track.style.transform = `translateX(-${current * 100}%)`;
            pillars[current].classList.add('active');
            dots[current].classList.add('active');
        }

        function startAuto() {
            clearInterval(autoTimer);
            autoTimer = setInterval(() => goTo(current + 1), 4200);
        }

        btnNext && btnNext.addEventListener('click', () => { goTo(current + 1); startAuto(); });
        btnPrev && btnPrev.addEventListener('click', () => { goTo(current - 1); startAuto(); });
        dots.forEach(d => d.addEventListener('click', () => { goTo(+d.dataset.idx); startAuto(); }));

        /* pause on hover */
        const carousel = document.getElementById('opCarousel');
        carousel && carousel.addEventListener('mouseenter', () => clearInterval(autoTimer));
        carousel && carousel.addEventListener('mouseleave', startAuto);

        startAuto();
    })();

    // ── Blog category filter ──────────────
    document.querySelectorAll('.blog-cat').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.blog-cat').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const cat = btn.dataset.cat;
            document.querySelectorAll('.blog-card').forEach(card => {
                if (cat === 'todos' || card.dataset.cat === cat) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // ── Depoimentos carousel (infinite auto-scroll) ──────────────
    (function() {
        const grid  = document.querySelector('.depo-grid');
        const track = document.querySelector('.depo-track');
        if (!grid || !track) return;

        // Duplicate all cards for seamless loop
        Array.from(track.children).forEach(c => track.appendChild(c.cloneNode(true)));

        let pos = 0;
        let paused = false;
        let isDragging = false;
        let dragStart = 0;
        let posAtDrag = 0;
        const SPEED = 0.6; // px per frame

        function halfWidth() {
            return track.scrollWidth / 2;
        }

        function tick() {
            if (!paused && !isDragging) {
                pos += SPEED;
                if (pos >= halfWidth()) pos -= halfWidth();
            }
            track.style.transform = `translateX(-${pos}px)`;
            requestAnimationFrame(tick);
        }

        grid.addEventListener('mouseenter', () => { paused = true; });
        grid.addEventListener('mouseleave', () => { paused = false; });

        grid.addEventListener('mousedown', e => {
            isDragging = true;
            dragStart = e.clientX;
            posAtDrag = pos;
            grid.classList.add('dragging');
        });
        window.addEventListener('mousemove', e => {
            if (!isDragging) return;
            pos = posAtDrag - (e.clientX - dragStart);
            if (pos < 0) pos += halfWidth();
            if (pos >= halfWidth()) pos -= halfWidth();
        });
        window.addEventListener('mouseup', () => {
            isDragging = false;
            grid.classList.remove('dragging');
        });

        tick();
    })();
});