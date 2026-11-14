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
  type.addEventListener('change', () => render(true));
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

// Keep optional motion under one control, including operating-system preferences.
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const motionToggle = document.querySelector('[data-motion-toggle]');
let motionPaused = reducedMotion.matches;
try {
  motionPaused = reducedMotion.matches || sessionStorage.getItem('tayfun-motion') === 'paused';
} catch (_) {
  // The page also works when browser storage is unavailable.
}
const setMotion = paused => {
  motionPaused = paused;
  document.documentElement.dataset.motion = paused ? 'paused' : 'active';
  if (motionToggle) {
    motionToggle.setAttribute('aria-pressed', String(paused));
    motionToggle.setAttribute('aria-label', paused ? 'Animationen abspielen' : 'Animationen pausieren');
    motionToggle.querySelector('[data-motion-label]').textContent = paused ? 'Bewegung abspielen' : 'Bewegung pausieren';
    motionToggle.firstElementChild.textContent = paused ? '▷' : 'Ⅱ';
  }
  for (const animation of document.getAnimations()) {
    if (paused && animation.effect?.getTiming().iterations !== Infinity) animation.finish();
    else if (paused) animation.pause();
    else if (animation.playState === 'paused') animation.play();
  }
};
setMotion(motionPaused);
motionToggle?.addEventListener('click', () => {
  setMotion(!motionPaused);
  try {
    sessionStorage.setItem('tayfun-motion', motionPaused ? 'paused' : 'active');
  } catch (_) { /* Motion remains controllable without storage. */ }
});
reducedMotion.addEventListener('change', event => setMotion(event.matches));

const heroScene = document.querySelector('.campaign-hero');
const stormScene = document.querySelector('[data-storm]');
let scrollFrame = 0;
const drawScroll = () => {
  scrollFrame = 0;
  const pageTravel = document.documentElement.scrollHeight - innerHeight;
  document.documentElement.style.setProperty('--read', pageTravel > 0 ? scrollY / pageTravel : 0);
  if (motionPaused) return;
  if (heroScene && scrollY < heroScene.offsetHeight) {
    heroScene.style.setProperty('--hero-drift', `${Math.min(scrollY * .16, 110)}px`);
  }
  if (stormScene) {
    const bounds = stormScene.getBoundingClientRect();
    if (bounds.top < innerHeight && bounds.bottom > 0) {
      stormScene.style.setProperty('--storm-shift', `${(innerHeight / 2 - bounds.top) * .1}px`);
    }
  }
};
const queueScroll = () => {
  if (!scrollFrame) scrollFrame = requestAnimationFrame(drawScroll);
};
addEventListener('scroll', queueScroll, { passive: true });
addEventListener('resize', queueScroll);
queueScroll();

if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      if (!motionPaused) {
        const isHeading = /^H[1-6]$/.test(entry.target.tagName);
        entry.target.animate([
          { opacity: .2, transform: 'translateY(45px)', clipPath: isHeading ? 'inset(0 0 90% 0)' : 'inset(0)' },
          { opacity: 1, transform: 'translateY(0)', clipPath: 'inset(0)' },
        ], { duration: 1000, easing: 'cubic-bezier(.16,1,.3,1)' });
      }
      revealObserver.unobserve(entry.target);
    }
  }, { threshold: .12 });
  document.querySelectorAll('[data-reveal]').forEach(element => revealObserver.observe(element));
}

const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
if (stormScene && finePointer.matches) {
  stormScene.addEventListener('pointermove', event => {
    if (motionPaused) return;
    const rect = stormScene.getBoundingClientRect();
    stormScene.style.setProperty('--tilt-x', `${(event.clientX / innerWidth - .5) * 20}deg`);
    stormScene.style.setProperty('--tilt-y', `${((event.clientY - rect.top) / rect.height - .5) * -14}deg`);
  }, { passive: true });
  stormScene.addEventListener('pointerleave', () => {
    stormScene.style.setProperty('--tilt-x', '0deg');
    stormScene.style.setProperty('--tilt-y', '0deg');
  });
}

const homeDays = [...document.querySelectorAll('[data-home-day]')];
if (homeDays.length) {
  const homeSlots = [...document.querySelectorAll('[data-home-slot]')];
  const dayLabel = document.querySelector('[data-home-day-label]');
  const homeStatus = document.querySelector('[data-home-status]');
  for (const button of homeDays) {
    button.addEventListener('click', () => {
      const selectedDay = button.dataset.homeDay;
      let visibleCount = 0;
      for (const day of homeDays) day.setAttribute('aria-pressed', String(day === button));
      for (const slot of homeSlots) {
        slot.hidden = slot.dataset.homeSlot !== selectedDay;
        if (!slot.hidden) visibleCount += 1;
      }
      dayLabel.textContent = button.getAttribute('aria-label');
      homeStatus.textContent = `${visibleCount} ${visibleCount === 1 ? 'Einheit' : 'Einheiten'} am ${dayLabel.textContent}`;
    });
  }
}
