window.onload = () => {
    //alert('Tu pue');
};

function onSubmit(e) {
  e.preventDefault();
  const form = document.getElementById('f_form');
  const values = new FormData(form);
  const json = JSON.stringify(Object.fromEntries(values));

  fetch('/simulation.gif', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: json
  }).then(resp => {
    if (!resp.ok) throw new Error('Could not process');
    return resp.blob();
  }).then(blob => {
    myImage.src = URL.createObjectURL(blob);
  }).catch(e => {
    alert(e);
  });
}
