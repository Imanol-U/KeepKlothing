
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementsByClassName('review-form')[0]; //Pillamos el formulario
    const contenedorResenas = document.getElementsByClassName('product-reviews'); //Este es el contenedor de las reseñas
    const lista_resenias = document.querySelector('.product-reviews ul'); //Esta es la lista en la que meteremos la reseña creada

    //const formDelete = document.getElementsByClassName('botonELiminar')[0]; //Formulario que elimina la reseña

    //Añadimos un listener al contenedor padre

    //if (contenedorResenas){
    //    contenedorResenas[0].addEventListener('click', function(event){
    //        const target = event.target;
    //
    //        const botonELiminar = target.closest('.btnEliminarResena');
    //
    //        if(botonELiminar){
    //            handleEliminarResenia(botonELiminar);
    //        }
    //
    //    });
    //
    //}
    //
    //

    form.addEventListener('submit', function (event) {

        event.preventDefault(); //Detener envío por defecto que es sincrono
        const data = new FormData(form);
        const csrftoken = data.get('csrfmiddlewaretoken'); //obtener token del formulario (porque es el metodo post)

        //Solicitud ajax con fetchApi
        fetch(form.action, {
            method: 'POST',
            body: data,
            headers: {
                'X-requested-With': 'XMLHttpRequest',
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Respuesta del servidor fallida. Estado: ' + response.status)
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    //La insercion en la bbdd exitosa
                    let nuevaResenaHTML = `
                <li>
                    <strong>${data.usuario_nombre}</strong>
                    -${data.estrellas} / 5 ⭐
                    <br>
                    <small>${data.fecha_resenia}</small>
                    <p>${data.comentario}</p>
                `;

                    // Si el servidor nos devuelve la URL para borrar, incluimos el formulario
                    if (data.delete_url) {
                        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                        nuevaResenaHTML += `
                    <form method="post" action="${data.delete_url}">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <button type="submit" class="btnEliminarResena">
                            Eliminar reseña
                        </button>
                    </form>
                    `;
                    }

                    nuevaResenaHTML += `</li>`;

                    lista_resenias.insertAdjacentHTML('afterbegin', nuevaResenaHTML);

                    const elementoAlerta = document.createElement('p');

                    // Asignarle el ID (como propiedad del objeto)
                    elementoAlerta.id = 'review-alert';

                    //Asignarle el contenido de texto
                    elementoAlerta.textContent = 'Gracias por tu opinión! Solo puedes dejar una reseña por producto.';

                    //Insertar el objeto DOM antes del formulario
                    form.before(elementoAlerta);
                    document.getElementById('MensajeResenia').remove();
                    form.remove();

                } else {
                    alert('Errores en el formulario:' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.error('Error en la solicitud AJAX:', error);
                alert('Erro al intentar enviar la reseña');
            });
    });
});

