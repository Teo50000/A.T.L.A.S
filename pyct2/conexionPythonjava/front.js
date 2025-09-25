document.getElementById("ejct").addEventListener("click", saldPy)
let data  = ""
async function saldPy(){
    let nombre = document.getElementById("nmbre").value
    const envio = await fetch('http://localhost:3000/echo', {
    method: 'POST',                        // Usamos POST para enviar datos
    headers: { 'Content-Type': 'application/json' }, // Indicamos que enviamos JSON
    body: JSON.stringify({ nombre })     // Convertimos el mensaje a JSON y lo mandamos
    });

    data = await envio.json();
    document.getElementById("sld").innerHTML = data.respF + " y del front"
}