const API_URL = "http://127.0.0.1:8000/collection-points";
const token = localStorage.getItem("token");

const tabla = document.getElementById("tablaCentros");
const formulario = document.getElementById("formCentro");

let modoEdicion = false;

function obtenerHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    };
}

function crearFila(centro) {
    return `
        <tr>
            <td>${centro.point_id}</td>
            <td>${centro.name}</td>
            <td>${centro.location}</td>
            <td>${centro.district}</td>
            <td>${centro.accepted_materials}</td>
            <td>${centro.capacity_kg}</td>
            <td>${centro.current_load_kg}</td>
            <td>${centro.is_active ? "Sí" : "No"}</td>
            <td>
                <button type="button" onclick="editarCentro('${centro.point_id}')">
                    Editar
                </button>
                <button type="button" onclick="eliminarCentro('${centro.point_id}')">
                    Eliminar
                </button>
            </td>
        </tr>
    `;
}

async function cargarCentros() {
    try {
        const respuesta = await fetch(API_URL, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Error cargando centros.");
            return;
        }

        const centros = await respuesta.json();

        tabla.innerHTML = "";
        centros.forEach(centro => {
            tabla.innerHTML += crearFila(centro);
        });

    } catch (error) {
        console.log(error);
        alert("Error cargando centros.");
    }
}

formulario.addEventListener("submit", async function(e) {
    e.preventDefault();

    const centro = {
        point_id: document.getElementById("point_id").value,
        name: document.getElementById("name").value,
        location: document.getElementById("location").value,
        district: document.getElementById("district").value,
        accepted_materials: document.getElementById("accepted_materials").value,
        capacity_kg: parseFloat(document.getElementById("capacity_kg").value),
        current_load_kg: 0,
        is_active: true
    };

    let url = API_URL + "/";
    let metodo = "POST";

    if (modoEdicion) {
        url = API_URL + "/" + centro.point_id;
        metodo = "PUT";
    }

    try {
        const respuesta = await fetch(url, {
            method: metodo,
            headers: obtenerHeaders(),
            body: JSON.stringify(centro)
        });

        if (!respuesta.ok) {
            const error = await respuesta.json();
            alert(error.detail);
            return;
        }

        if (modoEdicion) {
            alert("Centro actualizado correctamente.");
        } else {
            alert("Centro registrado correctamente.");
        }

        limpiarFormulario();
        cargarCentros();

    } catch (error) {
        console.log(error);
        alert("No fue posible guardar el centro.");
    }
});

async function editarCentro(id) {
    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Centro no encontrado.");
            return;
        }

        const centro = await respuesta.json();

        document.getElementById("point_id").value = centro.point_id;
        document.getElementById("name").value = centro.name;
        document.getElementById("location").value = centro.location;
        document.getElementById("district").value = centro.district;
        document.getElementById("accepted_materials").value = centro.accepted_materials;
        document.getElementById("capacity_kg").value = centro.capacity_kg;

        modoEdicion = true;
        document.getElementById("point_id").disabled = true;

    } catch (error) {
        console.log(error);
        alert("No fue posible cargar el centro.");
    }
}

async function eliminarCentro(id) {
    if (!confirm("¿Eliminar centro?")) {
        return;
    }

    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            method: "DELETE",
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("No fue posible eliminar el centro.");
            return;
        }

        alert("Centro eliminado correctamente.");
        cargarCentros();

    } catch (error) {
        console.log(error);
        alert("No fue posible eliminar el centro.");
    }
}

async function buscarCentro() {
    const id = document.getElementById("buscarID").value;

    if (id.trim() === "") {
        alert("Ingrese el ID del centro.");
        return;
    }

    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Centro no encontrado.");
            return;
        }

        const centro = await respuesta.json();
        tabla.innerHTML = crearFila(centro);

    } catch (error) {
        console.log(error);
        alert("No fue posible buscar el centro.");
    }
}

function limpiarFormulario() {
    formulario.reset();
    modoEdicion = false;
    document.getElementById("point_id").disabled = false;
}

cargarCentros();