/* script.js ---------------------------------------------------- */
/* Because the front‑end is served by Flask, same‑origin requests
 * work; we just hit '/api/charity-match'.                       */

 document.addEventListener('DOMContentLoaded', () => {
  const submitBtn  = document.getElementById('submit-btn');
  const resultsBox = document.getElementById('results-container');
  const resultsEl  = document.getElementById('results');

  const getRadio = n =>
    (document.querySelector(`input[name="${n}"]:checked`) || {}).value || null;

  const getChecks = n =>
    Array.from(document.querySelectorAll(`input[name="${n}"]:checked`))
         .map(el => el.value);

  submitBtn.addEventListener('click', () => {
    const answers = {
      cause:   getRadio('cause'),
      groups:  getChecks('groups'),
      region:  getRadio('region'),
      faith:   getRadio('faith'),
      support: getRadio('support')
    };

    resultsEl.textContent = 'Your answers:\n' +
                            JSON.stringify(answers, null, 2);
    resultsBox.style.display = 'block';

    fetch('/api/charity-match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers })
    })
      .then(r => { if (!r.ok) throw new Error(r.statusText); return r.json(); })
      .then(data => {
        resultsEl.textContent +=
          '\n\nLlama says:\n' + JSON.stringify(data, null, 2);
      })
      .catch(err => {
        console.error(err);
        resultsEl.textContent += '\n\n⚠️  Error calling backend.';
      });
  });
});
