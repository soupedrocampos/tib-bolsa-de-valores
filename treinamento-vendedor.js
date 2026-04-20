let slidesData = [];
let currentSlideIndex = 0;

const container = document.getElementById('presentation-container');
const counter = document.getElementById('slide-num');

async function init() {
    try {
        const response = await fetch('slides_data.json');
        slidesData = await response.json();
        
        // Handle URL Hash for slide index
        const hash = window.location.hash.replace('#', '');
        if (hash) {
            currentSlideIndex = parseInt(hash) - 1;
        }

        renderSlide(currentSlideIndex);
        setupNavigation();
    } catch (err) {
        console.error("Failed to load slides data:", err);
    }
}

function renderSlide(index) {
    if (index < 0) index = 0;
    if (index >= slidesData.length) index = slidesData.length - 1;
    
    currentSlideIndex = index;
    const slide = slidesData[index];
    const content = slide.content;
    
    container.innerHTML = '';
    const slideEl = document.createElement('div');
    slideEl.className = 'slide active';
    
    // Determine Slide Type
    let type = 'CONTENT';
    const allText = content.join(' ');
    
    if (index === 0) type = 'COVER';
    else if (allText.includes('BLOCO')) type = 'SECTION';
    else if (content.length === 1 && content[0].length < 30) type = 'TITLE_ONLY';
    else if (content.some(l => l.includes('%'))) type = 'METRIC';
    else if (content.length > 5) type = 'LIST';

    // Build Slide HTML
    if (type === 'COVER') {
        const title = content.slice(0, 2).join(' <br> ');
        const sub = content.slice(2).join(' | ');
        slideEl.innerHTML = `
            <h1 class="slide-title" style="font-size: var(--text-fluid-xl)">${title}</h1>
            <h2 class="slide-subtitle">${sub}</h2>
        `;
    } 
    else if (type === 'SECTION') {
        const title = content.find(l => l.includes('BLOCO')) || '';
        const subtitle = content.filter(l => !l.includes('BLOCO')).join(' ');
        slideEl.classList.add('slide-section');
        slideEl.innerHTML = `
            <h2 class="slide-subtitle">${title}</h2>
            <h1 class="slide-title">${subtitle}</h1>
        `;
    }
    else if (type === 'METRIC') {
        const metric = content.find(l => l.includes('%')) || '';
        const desc = content.filter(l => !l.includes('%')).join(' ');
        slideEl.innerHTML = `
            <div class="metric-value">${metric}</div>
            <div class="content-box">
                <div class="card-item">
                    <p style="font-size: var(--text-lg); text-align: center;">${desc}</p>
                </div>
            </div>
        `;
    }
    else if (type === 'LIST') {
        const title = content[0];
        const items = content.slice(1);
        slideEl.innerHTML = `
            <h2 class="slide-subtitle" style="margin-bottom: var(--sp-10)">${title}</h2>
            <div class="point-list">
                ${items.map(item => `<div class="card-item"><p>${item}</p></div>`).join('')}
            </div>
        `;
    }
    else {
        // Default Content Slide
        const title = content.length > 0 ? content[0] : '';
        const body = content.slice(1).join('<br><br>');
        slideEl.innerHTML = `
            <h1 class="slide-title" style="font-size: var(--text-2xl)">${title}</h1>
            <div class="content-box">
                 <p style="font-size: var(--text-md); line-height: 1.6; color: var(--white-60)">${body}</p>
            </div>
        `;
    }

    container.appendChild(slideEl);
    
    // Update Counter
    counter.innerText = `${String(index + 1).padStart(2, '0')} / 155`;
    window.location.hash = index + 1;
}

function setupNavigation() {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'Space') {
            renderSlide(currentSlideIndex + 1);
        } else if (e.key === 'ArrowLeft') {
            renderSlide(currentSlideIndex - 1);
        }
    });

    // Simple Click Nav
    document.body.addEventListener('click', (e) => {
        if (e.clientX > window.innerWidth / 2) {
            renderSlide(currentSlideIndex + 1);
        } else {
            renderSlide(currentSlideIndex - 1);
        }
    });
}

init();
