document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await axios.post("http://127.0.0.1:8000/api/login", {
      username,
      password
    });

    // Asegúrate de que usertype_id sea tratado como cadena desde el inicio si lo necesitas
    const usertype = String(response.data.user_type_id); // Convertir a cadena explícitamente
    const usernameResp = response.data.username;

    localStorage.setItem("usertype", usertype); // Guardará "1" o "2"
    localStorage.setItem("username", usernameResp);

    document.getElementById("message").innerHTML = `
      <div class="alert alert-success">
        ${response.data.message}
      </div>
    `;

    // Redirección según tipo de usuario
    // ¡Ahora comparamos con CADENAS DE TEXTO!
    if (usertype === "1") { // Comparación con CADENA
      window.location.href = "/templates/dashboard/dashboard.html";
    } else if (usertype === "2") { // Comparación con CADENA
      window.location.href = "/templates/reservation/reservation.html";
    } else {
      // En caso de que haya otro tipo, puedes manejarlo aquí
      window.location.href = "/templates/dashboard/dashboard.html";
    }

  } catch (error) {
    const errMsg = error.response?.data?.detail || "Error desconocido";
    document.getElementById("message").innerHTML = `
      <div class="alert alert-danger">
        ${errMsg}
      </div>
    `;
  }
});