console.log('JavaScript de validación cargado correctamente');
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (event) => {
            let esValido = true;

            const anio = document.getElementById('anio').value;
            const kilometraje = document.getElementById('kilometraje').value;
            const patente = document.getElementById('vin').value;
            //const patente = document.getElementById('patente') ? document.getElementById('patente').value : null;

            // Validar que el año no sea negativo o futuro
            const anioActual = new Date().getFullYear();
            if (anio < 1886 || anio > anioActual) {  // Los primeros autos fueron fabricados en 1886
                alert('Año inválido: debe ser entre 1886 y el año actual.');
                esValido = false;
            }

            // Validar que el kilometraje no sea negativo
            if (kilometraje < 0) {
                alert('El kilometraje no puede ser negativo.');
                esValido = false;
            }

            // Validar patente (opcional, si el campo está presente)
            if (patente && !validarPatente(patente)) {
                alert('Formato de patente inválido: debe ser ABC123 o AB123CD.');
                esValido = false;
            }

            if (!esValido) {
                event.preventDefault();  // Evita el envío si hay errores
            }
        });
    }
});


// Función para validar patente
function validarPatente(patente) {
    const regex = /^[A-Z]{3}[0-9]{3}$|^[A-Z]{2}[0-9]{3}[A-Z]{2}$/;  // Patente: ABC123 o AB123CD
    return regex.test(patente);
}
