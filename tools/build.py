"""Render the German static site from shared page chrome and the supplied training timetable."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
INSTAGRAM = "https://www.instagram.com/fightsport_gym_team_tayfun/"
GYM_PHOTO_ALT = "Trainierende beim Sparring in der Halle von Team Tayfun"
FIGHT_PHOTO_ALT = "Boxer und Team nach einem Kampf, Schwarzweißaufnahme"
WRAPS_PHOTO_ALT = "Hände beim Anlegen roter Boxbandagen"
DAYS = ("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag")
SHORT_DAYS = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
COURSES = {
    "boxen": {
        "name": "Boxen", "image": "boxen", "alt": "Boxerin mit Handschuhen beim Pratzentraining am Ring",
        "credit": "KI-Bildstudie",
        "line": "Timing. Distanz. Präzision.",
        "intro": "Vom ersten Schritt bis zur Kombination. Im Mittelpunkt stehen Beinarbeit, Deckung und kontrollierte Abläufe.",
        "level": "Beim Gym erfragen", "kit": "Sportkleidung, Wasser, Bandagen",
        "details": "Nach dem Aufwärmen folgen Bewegungsabläufe, Arbeit an den Pratzen und Übungen mit Partnern. Der Umfang lässt sich an das jeweilige Niveau anpassen.",
    },
    "kickboxen": {
        "name": "Kickboxen K1", "image": "kickboxen", "alt": "Kickboxer beim Anlegen eines Schienbeinschoners",
        "credit": "KI-Bildstudie",
        "line": "Rhythmus. Bewegung. Kontrolle.",
        "intro": "Schläge und Tritte kommen in flüssigen Kombinationen zusammen. Du lernst, das Gleichgewicht und die Distanz zu halten.",
        "level": "Beim Gym erfragen", "kit": "Sportkleidung, Wasser, Bandagen",
        "details": "Technikübungen und Pratzenarbeit bauen aufeinander auf. Im Einstieg steht die kontrollierte Ausführung im Vordergrund.",
    },
    "grappling": {
        "name": "Ringen / Grappling", "image": "grappling", "alt": "Zwei Grappling-Trainierende im Gespräch auf der Matte",
        "credit": "KI-Bildstudie",
        "line": "Position. Balance. Bewegung.",
        "intro": "Auf der Matte lernst du, Positionen zu verstehen und dich kontrolliert mit einem Trainingspartner zu bewegen.",
        "level": "Beim Gym erfragen", "kit": "Sportkleidung ohne Reißverschlüsse, Wasser",
        "details": "Die Einheit kombiniert Bewegungsübungen, Partnerdrills und Positionsarbeit. Einsteiger können mit einfachen Abläufen beginnen.",
    },
}
COURSES.update({
    "kindertraining": {
        "name": "Kindertraining", "image": "team", "alt": "Trainingsfläche im Team-Tayfun-Gym",
        "line": "Für Kinder von 6 bis 12 Jahren.", "intro": "Das Kinder- und Jugendtraining im Trainingsplan richtet sich an 6- bis 12-Jährige.",
        "level": "6–12 Jahre", "kit": "Ausrüstung bitte beim Gym erfragen",
        "details": "Die Einheit dauert laut Trainingsplan 50 Minuten. Für Fragen zur ersten Teilnahme erreichst du das Gym auf Instagram.",
    },
    "sparring": {
        "name": "Sparring", "image": "team", "alt": "Sparring in der Trainingshalle von Team Tayfun",
        "line": "Partnertraining auf der Matte.", "intro": "Sparring steht mittwochs im Trainingsplan. Frag beim Gym nach den Voraussetzungen für die Teilnahme.",
        "level": "Beim Gym erfragen", "kit": "Schutzausrüstung mit dem Gym abklären",
        "details": "Das Team kann dir sagen, ob die Einheit zu deiner Erfahrung passt und welche Ausrüstung du mitbringen solltest.",
    },
    "personal-training": {
        "name": "Personal Training",
        "line": "Training nach Absprache.", "intro": "Der Trainingsplan zeigt von Montag bis Samstag ein Zeitfenster für Personal Training.",
        "level": "Nach Absprache", "kit": "Ausrüstung bitte beim Gym erfragen",
        "details": "Das Zeitfenster ist keine Terminbestätigung. Frag direkt beim Gym nach Verfügbarkeit und Konditionen.",
    },
})
WEEK = (
    (("17:00", "17:50", "kindertraining"), ("18:00", "19:00", "kickboxen"), ("19:15", "20:15", "boxen")),
    (("17:00", "17:50", "kindertraining"), ("18:00", "19:00", "grappling"), ("19:15", "20:15", "kickboxen")),
    (("17:00", "17:50", "kindertraining"), ("18:00", "19:00", "boxen"), ("19:15", "20:15", "sparring")),
    (("17:00", "17:50", "kindertraining"), ("18:00", "19:00", "kickboxen"), ("19:15", "20:15", "grappling")),
    (("18:00", "19:00", "boxen"),),
    (("11:00", "12:00", "boxen"),),
)
COURSE_TYPES = {"kindertraining": "6–12 Jahre", "sparring": "Sparring", "personal-training": "Nach Absprache"}
SLOTS = tuple(
    (f"{SHORT_DAYS[day].lower()}-{slug}-{start.replace(':', '')}", day, start, end, slug, COURSE_TYPES.get(slug, "Gruppentraining"))
    for day, group in enumerate(WEEK)
    for start, end, slug in (("08:30", "12:00", "personal-training"), *group)
)
SCHEDULE_NOTE = "Quelle: Instagram-Trainingsplan vom 30. Juni. In den Ferien und an Feiertagen können die Zeiten abweichen. Bitte bestätige deinen Termin direkt beim Gym."
ARROW = '<span class="arrow arrow--diagonal" aria-hidden="true"></span>'
DOWN = '<span class="arrow arrow--down" aria-hidden="true"></span>'
MARK = """<svg viewBox="0 0 320 320" aria-hidden="true" focusable="false">
  <path class="t-top" d="M31 56H296L268 111H12Z"/>
  <path class="t-mid" d="M126 111H205L169 184L96 201Z"/>
  <path class="t-base" d="M93 213L164 196L131 264H67Z"/>
</svg>"""
NAV = (("/training/", "Training"), ("/trainingsplan/", "Trainingsplan"), ("/team/", "Team"))


def link(label, href, cls="button button--ink", arrow=ARROW):
    return f'<a class="{cls}" href="{escape(href, quote=True)}">{label}{arrow}</a>'


def image(name, alt, cls="", eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="{cls}" src="/assets/{name}.webp" alt="{escape(alt, quote=True)}" {loading} decoding="async">'


def course_visual(course, cls="", *, decorative=False, eager=False):
    if "image" in course:
        return image(course["image"], "" if decorative else course["alt"], cls, eager)
    return f'<span class="course-art {cls}" aria-hidden="true">{MARK}</span>'


def brand():
    return f'''<a class="brand" href="/" aria-label="Team Tayfun, Startseite">
        <span class="brand-mark"><img src="/assets/team-crest.webp" alt="" width="48" height="48"></span>
        <span class="brand-name" aria-hidden="true">TEAM TAYFUN<small>FIGHTSPORT GYM</small></span>
    </a>'''


def nav_links(path):
    return "".join(
        f'<a href="{href}"' + (' aria-current="page"' if path.startswith(href) else '') + f'>{label}</a>'
        for href, label in NAV
    )


def header(path):
    tone = " header--hero" if path == "/" else ""
    return f'''<header class="header{tone}">
      <div class="header-inner">
        {brand()}
        <nav class="desktop-nav" aria-label="Hauptnavigation">{nav_links(path)}</nav>
        {link("Probetraining", "/probetraining/", "button button--header")}
        <details class="mobile-nav"><summary><span>Menü</span><i aria-hidden="true"></i></summary>
          <nav aria-label="Mobile Navigation">{nav_links(path)}
          <a href="/kontakt/">Kontakt</a>{link("Probetraining", "/probetraining/", "button button--paper")}</nav>
        </details>
      </div>
    </header>'''


def footer():
    return f'''<footer class="footer">
      <div class="wrap footer-top">
        {brand()}
        <nav aria-label="Weitere Seiten">
          <a href="/training/">Training</a><a href="/trainingsplan/">Trainingsplan</a><a href="/team/">Team</a>
          <a href="/probetraining/">Probetraining</a><a href="/kontakt/">Kontakt</a>
        </nav>
        {link("Instagram", INSTAGRAM, "text-link")}
      </div>
      <div class="wrap footer-word" aria-hidden="true">TAYFUN<span>®</span></div>
      <div class="wrap footer-base">
        <p>Designvorschau · Instagram-Fotos und KI-Bildstudien</p>
        <div><a href="/impressum/">Impressum</a><a href="/datenschutz/">Datenschutz</a></div>
      </div>
    </footer>'''


def page(path, title, description, main, body_class=""):
    html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#131318">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="{escape(description, quote=True)}">
<title>{title} | Team Tayfun</title>
<link rel="icon" href="/assets/team-crest.webp" type="image/webp">
<link rel="preload" href="/assets/display.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/campaign.css">
<script src="/assets/site.js" defer></script>
</head>
<body class="{body_class}">
<div class="reading-progress" aria-hidden="true"></div>
<a href="#inhalt" class="skip">Zum Inhalt springen</a>
{header(path)}
<main id="inhalt">{main}</main>
{footer()}
</body>
</html>
'''
    target = DIST / path.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def section_head(kicker, title, description):
    return f'''<div class="section-head">
       <div><p class="eyebrow"><span></span>{kicker}</p><h2 data-reveal>{title}</h2></div><p>{description}</p>
    </div>'''


def closing(title="Deine erste Runde.", description="Sieh dir an, was dich beim Probetraining erwartet."):
    return f'''<section class="closing" aria-label="Probetraining">
      <div class="closing-lines" aria-hidden="true"><i></i><i></i><i></i></div><div class="closing-mark">{MARK}</div>
      <div class="wrap closing-inner"><div><h2>{title}</h2><p>{description}</p></div>
      {link("Zum Probetraining", "/probetraining/", "button button--paper")}</div>
    </section>'''


def inner_intro(kicker, title, description):
    return f'''<section class="inner-intro"><div class="wrap">
      <p class="eyebrow"><span></span>{kicker}</p><h1>{title}</h1><p class="intro-copy">{description}</p>
    </div><div class="inner-lines" aria-hidden="true"><i></i><i></i><i></i></div></section>'''


def lineup(include_heading=True):
    rows = []
    images = []
    courses = list(COURSES.items())[:3] if include_heading else list(COURSES.items())
    for idx, (slug, course) in enumerate(courses):
        rows.append(f'''<a class="lineup-row" data-course-preview="{slug}" href="/training/{slug}/">
          <span class="lineup-index" aria-hidden="true">0{idx+1}</span>
          {course_visual(course, "lineup-thumb", decorative=True)}
          <span class="lineup-name">{course["name"]}<small>{course["line"]}</small></span>{ARROW}
        </a>''')
        active = " is-active" if idx == 0 else ""
        images.append(f'<div class="lineup-frame{active}" data-course-image="{slug}">{course_visual(course, decorative=True)}</div>')
    more = link("Alle Trainingsangebote", "/training/", "text-link lineup-more") if include_heading else ""
    heading = section_head("Training", "Finde deinen<br>Sport.", "Boxen, Kickboxen K1 und Ringen stehen im Wochenplan. Weitere Einheiten findest du in der Trainingsübersicht.") if include_heading else ""
    return f'''<section class="paper section" id="training"><div class="wrap">
      {heading}
      <div class="lineup" data-lineup><div class="lineup-media" aria-hidden="true">{"".join(images)}</div>
        <div class="lineup-list">{"".join(rows)}{more}</div>
      </div>
    </div></section>'''


def home():
    cards = "".join(f'''<a class="discipline-card" href="/training/{slug}/" data-reveal>
      {course_visual(course, decorative=True)}<div class="card-shade"></div>
      <div class="card-top"><span>{course["line"]}</span><span class="card-go">{ARROW}</span></div>
      <div class="card-bottom"><h3>{course["name"]}</h3><span>Training entdecken {ARROW}</span></div>
    </a>''' for slug, course in list(COURSES.items())[:3])
    days = "".join(f'<button type="button" data-home-day="{idx}" aria-pressed="{str(idx == 0).lower()}" aria-label="{day}">{SHORT_DAYS[idx]}</button>' for idx, day in enumerate(DAYS[:6]))
    sessions = "".join(f'''<a class="home-session" href="/probetraining/?kurs={slot}#anfrage" data-home-slot="{day}"{' hidden' if day else ''}>
      <span class="session-time">{start}<small>– {end}</small></span><span>{COURSES[slug]["name"]}<small>{kind}</small></span>{ARROW}
    </a>''' for slot, day, start, end, slug, kind in SLOTS if slug != "personal-training")
    return f'''<section class="hero campaign-hero" aria-labelledby="hero-title">
      <picture class="hero-media">
        <source media="(max-width: 650px) and (orientation: portrait)" srcset="/assets/hero-mobile.webp">
        {image("hero", FIGHT_PHOTO_ALT, eager=True)}
      </picture>
      <div class="hero-shade"></div><div class="hero-gridlines" aria-hidden="true"></div>
      <div class="hero-mark" aria-hidden="true">{MARK}</div>
      <div class="hero-content wrap">
        <p class="eyebrow hero-kicker"><span></span>FIGHTSPORT GYM</p>
        <h1 id="hero-title"><span><b>HIER BEGINNT</b></span><span><b>DEINE RUNDE.</b></span></h1>
        <div class="hero-actions">{link("Probetraining", "/probetraining/", "button button--red")}
        {link("Trainingsplan", "/trainingsplan/", "hero-link")}</div>
      </div>
      <div class="hero-bottom wrap"><a href="#training">Training entdecken {DOWN}</a>
        <button type="button" class="motion-toggle" data-motion-toggle aria-pressed="false" aria-label="Animationen pausieren"><span aria-hidden="true">Ⅱ</span><span data-motion-label>Bewegung pausieren</span></button></div>
    </section>
    <div class="fight-ticker" aria-label="Disziplin. Respekt. Zusammenhalt."><div class="ticker-track" aria-hidden="true">
      {''.join('<span>DISZIPLIN</span><i></i><span>RESPEKT</span><i></i><span>ZUSAMMENHALT</span><i></i>' for _ in range(4))}
    </div></div>
    <section class="spirit-section" id="spirit" aria-labelledby="spirit-title">
      <div class="wrap spirit-layout"><div class="spirit-copy"><p class="eyebrow"><span></span>Die Haltung hinter dem Training</p>
      <h2 id="spirit-title" data-reveal>ES BEGINNT<br>MIT <em>DIR.</em></h2>
      <p>Der Moment, in dem du dich entscheidest. Für mehr Fokus. Für die nächste Runde. Für dich.</p>
      {link("Dein Einstieg", "/probetraining/", "text-link")}</div>
      <figure class="bandage-feature" data-reveal>{image("campaign-wraps", WRAPS_PHOTO_ALT)}<figcaption>Vor der ersten Runde · KI-Bildstudie</figcaption>
        <span class="photo-corner" aria-hidden="true">{MARK}</span></figure>
      </div>
    </section>
    <section class="discipline-section section" id="training"><div class="wrap">
      <div class="section-head"><div><p class="eyebrow"><span></span>Finde deinen Sport</p><h2 data-reveal>VIELE WEGE.<br><em>DEINER.</em></h2></div><div class="discipline-intro"><p>Präzision im Stand. Kontrolle auf der Matte. Entdecke die Disziplin, die zu dir passt.</p>{link("Alle Trainingsangebote", "/training/", "text-link")}</div></div>
      <div class="discipline-deck">{cards}</div><div class="deck-footer"><span>KI-Bildstudien</span><span class="swipe-hint">Wischen & entdecken ↔</span></div>
      <div class="extra-training"><span>Auch im Trainingsplan</span><a href="/training/kindertraining/">Kindertraining {ARROW}</a><a href="/training/sparring/">Sparring {ARROW}</a><a href="/training/personal-training/">Personal Training {ARROW}</a></div>
    </div></section>
    <section class="storm-section" data-storm aria-labelledby="storm-title">
      <div class="storm-lines" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div class="wrap storm-layout"><div class="storm-copy"><p class="eyebrow"><span></span>TEAM TAYFUN</p><h2 id="storm-title" data-reveal>ENTFESSELE<br>DEINEN<br><em>TAYFUN.</em></h2><p>Fokus im Kopf. Feuer im Herzen.<br>Dein Team in der Ecke.</p>{link("Lerne das Team kennen", "/team/", "text-link")}</div>
      <div class="storm-object" aria-hidden="true"><div class="storm-orbit orbit-one"></div><div class="storm-orbit orbit-two"></div><div class="storm-orbit orbit-three"></div>
      <div class="t-sculpture"><div class="t-depth depth-back">{MARK}</div><div class="t-depth depth-mid">{MARK}</div><div class="t-face">{MARK}</div><div class="t-wire">{MARK}</div></div>
      <span class="storm-ground"></span></div></div>
    </section>
    <section class="training-week section"><div class="wrap week-layout"><div class="week-copy"><p class="eyebrow"><span></span>Deine Woche im Gym</p><h2 data-reveal>WENIGER<br>IRGENDWANN.<br><em>MEHR JETZT.</em></h2><p>Finde deine Einheit.<br>Der erste Schritt passt in deinen Kalender.</p>{link("Zum gesamten Trainingsplan", "/trainingsplan/", "text-link")}</div>
      <div class="week-board"><div class="home-day-bar" aria-label="Trainingstag">{days}</div><div class="week-board-heading"><span data-home-day-label>Montag</span><span>Abendtraining & Wochenendkurse</span></div><div class="home-sessions">{sessions}</div><p class="week-note" role="status" data-home-status>3 Einheiten am Montag</p><p class="week-source">Plan laut Instagram vom 30. Juni. Zeiten bitte beim Gym bestätigen. Personal Training nach Absprache.</p></div>
    </div></section>
    <section class="community-section" aria-labelledby="gym-title"><div class="wrap community-layout"><div class="community-photo"><figure>{image("team", GYM_PHOTO_ALT)}<figcaption>Instagram / Team Tayfun</figcaption></figure></div>
      <div class="community-copy"><p class="eyebrow"><span></span>Team Tayfun</p><h2 id="gym-title" data-reveal>ZUSAMMEN<br>AUF DER <em>MATTE.</em></h2><p>Ein Blick in die Trainingshalle und auf das Team hinter den Runden.</p>{link("Team & Gym entdecken", "/team/", "text-link")}</div></div></section>
    <section class="final-round" aria-labelledby="final-title"><div class="final-echo" aria-hidden="true">TAYFUN</div><div class="wrap"><p class="eyebrow"><span></span>Dein nächster Schritt</p><h2 id="final-title" data-reveal>BEREIT FÜR<br><em>DEINE RUNDE?</em></h2><a class="round-cta" href="/probetraining/"><span>Zum<br>Probetraining</span>{ARROW}</a></div></section>'''


def training():
    return inner_intro("Training", "Finde deinen Sport.", "Boxen, Kickboxen K1, Ringen und weitere Einheiten aus dem Trainingsplan von Team Tayfun.") + lineup(include_heading=False) + closing()


def course_page(slug, course):
    if "image" in course:
        credit = course.get("credit", "Instagram / Team Tayfun")
        visual = f'<figure>{course_visual(course, eager=True)}<figcaption>{credit}</figcaption></figure>'
    else:
        visual = f'<div class="course-hero-art">{course_visual(course)}</div>'
    return f'''<section class="course-hero">
       <div class="wrap course-hero-grid"><div>
       {link("Alle Disziplinen", "/training/", "back-link", '<span class="arrow arrow--back" aria-hidden="true"></span>')}
       <p class="eyebrow"><span></span>Training / Team Tayfun</p>
       <h1>{course["name"]}.</h1><p class="intro-copy">{course["intro"]}</p>
       {link("Passende Zeiten ansehen", f"/trainingsplan/?sport={slug}#kurse", "button button--red")}</div>
       {visual}</div>
    </section>
    <section class="paper section"><div class="wrap split">
      <div><p class="eyebrow"><span></span>Die Einheit</p><h2>{course["line"].replace(". ", ".<br>")}</h2></div>
      <div class="info-stack"><p>{course["details"]}</p>
        <dl><div><dt>Niveau</dt><dd>{course["level"]}</dd></div><div><dt>Für den Einstieg</dt><dd>{course["kit"]}</dd></div></dl>
        {link("Probetraining ansehen", f"/probetraining/?sport={slug}#anfrage", "text-link")}
      </div>
    </div></section>{closing()}'''


def schedule():
    day_buttons = "".join(
        f'<button type="button" class="day-button" data-day="{idx}" aria-pressed="{str(idx == 0).lower()}" aria-label="{day}"><span>{short}</span><small aria-hidden="true">{day}</small></button>'
        for idx, (day, short) in enumerate(zip(DAYS, SHORT_DAYS))
    )
    options = "".join(f'<option value="{slug}">{course["name"]}</option>' for slug, course in COURSES.items())
    rows = "".join(
        f'''<li class="schedule-row" data-slot-day="{day}" data-slot-sport="{slug}" data-slot-type="{level}"{' hidden' if day else ''}>
          <span class="schedule-time">{start}<small>bis {end}</small></span>
          <span class="schedule-course">{COURSES[slug]["name"]}<small>{level}</small></span>
          <a class="text-link" href="/probetraining/?kurs={slot}#anfrage">Kurs wählen<span class="sr-only">, {COURSES[slug]["name"]} am {DAYS[day]} um {start}</span>{ARROW}</a>
        </li>''' for slot, day, start, end, slug, level in SLOTS
    )
    return inner_intro("Training", "Trainingsplan.", "Wähle einen Tag und finde eine passende Einheit.") + f'''
    <section class="paper section schedule" id="kurse" data-schedule><div class="wrap">
      <div class="notice"><span></span>{SCHEDULE_NOTE}</div>
      <div class="day-bar" aria-label="Wochentag">{day_buttons}</div>
      <div class="schedule-filters">
        <label>Disziplin<select name="sport"><option value="">Alle Disziplinen</option>{options}</select></label>
        <label>Trainingsart<select name="art"><option value="">Alle Trainingsarten</option><option>Gruppentraining</option><option>6–12 Jahre</option><option>Sparring</option><option>Nach Absprache</option></select></label>
      </div>
      <h2 class="schedule-heading" data-schedule-heading>Montag</h2>
      <p class="schedule-status" data-schedule-status role="status">4 Einheiten</p>
      <ul class="schedule-list">{rows}</ul>
      <div class="schedule-empty" data-empty hidden><p>Für diese Auswahl sind keine Einheiten eingetragen.</p>
      <button class="text-link" type="button" data-clear>Gesamten Plan anzeigen {ARROW}</button></div>
      <noscript><p>Für weitere Tage und Filter aktiviere JavaScript.</p></noscript>
    </div></section>{closing()}'''


def team():
    return inner_intro("Team Tayfun", "Zusammen auf<br>der Matte.", "Ein Gym wird von den Menschen geprägt, die dort trainieren.") + f'''
    <figure class="team-feature">{image("team", "Team Tayfun beim Sparring in der Trainingshalle", eager=True)}<figcaption>Instagram / Team Tayfun</figcaption></figure>
    <section class="paper section"><div class="wrap split">
      <div><p class="eyebrow"><span></span>Das Gym</p><h2>Vor der<br>ersten Runde.</h2></div>
      <div class="info-stack"><p>Wer leitet die Einheit? Wie sieht der Trainingsraum aus? Was solltest du für deinen ersten Besuch mitbringen?</p>
      <p>Auf dem Instagram-Kanal findest du weitere Einblicke ins Training und erreichst das Team direkt.</p>
      {link("Team Tayfun auf Instagram", INSTAGRAM, "text-link")}</div>
    </div></section>
    <section class="paper team-archive" aria-label="Team Tayfun auf Instagram"><div class="wrap archive-grid">
      <figure>{image("team-shirt", "Team-Tayfun-Wappen auf einem Trainingsshirt")}<figcaption>Teamshirt / Instagram</figcaption></figure>
      <figure>{image("hero", FIGHT_PHOTO_ALT)}<figcaption>Kampfabend / Instagram</figcaption></figure>
    </div></section>{closing()}'''


def trial():
    options = "".join(
        f'<optgroup label="{day}">' + "".join(
            f'<option value="{slot}" data-sport="{slug}">{day} · {start} · {COURSES[slug]["name"]} ({level})</option>'
            for slot, d, start, end, slug, level in SLOTS if d == idx
        ) + '</optgroup>' for idx, day in enumerate(DAYS) if any(slot[1] == idx for slot in SLOTS)
    )
    return inner_intro("Dein erster Besuch", "Probetraining.", "Wähle eine Einheit, sieh dir den Ablauf an und teste die Anfrage in der Vorschau.") + f'''
    <section class="paper section trial" id="anfrage"><div class="wrap trial-grid">
      <div><p class="eyebrow"><span></span>Vor deinem Besuch</p><h2>So läuft’s ab.</h2>
      <ol class="steps">
        <li><div><h3>Einheit aussuchen</h3><p>Wähle im Trainingsplan eine passende Disziplin und Trainingszeit.</p></div></li>
        <li><div><h3>Tasche packen</h3><p>Bequeme Sportkleidung und Wasser sind ein guter Ausgangspunkt. Frag das Gym nach der Ausrüstung für deinen Kurs.</p></div></li>
        <li><div><h3>Termin bestätigen lassen</h3><p>Ort, Uhrzeit und Konditionen klärst du für einen echten Besuch direkt mit dem Gym.</p></div></li>
      </ol>
      {link("Zum Trainingsplan", "/trainingsplan/", "text-link")}</div>
      <div class="trial-form-box">
        <div class="notice"><span></span>Demoformular. Es werden keine Daten versendet oder gespeichert.</div>
        <h2>Anfrage testen.</h2>
        <form data-trial autocomplete="off" novalidate>
          <fieldset disabled><legend class="sr-only">Testanfrage</legend>
            <label>Trainingstermin<select name="kurs" required aria-describedby="kurs-fehler"><option value="">Termin auswählen</option>{options}</select><span class="field-error" id="kurs-fehler" hidden></span></label>
            <label>Name <span>(Testdaten)</span><input name="name" type="text" placeholder="Erika Muster" required maxlength="100" aria-describedby="name-fehler"><span class="field-error" id="name-fehler" hidden></span></label>
            <label>E-Mail <span>(Testdaten)</span><input name="email" type="email" placeholder="erika@example.com" required maxlength="160" aria-describedby="email-fehler"><span class="field-error" id="email-fehler" hidden></span></label>
            <button type="submit" class="button button--red">Demo-Anfrage testen {ARROW}</button>
          </fieldset>
        </form>
        <noscript><p>Aktiviere JavaScript, um die Testanfrage auszuprobieren.</p></noscript>
        <div class="form-result" data-form-result role="status" tabindex="-1" hidden></div>
      </div>
    </div></section>
    <section class="paper faq"><div class="wrap split">
      <div><p class="eyebrow"><span></span>Vor dem Training</p><h2>Häufige Fragen.</h2></div>
      <div class="faq-list">
        <details><summary>Kann ich ohne Erfahrung anfangen?</summary><p>Frag beim Gym nach einem passenden Kurs für deinen ersten Besuch und nach der Ausrüstung, die du brauchst.</p></details>
        <details><summary>Was kostet das Probetraining?</summary><p>Die Konditionen sind in dieser Vorschau noch offen. Frage direkt beim Gym nach dem aktuellen Preis.</p></details>
        <details><summary>Wo findet das Training statt?</summary><p>Die Adresse wird nach Bestätigung ergänzt. Für eine aktuelle Auskunft erreichst du das Gym auf Instagram.</p></details>
      </div>
    </div></section>'''


def contact():
    return inner_intro("Team Tayfun", "Kontakt.", "Fragen zu Kursen, Anfahrt oder zum ersten Besuch? Hier erreichst du das Gym.") + f'''
    <section class="paper section"><div class="wrap split">
      <div><p class="eyebrow"><span></span>Direkt zum Team</p><h2>Schreib uns.</h2></div>
      <div class="info-stack"><h3>Instagram</h3><p>@fightsport_gym_team_tayfun</p>
      {link("Instagram öffnen", INSTAGRAM, "button button--ink")}
      <dl><div><dt>Standort</dt><dd>Adresse und Anfahrt folgen nach Bestätigung.</dd></div>
      <div><dt>Trainingszeiten</dt><dd><a href="/trainingsplan/">Zum Trainingsplan</a></dd></div></dl></div>
    </div></section>'''


def legal(kicker, title, copy):
    return inner_intro(kicker, title, "Informationen zur Frontend-Vorschau.") + f'''
    <section class="paper section"><div class="wrap split"><h2>Zur Vorschau.</h2>
    <div class="info-stack"><p>{copy}</p>{link("Zum Kontakt", "/kontakt/", "text-link")}</div></div></section>'''


page("/", "Fightsport Gym", "Team Tayfun: Training, Trainingsplan und Probetraining.", home(), "home")
page("/training/", "Training", "Entdecke die Disziplinen im Frontend-Entwurf für Team Tayfun.", training())
for slug, course in COURSES.items():
    page(f"/training/{slug}/", course["name"], course["intro"], course_page(slug, course))
page("/trainingsplan/", "Trainingsplan", "Trainingszeiten und Disziplinen laut Instagram-Trainingsplan.", schedule())
page("/team/", "Team & Gym", "Einblick in die Bildwelt von Team Tayfun.", team())
page("/probetraining/", "Probetraining", "Ablauf, Checkliste und Testanfrage für das Probetraining.", trial())
page("/kontakt/", "Kontakt", "Kontakt zu Team Tayfun.", contact())
page("/impressum/", "Impressum", "Hinweise zur Frontend-Vorschau.", legal("Rechtliches", "Impressum.", "Die Angaben zum Betreiber des Gyms werden für die öffentliche Website ergänzt."))
page("/datenschutz/", "Datenschutz", "Hinweise zum Datenschutz der Frontend-Vorschau.", legal("Rechtliches", "Datenschutz.", "Das Testformular verarbeitet Eingaben im Browser. Die Website sendet und speichert die Formulardaten nicht. Links zu Instagram führen zu einem externen Angebot. Die vollständigen Datenschutzhinweise folgen für die öffentliche Website."))
