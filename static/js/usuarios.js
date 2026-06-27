const API_URL = "http://127.0.0.1:8000/recyclers";
const token = localStorage.getItem("token");

const tabla = document.getElementById("tablaRecicladores");
const formulario = document.getElementById("formRecycler");

let modoEdicion = false;

function obtenerHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    };
}

function crearFila(reciclador) {
    return `
        <tr>
            <td>${reciclador.recycler_id}</td>
            <td>${reciclador.full_name}</td>
            <td>${reciclador.id_number}</td>
            <td>${reciclador.email}</td>
            <td>${reciclador.phone}</td>
            <td>${reciclador.district}</td>
            <td>${reciclador.is_active ? "Si" : "No"}</td>
            <td>
                <button type="button" onclick="editarReciclador('${reciclador.recycler_id}')">
                    Editar
                </button>
                <button type="button" onclick="eliminarReciclador('${reciclador.recycler_id}')">
                    Eliminar
                </button>
            </td>
        </tr>
    `;
}

async function cargarRecicladores() {
    try {
        const respuesta = await fetch(API_URL, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Error cargando recicladores.");
            return;
        }

        const recicladores = await respuesta.json();

        tabla.innerHTML = "";
        recicladores.forEach(reciclador => {
            tabla.innerHTML += crearFila(reciclador);
        });
    } catch (error) {
        console.log(error);
        alert("Error cargando recicladores.");
    }
}

formulario.addEventListener("submit", async function (e) {
    e.preventDefault();

    const reciclador = {
        recycler_id: document.getElementById("recycler_id").value,
        full_name: document.getElementById("full_name").value,
        id_number: document.getElementById("id_number").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        district: document.getElementById("district").value,
        registration_date: document.getElementById("registration_date").value,
        is_active: true
    };

    let url = API_URL;
    let metodo = "POST";

    if (modoEdicion) {
        url = API_URL + "/" + reciclador.recycler_id;
        metodo = "PUT";
    }

    try {
        const respuesta = await fetch(url, {
            method: metodo,
            headers: obtenerHeaders(),
            body: JSON.stringify(reciclador)
        });

        if (!respuesta.ok) {
            alert("No fue posible guardar el reciclador.");
            return;
        }

        if (modoEdicion) {
            alert("Reciclador actualizado correctamente.");
        } else {
            alert("Reciclador registrado correctamente.");
        }

        limpiarFormulario();
        cargarRecicladores();
    } catch (error) {
        console.log(error);
        alert("No fue posible guardar el reciclador.");
    }
});

async function editarReciclador(id) {
    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Reciclador no encontrado.");
            return;
        }

        const reciclador = await respuesta.json();

        document.getElementById("recycler_id").value = reciclador.recycler_id;
        document.getElementById("full_name").value = reciclador.full_name;
        document.getElementById("id_number").value = reciclador.id_number;
        document.getElementById("email").value = reciclador.email;
        document.getElementById("phone").value = reciclador.phone;
        document.getElementById("district").value = reciclador.district;
        document.getElementById("registration_date").value = reciclador.registration_date;

        modoEdicion = true;
        document.getElementById("recycler_id").disabled = true;
    } catch (error) {
        console.log(error);
        alert("No fue posible cargar el reciclador.");
    }
}

async function eliminarReciclador(id) {
    if (!confirm("Eliminar reciclador?")) {
        return;
    }

    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            method: "DELETE",
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("No fue posible eliminar el reciclador.");
            return;
        }

        alert("Reciclador eliminado correctamente.");
        cargarRecicladores();
    } catch (error) {
        console.log(error);
        alert("No fue posible eliminar el reciclador.");
    }
}

async function buscarReciclador() {
    const id = document.getElementById("buscarID").value;

    if (id.trim() === "") {
        alert("Ingrese el ID del reciclador.");
        return;
    }

    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Reciclador no encontrado.");
            return;
        }

        const reciclador = await respuesta.json();
        tabla.innerHTML = crearFila(reciclador);
    } catch (error) {
        console.log(error);
        alert("No fue posible buscar el reciclador.");
    }
}

function limpiarFormulario() {
    formulario.reset();
    modoEdicion = false;
    document.getElementById("recycler_id").disabled = false;
}

cargarRecicladores();
