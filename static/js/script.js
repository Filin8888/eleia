document.addEventListener('DOMContentLoaded', function() {
    const burgerBtn = document.getElementById('burger');
    const mobileMenu = document.getElementById('mobile-menu');


    if (!burgerBtn || !mobileMenu) {
        console.error("Не знайдено burger-btn або mobile-menu!");
        return;
    }

    // Відкриває меню
    burgerBtn.addEventListener('click', function() {
        mobileMenu.classList.add('open');
        mobileMenu.setAttribute('aria-hidden', 'false');
    });

    // Закриває меню
    // if (closeBtn) {
    //     closeBtn.addEventListener('click', function() {
    //         mobileMenu.classList.remove('open');
    //         mobileMenu.setAttribute('aria-hidden', 'true');
    //     });
    // }

    // Закриває меню, якщо клацнути поза ним (опціонально)
    document.addEventListener('click', function(e) {
        if (
            mobileMenu.classList.contains('open') &&
            !mobileMenu.contains(e.target) &&
            !burgerBtn.contains(e.target)
        ) {
            mobileMenu.classList.remove('open');
            mobileMenu.setAttribute('aria-hidden', 'true');
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
  const toggles = document.querySelectorAll('.dropdown-toggle');

  toggles.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const parent = btn.closest('.dropdown');

      // Закриваємо інші відкриті
      document.querySelectorAll('.dropdown.open').forEach(openItem => {
        if (openItem !== parent) openItem.classList.remove('open');
      });

      // Перемикаємо поточне
      const willOpen = !parent.classList.contains('open');
      parent.classList.toggle('open', willOpen);

      // ARIA для доступності
      btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const copyItems = document.querySelectorAll('.copy-text');
  const message = document.getElementById('copy-message');

  copyItems.forEach(item => {
    item.addEventListener('click', () => {
      const textToCopy = item.getAttribute('data-copy');

      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          message.classList.add('show');
          setTimeout(() => message.classList.remove('show'), 1500);
        })
        .catch(err => {
          console.error('Помилка копіювання:', err);
        });
    });
  });
});
