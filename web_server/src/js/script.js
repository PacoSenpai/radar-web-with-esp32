// Función para realizar la solicitud al servidor y mostrar la lista
function obtenerListaDelServidor() {
    fetch('http://localhost:8000/api/obtener_cadenas')
        .then(response => response.json())
        .then(data => mostrarLista(data.cadenas_recibidas))
        .catch(error => console.error('Error al obtener la lista:', error));
}

// Función para mostrar la lista en el HTML
function mostrarLista(cadenas) {
    const listaElement = document.getElementById('listaCadenas');
    listaElement.innerHTML = '';

    cadenas.forEach(cadena => {
        const listItem = document.createElement('li');
        listItem.textContent = cadena;
        listaElement.appendChild(listItem);
    });
}


// Llamar a la función para obtener la lista cada segundo
setInterval(obtenerListaDelServidor, 1000);