const API_URL = "http://127.0.0.1:8000/auth/login";

const form = document.getElementById("loginForm");
const mensaje = document.getElementById("mensaje");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const recycler_id = document.getElementById("recycler_id").value;
    const password = document.getElementById("password").value;

    try {

        const respuesta = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                recycler_id: recycler_id,
                password: password
            })

        });

        const datos = await respuesta.json();

        if (respuesta.ok) {

            localStorage.setItem("token", datos.token);

            mensaje.innerHTML = "Inicio de sesión correcto.";

            window.location.href = "/usuarios";

        } else {

            mensaje.innerHTML = datos.detail;

        }

    } catch (error) {

        mensaje.innerHTML = "No fue posible conectar con el servidor.";

    }

});