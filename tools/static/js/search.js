document.addEventListener('DOMContentLoaded', () => {
    let matches = [];
    let currentIndex = 0;

    window.searchText = function () {
        const query = document.getElementById('searchInput').value.trim();
        const controls = document.querySelector('.controls');
        matches = [];
        currentIndex = 0;

        // Сбрасываем старые выделения
        document.querySelectorAll('.highlight, .current').forEach(el => {
            el.outerHTML = el.innerHTML;
        });

        if (query) {
            const regex = new RegExp(`(${query})`, 'gi');
            const elements = document.querySelectorAll('h4, h6, a');

            elements.forEach(el => {
                el.innerHTML = el.innerHTML.replace(regex, '<span class="highlight">$1</span>');
            });

            matches = Array.from(document.querySelectorAll('.highlight'));

            if (matches.length > 0) {
                controls.style.display = 'inline-block';
                highlightCurrent();
            } else {
                controls.style.display = 'none';
                document.getElementById('matchCounter').textContent = 'Совпадений не найдено';
            }
        } else {
            controls.style.display = 'none';
            document.getElementById('matchCounter').textContent = '';
        }
    };

    window.highlightCurrent = function () {
        matches.forEach(el => el.classList.remove('current'));
        if (matches.length > 0) {
            const current = matches[currentIndex];
            current.classList.add('current');
            current.scrollIntoView({ behavior: 'smooth', block: 'center' });
            document.getElementById('matchCounter').textContent =
                `Совпадение ${currentIndex + 1} из ${matches.length}`;
        }
    };

    window.nextMatch = function () {
        if (matches.length === 0) return;
        currentIndex = (currentIndex + 1) % matches.length;
        highlightCurrent();
    };

    window.prevMatch = function () {
        if (matches.length === 0) return;
        currentIndex = (currentIndex - 1 + matches.length) % matches.length;
        highlightCurrent();
    };
});
