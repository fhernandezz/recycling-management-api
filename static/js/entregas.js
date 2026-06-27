const API_URL = "http://127.0.0.1:8000/records";

const token = localStorage.getItem("token");

const tabla = document.getElementById("tablaEntregas");

const formulario = document.getElementById("formEntrega");

async function cargarEntregas() {

    try {

        const respuesta = await fetch(API_URL, {

            headers: {

                "Authorization": "Bearer " + token

            }

        });

        const entregas = await respuesta.json();

        console.log("STATUS:", respuesta.status);
        console.log("ENTREGAS:", entregas);

        tabla.innerHTML = "";

        entregas.forEach(entrega => {

            tabla.innerHTML += `

            <tr>

                <td>${entrega.record_id}</td>

                <td>${entrega.recycler_id}</td>

                <td>${entrega.point_id}</td>

                <td>${entrega.material_type}</td>

                <td>${entrega.weight_kg}</td>

                <td>${entrega.record_date}</td>

                <td>${entrega.notes}</td>

            </tr>

            `;

        });

    }

    catch(error){

        console.log(error);

        alert("Error cargando entregas.");

    }

}

cargarEntregas();

formulario.addEventListener("submit", async function(e){

    e.preventDefault();

    const nuevaEntrega = {

        record_id: document.getElementById("record_id").value,

        recycler_id: document.getElementById("recycler_id").value,

        point_id: document.getElementById("point_id").value,

        material_type: document.getElementById("material_type").value,

        weight_kg: parseFloat(document.getElementById("weight_kg").value),

        record_date: document.getElementById("record_date").value,

        notes: document.getElementById("notes").value

    };

    try{

        const respuesta = await fetch(API_URL + "/",{

            method:"POST",

            headers:{

                "Content-Type":"application/json",

                "Authorization":"Bearer " + token

            },

            body: JSON.stringify(nuevaEntrega)

        });

        if(respuesta.ok){

            alert("Entrega registrada correctamente.");

            formulario.reset();

            cargarEntregas();

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