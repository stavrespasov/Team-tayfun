'use strict';

const parameters = new URLSearchParams(window.location.search);
const menu = document.querySelector('.mobile-nav');

if (menu) {
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
  document.addEventListener('pointerdown', event => {
    if (menu.open && !menu.contains(event.target)) menu.open = false;
  });
}

const lineup = document.querySelector('[data-lineup]');
if (lineup) {
  const frames = [...lineup.querySelectorAll('[data-course-image]')];
  for (const row of lineup.querySelectorAll('[data-course-preview]')) {
    const showImage = () => {
      for (const frame of frames) {
        frame.classList.toggle('is-active', frame.dataset.courseImage === row.dataset.coursePreview);
      }
    };
    row.addEventListener('pointerenter', showImage);
    row.addEventListener('focus', showImage);
  }
}

const scene = document.querySelector('[data-ring-cut]');
const motion = window.matchMedia('(prefers-reduced-motion: no-preference)');
const desktop = window.matchMedia('(min-width: 801px)');
if (scene) {
  let frame = 0;
  const draw = () => {
    frame = 0;
    if (!motion.matches) {
      scene.removeAttribute('data-motion');
      scene.style.removeProperty('--cut-progress');
      return;
    }
    const rect = scene.getBoundingClientRect();
    const travel = window.innerHeight * (desktop.matches ? 0.55 : 0.42);
    const progress = Math.max(0, Math.min(1, (window.innerHeight - rect.top) / travel));
    scene.style.setProperty('--cut-progress', progress.toFixed(3));
    scene.dataset.motion = '';
  };
  const queueDraw = () => {
    if (!frame) frame = requestAnimationFrame(draw);
  };
  addEventListener('scroll', queueDraw, { passive: true });
  addEventListener('resize', queueDraw);
  motion.addEventListener('change', queueDraw);
  queueDraw();
}

if (motion.matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      if (motion.matches && typeof entry.target.animate === 'function') {
        entry.target.animate(
          [{ transform: 'translateY(18px)', opacity: 0.65 }, { transform: 'none', opacity: 1 }],
          { duration: 560, easing: 'cubic-bezier(.2,.75,.25,1)' },
        );
      }
      observer.unobserve(entry.target);
    }
  }, { threshold: 0.18 });
  for (const target of document.querySelectorAll('[data-reveal]')) observer.observe(target);
}

const schedule = document.querySelector('[data-schedule]');
if (schedule) {
  const days = [...schedule.querySelectorAll('[data-day]')];
  const rows = [...schedule.querySelectorAll('[data-slot-day]')];
  const sport = schedule.querySelector('[name="sport"]');
  const type = schedule.querySelector('[name="art"]');
  const heading = schedule.querySelector('[data-schedule-heading]');
  const status = schedule.querySelector('[data-schedule-status]');
  const empty = schedule.querySelector('[data-empty]');
  const validDay = value => days.find(button => button.dataset.day === value)?.dataset.day;
  let activeDay = validDay(parameters.get('tag'))
    ?? rows.find(row => row.dataset.slotSport === parameters.get('sport'))?.dataset.slotDay
    ?? '0';

  if ([...sport.options].some(option => option.value === parameters.get('sport'))) {
    sport.value = parameters.get('sport');
  }
  if ([...type.options].some(option => option.value === parameters.get('art'))) {
    type.value = parameters.get('art');
  }

  const render = (syncUrl = false) => {
    for (const day of days) day.setAttribute('aria-pressed', String(day.dataset.day === activeDay));
    heading.textContent = days[Number(activeDay)].getAttribute('aria-label');

    let count = 0;
    for (const row of rows) {
      const matches = row.dataset.slotDay === activeDay
        && (!sport.value || row.dataset.slotSport === sport.value)
        && (!type.value || row.dataset.slotType === type.value);
      row.hidden = !matches;
      if (matches) count += 1;
    }
    status.textContent = count === 1 ? '1 Einheit' : `${count} Einheiten`;
    empty.hidden = count > 0;

    if (syncUrl) {
      const url = new URL(location.href);
      url.searchParams.set('tag', activeDay);
      for (const input of [sport, type]) {
        if (input.value) url.searchParams.set(input.name, input.value);
        else url.searchParams.delete(input.name);
      }
      history.replaceState(null, '', url);
    }
  };

  for (const day of days) {
    day.addEventListener('click', () => {
      activeDay = day.dataset.day;
      render(true);
    });
  }
  sport.addEventListener('change', () => render(true));
  level.addEventListener('change', () => render(true));
  schedule.querySelector('[data-clear]').addEventListener('click', () => {
    activeDay = '0';
    sport.value = '';
    type.value = '';
    render(true);
    days[0].focus();
  });
  render();
}

const trial = document.querySelector('[data-trial]');
if (trial) {
  const fieldset = trial.querySelector('fieldset');
  const course = trial.elements.kurs;
  const result = document.querySelector('[data-form-result]');
  const options = [...course.options];
  const selected = options.find(option => option.value === parameters.get('kurs'))
    ?? options.find(option => option.dataset.sport === parameters.get('sport'));

  const fields = [course, trial.elements.name, trial.elements.email];
  const messages = {
    kurs: 'Wähle einen Trainingstermin aus.',
    name: 'Gib einen Namen für den Test ein.',
    email: 'Gib eine gültige E-Mail-Adresse für den Test ein.',
  };
  const showError = (field, message = '') => {
    const hint = document.getElementById(field.getAttribute('aria-describedby'));
    field.setAttribute('aria-invalid', String(Boolean(message)));
    hint.textContent = message;
    hint.hidden = !message;
  };
  for (const field of fields) {
    field.addEventListener('input', () => showError(field));
  }
  if (selected) course.value = selected.value;
  trial.addEventListener('submit', event => {
    event.preventDefault();
    const invalid = fields.filter(field => !field.validity.valid || !field.value.trim());
    for (const field of fields) showError(field, invalid.includes(field) ? messages[field.name] : '');
    if (invalid.length) {
      invalid[0].focus();
      return;
    }

    const summary = document.createElement('strong');
    summary.textContent = 'Demo erfolgreich abgeschlossen.';
    const details = document.createElement('p');
    details.textContent = `Ausgewählt: ${course.selectedOptions[0].textContent}. Es wurde keine Anfrage versendet.`;
    const reset = document.createElement('button');
    reset.type = 'button';
    reset.className = 'text-link';
    reset.textContent = 'Erneut testen';
    reset.addEventListener('click', () => {
      trial.reset();
      if (selected) course.value = selected.value;
      result.hidden = true;
      fieldset.disabled = false;
      course.focus();
    });

    result.replaceChildren(summary, details, reset);
    result.hidden = false;
    fieldset.disabled = true;
    trial.elements.name.value = '';
    trial.elements.email.value = '';
    result.focus();
  });
  fieldset.disabled = false;
}
