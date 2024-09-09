document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form'); // Cambiado para seleccionar el formulario correcto
    if (form) {
        form.addEventListener('submit', validarFormulario);
    }
});
//validar cuestionario completo
function validarFormulario(event) {
    let esValido = true;

    // validar nombre
    const nombreInput = document.getElementById('nombre');
    const nombreError = document.getElementById('error-nombre');
    if (!validarNombreApellido(nombreInput.value)) {
        nombreError.textContent = 'El nombre solo debe contener letras y espacios.';
        nombreError.style.display = 'block';
        esValido = false;
    } else {
        nombreError.style.display = 'none';
    }

    // Validar apellido
    const apellidoInput = document.getElementById('apellido');
    const apellidoError = document.getElementById('error-apellido');
    if (!validarNombreApellido(apellidoInput.value)) {
        apellidoError.textContent = 'El apellido solo debe contener letras y espacios.';
        apellidoError.style.display = 'block';
        esValido = false;
    } else {
        apellidoError.style.display = 'none';
    }

    // validar correo electrónico
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('error-email');
    if (!validarEmail(emailInput.value)) {
        emailError.textContent = 'Por favor, ingrese un correo electrónico válido.';
        emailError.style.display = 'block';
        esValido = false;
    } else {
        emailError.style.display = 'none';
    }

    // validar contraseña
    const contrasenaInput = document.getElementById('contrasena');
    const contrasenaError = document.getElementById('error-contrasena');
    if (!validarContrasena(contrasenaInput.value)) {
        contrasenaError.textContent = 'La contraseña debe tener al menos 8 caracteres, incluyendo letras y números.';
        contrasenaError.style.display = 'block';
        esValido = false;
    } else {
        contrasenaError.style.display = 'none';
    }

    // no envía el formulario si no es válido
    if (!esValido) {
        event.preventDefault();
    }
    return esValido;
}

// validar nombre y apellido
function validarNombreApellido(texto) {
    const regex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/; // Solo letras y espacios
    return regex.test(texto);
}

// validar el formato del correo electrónico
function validarEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}

// validar que la contraseña tenga al menos 8 caracteres, incluyendo letras y números
function validarContrasena(contrasena) {
    const regex = /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/; // Al menos 8 caracteres, letras y números
    return regex.test(contrasena);
}
