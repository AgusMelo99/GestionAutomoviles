document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form'); // Asegúrate de seleccionar el formulario correcto
    if (form) {
        form.addEventListener('submit', validarFormulario);
    }
});

// Función para validar el formulario completo
function validarFormulario(event) {
    let esValido = true;

    // Validar nombre
    const nombreInput = document.getElementById('nombre');
    if (!validarNombreApellido(nombreInput.value)) {
        alert('Registro fallido: el nombre solo debe contener letras y espacios.');
        esValido = false;
    }

    // Validar apellido
    const apellidoInput = document.getElementById('apellido');
    if (!validarNombreApellido(apellidoInput.value)) {
        alert('Registro fallido: el apellido solo debe contener letras y espacios.');
        esValido = false;
    }

    // Validar correo electrónico
    const emailInput = document.getElementById('email');
    if (!validarEmail(emailInput.value)) {
        alert('Registro fallido: por favor, ingrese un correo electrónico válido.');
        esValido = false;
    }

    // Validar contraseña
    const contrasenaInput = document.getElementById('contrasena');
    if (!validarContrasena(contrasenaInput.value)) {
        alert('Registro fallido: la contraseña debe tener al menos 8 caracteres, incluyendo letras y números.');
        esValido = false;
    }

    // Prevenir el envío del formulario si no es válido
    if (!esValido) {
        event.preventDefault();
    }

    return esValido;
}

// Función para validar nombre y apellido
function validarNombreApellido(texto) {
    const regex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/; // Solo letras y espacios
    return regex.test(texto);
}

// Función para validar el formato del correo electrónico
function validarEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}

// Función para validar que la contraseña tenga al menos 8 caracteres, incluyendo letras y números
function validarContrasena(contrasena) {
    const regex = /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/; // Al menos 8 caracteres, letras y números
    return regex.test(contrasena);
}
