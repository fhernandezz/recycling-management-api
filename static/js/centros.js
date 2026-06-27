const API_URL = "http://127.0.0.1:8000/collection-points";

const token = localStorage.getItem("token");

console.log("TOKEN FRONT:", token);

const tabla = document.getElementById("tablaCentros");

const formulario = document.getElementById("formCentro");

async function cargarCentros() {

    try {

        const respuesta = await fetch(API_URL, {

            headers: {

                "Authorization": "Bearer " + token

            }

        });

        console.log("STATUS:", respuesta.status);
        console.log("RESPUESTA:", await respuesta.clone().text());

        const centros = await respuesta.json();

        tabla.innerHTML = "";

        centros.forEach(centro => {

            tabla.innerHTML += `

            <tr>

                <td>${centro.point_id}</td>

                <td>${centro.name}</td>

                <td>${centro.location}</td>

                <td>${centro.district}</td>

                <td>${centro.accepted_materials}</td>

                <td>${centro.capacity_kg}</td>

                <td>${centro.current_load_kg}</td>

                <td>${centro.is_active ? "Sí" : "No"}</td>

            </tr>

            `;

        });

    }

    catch(error){

        console.log(error);

        alert("Error cargando centros.");

    }

}

cargarCentros();

formulario.addEventListener("submit", async function(e){

    e.preventDefault();

    const nuevoCentro = {

        point_id: document.getElementById("point_id").value,

        name: document.getElementById("name").value,

        location: document.getElementById("location").value,

        district: document.getElementById("district").value,

        accepted_materials: document.getElementById("accepted_materials").value,

        capacity_kg: parseFloat(document.getElementById("capacity_kg").value),

        current_load_kg: 0,

        is_active: true

    };

    try{

        const respuesta = await fetch(API_URL + "/",{

            method:"POST",

            headers:{

                "Content-Type":"application/json",

                "Authorization":"Bearer " + token

            },

            body: JSON.stringify(nuevoCentro)

        });

        if(respuesta.ok){

            alert("Centro registrado correctamente.");

            formulario.reset();

            cargarCentros();

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