const API_URL = "http://127.0.0.1:8000/recyclers";

const token = localStorage.getItem("token");

const tabla = document.getElementById("tablaRecicladores");

const formulario = document.getElementById("formRecycler");


// =========================
// Mostrar todos
// =========================

async function cargarRecicladores() {

    try {

        const respuesta = await fetch(API_URL, {

            headers: {
                "Authorization": "Bearer " + token
            }

        });

        const recicladores = await respuesta.json();

        tabla.innerHTML = "";

        recicladores.forEach(reciclador => {

            tabla.innerHTML += `

            <tr>

                <td>${reciclador.recycler_id}</td>

                <td>${reciclador.full_name}</td>

                <td>${reciclador.id_number}</td>

                <td>${reciclador.email}</td>

                <td>${reciclador.phone}</td>

                <td>${reciclador.district}</td>

                <td>${reciclador.is_active ? "Sí" : "No"}</td>

            </tr>

            `;

        });

    }

    catch(error){

        console.log(error);

        alert("Error cargando recicladores");

    }

}

cargarRecicladores();


// =========================
// Registrar
// =========================

formulario.addEventListener("submit", async function(e){

    e.preventDefault();

    const nuevoReciclador = {

        recycler_id: document.getElementById("recycler_id").value,

        full_name: document.getElementById("full_name").value,

        id_number: document.getElementById("id_number").value,

        email: document.getElementById("email").value,

        phone: document.getElementById("phone").value,

        district: document.getElementById("district").value,

        registration_date: document.getElementById("registration_date").value,

        is_active: true

    };


    try{

        const respuesta = await fetch(API_URL + "/",{

            method:"POST",

            headers:{

                "Content-Type":"application/json",

                "Authorization":"Bearer " + token

            },

            body: JSON.stringify(nuevoReciclador)

        });

        if(respuesta.ok){

            alert("Reciclador registrado correctamente.");

            formulario.reset();

            cargarRecicladores();

        }

        else{

            const error = await respuesta.json();

            alert(error.detail);

        }

    }

    catch(error){

        console.log(error);

        alert("No fue posible registrar.");

    }

});