const API_URL = "http://127.0.0.1:8000";

const formulario = document.getElementById("loginForm");

formulario.addEventListener("submit", async function (event) {

    event.preventDefault();

    const recycler_id = document.getElementById("recycler_id").value;
    const password = document.getElementById("password").value;

    try {

        const respuesta = await fetch(`${API_URL}/auth/login`, {

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

            localStorage.setItem("recycler_id", datos.recycler_id);

            localStorage.setItem("full_name", datos.full_name);

            alert("Bienvenido " + datos.full_name);

            window.location.href = "usuarios.html";

        } else {

            alert(datos.detail);

        }

    } catch (error) {

        console.error(error);

        alert("No fue posible conectar con el servidor.");

    }

});