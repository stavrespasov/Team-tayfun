# Team Tayfun | Fightsport Gym

German-language, static frontend preview. Build the HTML with `python3 tools/build.py`. The generated pages, styles, scripts, and optimized media are in `dist/`.

Course metadata and the timetable transcribed from the supplied 30 June Instagram story are in `tools/build.py`. Course links pass the stable slot ID to `/probetraining/?kurs=…`. The preview form validates in the browser and does not transmit or store submissions. For production, confirm the timetable, clear the social imagery for reuse, and replace the legal placeholders with approved details and connect the trial flow to the backend.

Vercel serves the committed static output from `dist/`. The homepage uses the supplied black-and-white fight photo in its hero and the Team Tayfun training hall photo in the community section. The red hand-wrap image is an AI image study. Boxing, K1, and grappling use illustrated emblems in the card deck, course overview, and detail pages. The site retains the original crest, animated T, swipeable course cards, and day-switching training schedule. Motion can be paused and respects reduced-motion preferences.
