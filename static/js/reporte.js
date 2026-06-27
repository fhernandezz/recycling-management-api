const token = localStorage.getItem("token");

async function cargarTopRecicladores() {

    const respuesta = await fetch(
        "http://127.0.0.1:8000/records/reports/top-recyclers",
        {
            headers:{
                "Authorization":"Bearer " + token
            }
        }
    );

    const datos = await respuesta.json();

    const tabla = document.getElementById("tablaTop");

    tabla.innerHTML="";

    datos.forEach(reciclador=>{

        tabla.innerHTML += `
        <tr>

            <td>${reciclador[0]}</td>
            <td>${reciclador[1]}</td>
            <td>${reciclador[2]}</td>
            <td>${reciclador[3]}</td>

        </tr>
        `;

    });

}

async function cargarEstadoCentros(){

    const respuesta = await fetch(
        "http://127.0.0.1:8000/records/reports/collection-points-status",
        {
            headers:{
                "Authorization":"Bearer " + token
            }
        }
    );

    const datos = await respuesta.json();

    const tabla = document.getElementById("tablaCentros");

    tabla.innerHTML="";

    datos.forEach(centro=>{

        tabla.innerHTML += `
        <tr>

            <td>${centro.name}</td>
            <td>${centro.current_load}</td>
            <td>${centro.max_capacity}</td>
            <td>${centro.percentage}%</td>
            <td>${centro.status}</td>

        </tr>
        `;

    });

}

cargarTopRecicladores();

cargarEstadoCentros();