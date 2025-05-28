const apiUrl = "http://127.0.0.1:8000/api/client";
const rowsPerPage = 12;
let currentPage = 1;
let clients = []; // This will now hold ALL clients, sorted by the backend
let currentlyDisplayedClients = []; // This will be used for display and filtering
let clientModalInstance;

function fetchClients() {
    axios.get(apiUrl).then(res => {
        clients = res.data.map(c => ({ ...c, active: Boolean(c.active) }));
        currentlyDisplayedClients = [...clients]; // Initialize with all clients, already sorted
        renderTable();
        // renderPagination is called within renderTable now
    }).catch(handleError);
}

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");
    sidebar.classList.toggle("sidebar-hidden");
    mainContent.classList.toggle("main-collapsed");
}

function getFilteredClients() {
    const query = document.getElementById("searchInput").value.trim().toLowerCase();
    const status = document.getElementById("statusFilter").value;

    return clients.filter(c => { // Filter from the 'clients' array (all data)
        const matchesQuery = !query || (
            c.first_name.toLowerCase().includes(query) ||
            c.last_name.toLowerCase().includes(query) ||
            c.email.toLowerCase().includes(query) ||
            c.number_identification.toLowerCase().includes(query)
        );

        const matchesStatus =
            status === "all" ||
            (status === "active" && c.active === true) ||
            (status === "inactive" && c.active === false);

        return matchesQuery && matchesStatus;
    });
}

function renderTable() {
    const tbody = document.getElementById("clientTableBody");
    tbody.innerHTML = "";

    // The filtering logic is now applied here before pagination
    const filtered = getFilteredClients();
    currentlyDisplayedClients = filtered; // Update the displayed array with filtered data
    
    const start = (currentPage - 1) * rowsPerPage;
    const paginated = currentlyDisplayedClients.slice(start, start + rowsPerPage); // Paginate the displayed array

    paginated.forEach(client => {
        const estadoTexto = client.active ? "Activo" : "Inactivo";
        const estadoClase = client.active ? "text-success" : "text-danger";

        const actionBtn = client.active
            ? `<button class="btn btn-sm btn-danger btn-status-toggle" onclick='toggleClientStatus(${client.id}, false)'>Desactivar</button>`
            : `<button class="btn btn-sm btn-success btn-status-toggle" onclick='toggleClientStatus(${client.id}, true)'>Activar</button>`;

        tbody.innerHTML += `
            <tr>
                <td>${client.id}</td>
                <td>${client.first_name}</td>
                <td>${client.last_name}</td>
                <td>${client.phone}</td>
                <td>${client.email}</td>
                <td>${client.number_identification}</td>
                <td><span class="${estadoClase}">${estadoTexto}</span></td>
                <td>
                    <button class="btn btn-sm btn-custom me-1" onclick='openEditModal(${JSON.stringify(client)})'>Editar</button>
                    ${actionBtn}
                </td>
            </tr>`;
    });

    renderPagination(currentlyDisplayedClients.length); // Pass the length of the currently displayed clients
}

function renderPagination(total) {
    const pageCount = Math.ceil(total / rowsPerPage);
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    for (let i = 1; i <= pageCount; i++) {
        pagination.innerHTML += `
            <li class="page-item ${i === currentPage ? "active" : ""}">
                <button class="page-link btn-custom" onclick="goToPage(${i})">${i}</button>
            </li>`;
    }
}

function goToPage(page) {
    currentPage = page;
    renderTable(); // This will now re-render the table with the correct slice of currentlyDisplayedClients
}

function openClientModal(client = {}) {
    document.getElementById("modalTitle").innerText = client.id ? "Editar Cliente" : "Crear Cliente";
    document.getElementById("clientId").value = client.id || "";
    document.getElementById("firstName").value = client.first_name || "";
    document.getElementById("lastName").value = client.last_name || "";
    document.getElementById("phone").value = client.phone || "";
    document.getElementById("email").value = client.email || "";
    document.getElementById("identification").value = client.number_identification || "";
    if (clientModalInstance) {
        clientModalInstance.show();
    }
}

function openEditModal(client) {
    openClientModal(client);
}

function submitClient(e) {
    e.preventDefault();
    const id = document.getElementById("clientId").value;
    const data = {
        first_name: document.getElementById("firstName").value,
        last_name: document.getElementById("lastName").value,
        phone: document.getElementById("phone").value,
        email: document.getElementById("email").value,
        number_identification: document.getElementById("identification").value,
    };

    const closeModal = () => {
        if (clientModalInstance) {
            document.activeElement.blur();
            setTimeout(() => {
                clientModalInstance.hide();
            }, 10);
        }
    };

    if (id) {
        axios.patch(`${apiUrl}/${id}/`, data)
            .then(res => {
                const updatedClient = res.data;
                // Update the main clients array
                const index = clients.findIndex(c => c.id === updatedClient.id);
                if (index !== -1) {
                    clients[index] = { ...updatedClient, active: Boolean(updatedClient.active) };
                }
                // Re-apply filters and render table to ensure updated data is shown correctly
                currentPage = 1; // Go back to first page
                renderTable(); 
                closeModal();
            })
            .catch(handleError);
    } else {
        axios.post(apiUrl, data)
            .then(res => {
                const newClient = res.data;
                // Add new client to the beginning of the arrays
                clients.unshift({ ...newClient, active: Boolean(newClient.active) });
                
                currentPage = 1; // Go to the first page to see the new client
                renderTable(); 
                closeModal();
            })
            .catch(handleError);
    }
}

function toggleClientStatus(id, activate) {
    const actionText = activate ? "activar" : "marcado como inactivo";
    const confirmText = activate ? "Sí, activar" : "Sí, marcar como inactivo";
    const successMessage = activate ? "El cliente ha sido activado." : "El cliente ha sido marcado como inactivo.";

    Swal.fire({
        title: "¿Estás seguro?",
        text: `El cliente será ${actionText}.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: activate ? "#28a745" : "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: confirmText,
        cancelButtonText: "Cancelar"
    }).then((result) => {
        if (result.isConfirmed) {
            axios.patch(`${apiUrl}/${id}/status/`, { active: activate })
                .then(() => {
                    Swal.fire("Éxito", successMessage, "success");
                    // Update the client's status in the local 'clients' array
                    const clientIndex = clients.findIndex(c => c.id === id);
                    if (clientIndex !== -1) {
                        clients[clientIndex].active = activate;
                    }
                    // Re-render to reflect the change
                    renderTable();
                })
                .catch((error) => {
                    console.error("Error al cambiar estado del cliente:", error);
                    handleError(error, "No se pudo cambiar el estado del cliente.");
                });
        }
    });
}

function handleError(err, customMessage = 'Ocurrió un error al procesar la solicitud.') {
    console.error("Error:", err);
    let errorMessage = customMessage;

    if (err.response) {
        console.error("Data:", err.response.data);
        console.error("Status:", err.response.status);
        console.error("Headers:", err.response.headers);
        if (typeof err.response.data === 'string') {
            errorMessage = err.response.data;
        } else if (err.response.data && typeof err.response.data.detail === 'string') {
            errorMessage = err.response.data.detail;
        } else if (err.response.data && typeof err.response.data.error === 'string') {
            errorMessage = err.response.data.error;
        } else if (err.response.data && typeof err.response.data.message === 'string') {
            errorMessage = err.response.data.message;
        } else if (err.response.status) {
            errorMessage = `Error del servidor: ${err.response.status}`;
        }
    } else if (err.request) {
        console.error("Request:", err.request);
        errorMessage = "No se pudo obtener respuesta del servidor. Verifica tu conexión o la disponibilidad del servicio.";
    } else {
        console.error('Error Message:', err.message);
        errorMessage = `Error en la configuración de la solicitud: ${err.message}`;
    }

    if (typeof Swal !== 'undefined') {
        Swal.fire("Error", errorMessage, "error");
    } else {
        alert(`Ha ocurrido un error: ${errorMessage}`);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    fetchClients();

    const modalEl = document.getElementById("clientModal");
    if (modalEl) {
        clientModalInstance = new bootstrap.Modal(modalEl);
    } else {
        console.error("Elemento del modal #clientModal no encontrado.");
    }

    const statusFilterEl = document.getElementById("statusFilter");
    if (statusFilterEl) {
        statusFilterEl.addEventListener("change", () => {
            currentPage = 1;
            renderTable(); // This will re-filter and re-render
        });
    }

    const searchInputEl = document.getElementById("searchInput");
    if (searchInputEl) {
        searchInputEl.addEventListener('keyup', () => {
            currentPage = 1;
            renderTable(); // This will re-filter and re-render
        });
    }

    const clientFormEl = document.getElementById("clientForm");
    if (clientFormEl) {
        clientFormEl.addEventListener("submit", submitClient);
    }

    const createClientButton = document.querySelector('[data-bs-target="#clientModal"]');
    if (createClientButton) {
        createClientButton.addEventListener('click', () => openClientModal());
    }

    const sidebarToggler = document.getElementById('sidebarToggle');
    if (sidebarToggler) {
        sidebarToggler.addEventListener('click', toggleSidebar);
    }
});

window.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const cedula = params.get('cedula');
    const abrirModal = params.get('nuevo');

    if (cedula && abrirModal === '1') {
        // Abrir modal
        const modal = new bootstrap.Modal(document.getElementById('clientModal'));
        modal.show();

        // Prellenar campo de cédula (asegúrate de tener un input con este ID)
        const cedulaInput = document.getElementById('identification'); // Changed to 'identification' based on your form
        if (cedulaInput) {
            cedulaInput.value = cedula;
        }
    }
});

function aplicarRolesMenu() {
    const usertype = localStorage.getItem("usertype");

    const adminIcons = document.querySelectorAll(".only-admin");

    if (usertype === "1") {
        adminIcons.forEach(icon => {
            const parentLink = icon.closest("a");
            if (parentLink) {
                parentLink.style.display = "";
            }
        });
    } else {
        adminIcons.forEach(icon => {
            const parentLink = icon.closest("a");
            if (parentLink) {
                parentLink.style.display = "none";
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    aplicarRolesMenu();
});

function logout() {
    localStorage.clear();
    window.location.href = "/index.html";
}