const API_URL = "http://127.0.0.1:8000/records";
const token = localStorage.getItem("token");

const tabla = document.getElementById("tablaEntregas");
const formulario = document.getElementById("formEntrega");

let modoEdicion = false;

function obtenerHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    };
}

function crearFila(entrega) {
    return `
        <tr>
            <td>${entrega.record_id}</td>
            <td>${entrega.recycler_id}</td>
            <td>${entrega.point_id}</td>
            <td>${entrega.material_type}</td>
            <td>${entrega.weight_kg}</td>
            <td>${entrega.record_date}</td>
            <td>${entrega.notes}</td>
            <td>
                <button type="button" onclick="editarEntrega('${entrega.record_id}')">
                    Editar
                </button>
                <button type="button" onclick="eliminarEntrega('${entrega.record_id}')">
                    Eliminar
                </button>
            </td>
        </tr>
    `;
}

async function cargarEntregas() {
    try {
        const respuesta = await fetch(API_URL, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Error cargando entregas.");
            return;
        }

        const entregas = await respuesta.json();

        tabla.innerHTML = "";
        entregas.forEach(entrega => {
            tabla.innerHTML += crearFila(entrega);
        });

    } catch (error) {
        console.log(error);
        alert("Error cargando entregas.");
    }
}

formulario.addEventListener("submit", async function(e) {
    e.preventDefault();

    const entrega = {
        record_id: document.getElementById("record_id").value,
        recycler_id: document.getElementById("recycler_id").value,
        point_id: document.getElementById("point_id").value,
        material_type: document.getElementById("material_type").value,
        weight_kg: parseFloat(document.getElementById("weight_kg").value),
        record_date: document.getElementById("record_date").value,
        notes: document.getElementById("notes").value
    };

    let url = API_URL + "/";
    let metodo = "POST";

    if (modoEdicion) {
        url = API_URL + "/" + entrega.record_id;
        metodo = "PUT";
    }

    try {
        const respuesta = await fetch(url, {
            method: metodo,
            headers: obtenerHeaders(),
            body: JSON.stringify(entrega)
        });

        if (!respuesta.ok) {
            const error = await respuesta.json();
            alert(error.detail);
            return;
        }

        if (modoEdicion) {
            alert("Entrega actualizada correctamente.");
        } else {
            alert("Entrega registrada correctamente.");
        }

        limpiarFormulario();
        cargarEntregas();

    } catch (error) {
        console.log(error);
        alert("No fue posible guardar la entrega.");
    }
});

async function editarEntrega(id) {
    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Entrega no encontrada.");
            return;
        }

        const entrega = await respuesta.json();

        document.getElementById("record_id").value = entrega.record_id;
        document.getElementById("recycler_id").value = entrega.recycler_id;
        document.getElementById("point_id").value = entrega.point_id;
        document.getElementById("material_type").value = entrega.material_type;
        document.getElementById("weight_kg").value = entrega.weight_kg;
        document.getElementById("record_date").value = entrega.record_date;
        document.getElementById("notes").value = entrega.notes;

        modoEdicion = true;
        document.getElementById("record_id").disabled = true;

    } catch (error) {
        console.log(error);
        alert("No fue posible cargar la entrega.");
    }
}

async function eliminarEntrega(id) {
    if (!confirm("¿Eliminar entrega?")) {
        return;
    }

    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            method: "DELETE",
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("No fue posible eliminar la entrega.");
            return;
        }

        alert("Entrega eliminada correctamente.");
        cargarEntregas();

    } catch (error) {
        console.log(error);
        alert("No fue posible eliminar la entrega.");
    }
}

async function buscarEntrega() {
    const id = document.getElementById("buscarID").value;

    if (id.trim() === "") {
        alert("Ingrese el ID de la entrega.");
        return;
    }

    try {
        const respuesta = await fetch(API_URL + "/" + id, {
            headers: obtenerHeaders()
        });

        if (!respuesta.ok) {
            alert("Entrega no encontrada.");
            return;
        }

        const entrega = await respuesta.json();
        tabla.innerHTML = crearFila(entrega);

    } catch (error) {
        console.log(error);
        alert("No fue posible buscar la entrega.");
    }
}

function limpiarFormulario() {
    formulario.reset();
    modoEdicion = false;
    document.getElementById("record_id").disabled = false;
}

cargarEntregas();