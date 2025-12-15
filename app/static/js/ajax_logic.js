
document.addEventListener('DOMContentLoaded', function(){
const form = document.getElementsByClassName('review-form')[0]; //Pillamos el formulario
const contenedorResenas = document.getElementsByClassName('product-reviews') //Este es el contenedor de las reseñas

form.addEventListener('submit', function(event){
    event.preventDefault(); //Detener envío por defecto que es sincrono

    const data = new FormData(form);
    const csrftoken = data.get('csrfmiddlewaretoken'); //obtener token del formulario (porque es el metodo post)

    //Solicitud ajax con fetchApi
    fetch(form.action, {
        method: 'POST',
        body: data,
        headers: {
            'X-requested-With':'XMLHttpRequest',
        },
    })
    .then(response =>{
        if (!response.ok){
            throw new Error('Respuesta del servidor fallida. Estado: ' + response.status)
            }
            return response.json();
        })
        .then(data => {
            if (data.success){
                //La insercion en la bbdd exitosa
                const nuevaResenaHTML = `
                <div class="resena-item">
                    <h4>Autor: ${data.usuario_nombre}</h4>
                    <p>${data.comentario}</p>
                    <small>Fecha: ${data.fecha_resenia}</small>
                </div>
            `;      
            contenedorResenas[0].insertAdjacentHTML('afterbegin', nuevaResenaHTML);
            
            //Opcional pero recomencable limpiar form
            form.reset();

            } else {
                alert('Errores en el formulario:' + JSON.stringify(data.errors));
            }
        })
        .catch(error =>{
        //Manejo de errores de red o del bloque .then
        console.error('Error en la solicitud AJAX:', error);
        alert('Erro al intentar enviar la reseña');
        });
    });
});