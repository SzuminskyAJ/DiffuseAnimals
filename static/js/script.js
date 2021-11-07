window.onload = () => {
    //alert('Tu pue');
};

function onSubmit(e) {
  const form = document.getElementById('f_form');
  const values = new FormData(form);
  const vals = Object.fromEntries(values);
  const button = document.getElementById('submit-button');

  button.disabled = true;
  button.value = "Processing…";

  const keys = ['diffusionA', 'diffusionB', 'tau', 'k', 's', 'L', 'steps', 'noise', 'size', 'Kill', 'Feed']
  for (key of keys) {
    if (vals[key] !== undefined) {
      vals[key] = Number(vals[key]); // Convert to numbers
    }
  }

  const json = JSON.stringify(vals);
  fetch('/simulation.gif', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: json
  }).then(resp => {
    if (!resp.ok) throw new Error('Could not process');
    return resp.blob();
  }).then(blob => {
    document.getElementById('output').src = URL.createObjectURL(blob);
    button.disabled = false;
    button.value = "Generate";
  }).catch(e => {
    button.disabled = true;
    button.value = "Generate";
    alert(e);
  });
}
