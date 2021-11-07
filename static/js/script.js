window.onload = () => {
    //alert('Tu pue');
};

function onSubmit(e) {
  const form = document.getElementById('f_form');
  const values = new FormData(form);
  const vals = Object.fromEntries(values);
  vals.Model = 'FitzHugh-Nagumo';
  vals.InitialModel = 'Random';
  vals.noise = 0.05;
  vals.size = 100;

  const keys = ['diffusionA', 'diffusionB', 'tau', 'k', 's', 'L', 'steps', 'noise', 'size']
  for (key of keys) {
    vals[key] = Number(vals[key]); // Convert to numbers
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
  }).catch(e => {
    alert(e);
  });
}
