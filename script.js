/* -------------------------------------------------------------
 *  script.js  –  front‑end logic for Charity‑Match
 *
 *  1.  Change BACKEND_BASE to where your Flask server is running.
 *      • Local dev:  'http://127.0.0.1:5000'
 *      • Codespaces: 'https://<codespace‑id>-5000.app.github.dev'
 *      • Render/Heroku/etc.: your deployed domain
 *
 *  2.  Ensure index.html uses the same field names:
 *      cause, groups, region, faith, support
 * ------------------------------------------------------------ */
const BACKEND_BASE = 'http://127.0.0.1:5000';   //  ← EDIT ME!

document.addEventListener('DOMContentLoaded', () => {
  const submitBtn  = document.getElementById('submit-btn');
  const resultsBox = document.getElementById('results-container');
  const resultsEl  = document.getElementById('results');

  /* ---------- helpers to collect form data ---------------- */
  const getRadio = name =>
    (document.querySelector(`input[name="${name}"]:checked`) || {}).value || null;

  const getChecks = name =>
    Array.from(document.querySelectorAll(`input[name="${name}"]:checked`))
         .map(el => el.value);

  /* ---------- main click handler -------------------------- */
  submitBtn.addEventListener('click', () => {
    /* 1. Gather answers from the form */
    const answers = {
      cause:   getRadio('cause'),
      groups:  getChecks('groups'),
      region:  getRadio('region'),
      faith:   getRadio('faith'),
      support: getRadio('support')
    };

    /* 2. Show the captured answers (optional) */
    resultsEl.textContent = 'Your answers:\n' +
                            JSON.stringify(answers, null, 2);
    resultsBox.style.display = 'block';

    /* 3. POST answers to the backend */
    fetch(`${BACKEND_BASE}/api/charity-match`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers })
    })
      .then(res => {
        if (!res.ok) throw new Error(`Backend returned ${res.status}`);
        return res.json();
      })
      .then(data => {
        /* 4. Display Llama’s reply */
        resultsEl.textContent +=
          '\n\nLlama says:\n' + JSON.stringify(data, null, 2);
      })
      .catch(err => {
        console.error(err);
        resultsEl.textContent += '\n\n⚠️  Error calling backend.';
      });
  });
});
