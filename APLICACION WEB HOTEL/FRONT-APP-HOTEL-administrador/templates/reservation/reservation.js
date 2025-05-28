let rooms = [];
let clients = [];
let reservationStatuses = [];
let reservations = [];
let users = [];
let types = [];
let currentPage = 1;
const itemsPerPage = 20;

// New global variable to hold the currently displayed (and potentially filtered) reservations
let currentlyDisplayedReservations = [];

async function fetchData() {
    try {
        const usersResponse = await axios.get('http://127.0.0.1:8000/api/user');
        users = usersResponse.data;

        const clientsResponse = await axios.get('http://127.0.0.1:8000/api/client');
        clients = clientsResponse.data;

        const roomsResponse = await axios.get('http://127.0.0.1:8000/api/room');
        rooms = roomsResponse.data;

        const statusResponse = await axios.get('http://127.0.0.1:8000/api/reservationstatus');
        reservationStatuses = statusResponse.data;

        // Fetch ALL reservations, now sorted by the backend
        const reservationsResponse = await axios.get('http://127.0.0.1:8000/api/reservations/');
        reservations = reservationsResponse.data; // All reservations fetched, already sorted
        currentlyDisplayedReservations = [...reservations]; // Initialize with all reservations

        const typesResponse = await axios.get("http://127.0.0.1:8000/api/roomtypes/")
        types = typesResponse.data;

        populateTables(); // Now uses `currentlyDisplayedReservations`
        populateSelects();
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

function populateSelects() {
  const userSelect = document.getElementById('user_id');
  const clientSelect = document.getElementById('client_id');
  const roomSelect = document.getElementById('room_id');
  const statusSelect = document.getElementById('reservation_status_id');

  userSelect.innerHTML = '<option value="">Seleccionar...</option>';
  users.forEach(user => {
    const option = document.createElement('option');
    option.value = user.id;
    option.textContent = user.username;
    userSelect.appendChild(option);
  });

  clientSelect.innerHTML = '<option value="">Seleccionar...</option>';
  clients.forEach(client => {
    const option = document.createElement('option');
    option.value = client.id;
    option.textContent = `${client.first_name} ${client.last_name}`;
    clientSelect.appendChild(option);
  });

  roomSelect.innerHTML = '<option value="">Seleccionar...</option>';
  rooms.forEach(room => {
    const option = document.createElement('option');
    option.value = room.id;
    option.textContent = `Habitación ${room.room_number}`;
    roomSelect.appendChild(option);
  });

  statusSelect.innerHTML = '<option value="">Seleccionar...</option>';
  reservationStatuses.forEach(status => {
    const option = document.createElement('option');
    option.value = status.id;
    option.textContent = status.name;
    statusSelect.appendChild(option);
  });

  // Rellenar el filtro por estado
  const filterStatus = document.getElementById('filter_status');
  filterStatus.innerHTML = '<option value="">Todos</option>';
  reservationStatuses.forEach(status => {
    const option = document.createElement('option');
    option.value = status.id;
    option.textContent = status.name;
    filterStatus.appendChild(option);
  });

}


function populateTables() {
    const reservationTableBody = document.getElementById('reservationTableBody');
    reservationTableBody.innerHTML = '';

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedReservations = currentlyDisplayedReservations.slice(start, end);

    paginatedReservations.forEach(reservation => {
        const user = users.find(u => u.id === reservation.user_id);
        const client = clients.find(c => c.id === reservation.client_id);
        const room = rooms.find(r => r.id === reservation.room_id);
        const status = reservationStatuses.find(s => s.id === reservation.reservation_status_id);

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${reservation.id}</td>
            <td>${client ? client.first_name + " " + client.last_name : 'Desconocido'}</td>
            <td>${client ? client.number_identification : 'Sin cédula'}</td>
            <td>${room ? room.room_number : 'Desconocido'}</td>
            <td>${reservation.check_in_date}</td>
            <td>${reservation.check_out_date}</td>
            <td>${reservation.total}</td>
            <td>${status ? status.name : 'Desconocido'}</td>
            <td>${user ? user.username : 'Desconocido'}</td>
            <td>
                <div class="d-flex flex-wrap gap-1">
                    <button class="btn btn-warning btn-sm" onclick="editReservation(${reservation.id})">Editar</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteReservation(${reservation.id})">Eliminar</button>
                    <button class="btn btn-custom btn-sm" onclick="generateReservationTicket(${reservation.id})">Ticket</button>
                </div>
            </td>
        `;
        reservationTableBody.appendChild(tr);
    });

    renderPagination();
}

function renderPagination() {
    const paginationContainer = document.getElementById('pagination');
    paginationContainer.innerHTML = '';

    // Calculate total pages based on `currentlyDisplayedReservations`
    const totalPages = Math.ceil(currentlyDisplayedReservations.length / itemsPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.className = `btn btn-sm ${i === currentPage ? 'btn-primary' : 'btn-outline-primary'} m-1`;
        btn.textContent = i;
        btn.onclick = () => {
            currentPage = i;
            populateTables();
        };
        paginationContainer.appendChild(btn);
    }
}


function openReservationModal() {
  document.getElementById('reservationId').value = '';
  document.getElementById('client_id').value = '';
  document.getElementById('room_id').value = '';
  document.getElementById('user_id').value = '';
  document.getElementById('reservation_status_id').value = '';
  document.getElementById('check_in_date').value = '';
  document.getElementById('check_out_date').value = '';
  document.getElementById('note').value = '';

  const modal = new bootstrap.Modal(document.getElementById('reservationModal'));
  modal.show();
}

function editReservation(id) {
  const reservation = reservations.find(r => r.id === id);
  if (reservation) {
    document.getElementById('reservationId').value = reservation.id;
    document.getElementById('client_id').value = reservation.client_id;
    document.getElementById('room_id').value = reservation.room_id;
    document.getElementById('user_id').value = reservation.user_id;
    document.getElementById('reservation_status_id').value = reservation.reservation_status_id;
    document.getElementById('check_in_date').value = reservation.check_in_date;
    document.getElementById('check_out_date').value = reservation.check_out_date;
    document.getElementById('note').value = reservation.note;

    const modal = new bootstrap.Modal(document.getElementById('reservationModal'));
    modal.show();
  }
}

function deleteReservation(id) {
  Swal.fire({
    title: '¿Estás seguro?',
    text: "¡No podrás revertir esto!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  }).then((result) => {
    if (result.isConfirmed) {
      axios.delete(`http://127.0.0.1:8000/api/reservations/${id}`)
        .then(response => {
          reservations = reservations.filter(r => r.id !== id);
          currentlyDisplayedReservations = currentlyDisplayedReservations.filter(r => r.id !== id); // Also update the displayed array
          populateTables();
          Swal.fire('¡Eliminado!', 'La reserva ha sido eliminada.', 'success');
        })
        .catch(error => {
          console.error("Error eliminando reserva:", error);
          Swal.fire('Error', 'Hubo un problema al eliminar la reserva.', 'error');
        });
    }
  });
}

function searchReservations() {
    const searchQuery = document.getElementById('searchClient').value.toLowerCase();
    currentlyDisplayedReservations = reservations.filter(reservation => {
        const client = clients.find(c => c.id === reservation.client_id);
        return client && (
            client.first_name.toLowerCase().includes(searchQuery) ||
            client.last_name.toLowerCase().includes(searchQuery)
        );
    });
    currentPage = 1; // Reset to first page for search results
    populateTables();
}

function searchClientByDocument() {
  const documentInput = document.getElementById('searchDocument').value.trim();
  if (!documentInput) {
    Swal.fire('Campo vacío', 'Por favor ingresa una cédula para buscar.', 'warning');
    return;
  }

  const client = clients.find(c => c.number_identification === documentInput);
  if (client) {
    document.getElementById('client_id').value = client.id;
    Swal.fire('Cliente encontrado', `${client.first_name} ${client.last_name}`, 'success');
  } else {
    Swal.fire({
      title: 'Cliente no encontrado',
      text: '¿Deseas crear un nuevo cliente?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'Sí, crear cliente',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        // Redirige con la cédula como parámetro
        window.location.href = `/templates/clients/clients.html?cedula=${encodeURIComponent(documentInput)}&nuevo=1`;
      }
    });
  }
}


function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.getElementById("main-content");
  sidebar.classList.toggle("sidebar-hidden");
  mainContent.classList.toggle("main-collapsed");
}

document.getElementById('reservationForm').addEventListener('submit', function (event) {
  event.preventDefault();

  const reservationId = document.getElementById('reservationId').value;
  const clientId = document.getElementById('client_id').value;
  const roomId = document.getElementById('room_id').value;
  const userId = document.getElementById('user_id').value;
  const reservationStatusId = document.getElementById('reservation_status_id').value;
  const checkInDate = document.getElementById('check_in_date').value;
  const checkOutDate = document.getElementById('check_out_date').value;
  const note = document.getElementById('note').value;

  const reservationData = {
    client_id: clientId,
    room_id: roomId,
    reservation_status_id: reservationStatusId,
    check_in_date: checkInDate,
    check_out_date: checkOutDate,
    note: note,
    user_id: userId,
  };

  if (reservationId) {
    axios.patch(`http://127.0.0.1:8000/api/reservations/${reservationId}`, reservationData)
      .then(response => {
        const updatedReservation = response.data;
        const index = reservations.findIndex(r => r.id === updatedReservation.id);
        if (index !== -1) {
            reservations[index] = updatedReservation; // Update the main data array
        }
        // Also update currentlyDisplayedReservations if the item is there
        const displayedIndex = currentlyDisplayedReservations.findIndex(r => r.id === updatedReservation.id);
        if (displayedIndex !== -1) {
            currentlyDisplayedReservations[displayedIndex] = updatedReservation;
        }

        // After update, if you want to maintain the "newest first" visually,
        // you might re-sort `currentlyDisplayedReservations` or refresh `fetchData`.
        // For simplicity and since the backend sends it sorted, just re-populating is usually fine.
        populateTables();
        document.getElementById('reservationModal').querySelector('.btn-close').click();
      })
      .catch(error => {
        console.error('Error editando reserva:', error);
        alert('Error al editar la reserva');
      });
  } else {
    axios.post('http://127.0.0.1:8000/api/reservations/', reservationData)
      .then(response => {
        // When creating a new reservation, add it to the beginning of the arrays
        reservations.unshift(response.data); // Add to the main data array
        currentlyDisplayedReservations.unshift(response.data); // Add to the displayed data array
        
        // Reset current page to 1 to show the newly added item at the top
        currentPage = 1;
        populateTables();
        document.getElementById('reservationModal').querySelector('.btn-close').click();
      })
      .catch(error => {
        console.error('Error creando reserva:', error);
        alert('Error al crear la reserva');
      });
  }
});

// Filtro por fechas y estado
function filterReservations() {
    const checkInFilter = document.getElementById('filter_check_in').value;
    const checkOutFilter = document.getElementById('filter_check_out').value;
    const statusFilter = document.getElementById('filter_status').value;

    let filtered = [...reservations]; // Start with all reservations

    if (checkInFilter) {
        filtered = filtered.filter(r => r.check_in_date >= checkInFilter);
    }
    if (checkOutFilter) {
        filtered = filtered.filter(r => r.check_out_date <= checkOutFilter);
    }
    if (statusFilter) {
        filtered = filtered.filter(r => r.reservation_status_id == statusFilter);
    }

    currentlyDisplayedReservations = filtered; // Update the displayed array
    currentPage = 1; // Reset to first page for filtered results
    populateTables();
}

// Botón limpiar filtros
function clearFilters() {
  document.getElementById('filter_check_in').value = '';
  document.getElementById('filter_check_out').value = '';
  document.getElementById('filter_status').value = '';
  currentlyDisplayedReservations = [...reservations]; // Reset to all original reservations
  currentPage = 1; // Reset to first page
  populateTables();

  Swal.fire('Filtros limpiados', '', 'success');
}


// Validación de fechas al crear/editar reservas
document.getElementById('check_out_date').addEventListener('change', function () {
  const checkInDate = document.getElementById('check_in_date').value;
  const checkOutDate = this.value;

  if (checkInDate && checkOutDate && checkOutDate < checkInDate) {
    Swal.fire('Error', 'La fecha de salida no puede ser menor que la de entrada.', 'error');
    this.value = '';
  }
});

document.getElementById('room_id').addEventListener('change', function () {
  const selectedRoomId = parseInt(this.value);
  const selectedRoom = rooms.find(room => room.id === selectedRoomId);

  if (selectedRoom) {
    const typeId = selectedRoom.room_type_id || (selectedRoom.room && selectedRoom.room.room_type_id);
    const type = types.find(t => t.id === typeId);
    document.getElementById('room_type').value = type ? type.name : 'Desconocido';
    document.getElementById('room_price').value = selectedRoom.price_per_night || selectedRoom.cost || '';
  } else {
    document.getElementById('room_type').value = '';
    document.getElementById('room_price').value = '';
  }
});

fetchData();

async function generateReservationTicket(id) {
  const reservation = reservations.find(r => r.id === id);
  if (!reservation) return Swal.fire('Error', 'Reserva no encontrada.', 'error');

  const client = clients.find(c => c.id === reservation.client_id);
  const user = users.find(u => u.id === reservation.user_id);
  const room = rooms.find(r => r.id === reservation.room_id);
  const status = reservationStatuses.find(s => s.id === reservation.reservation_status_id);
  const typeId = room?.room_type_id || room?.room?.room_type_id;
  const roomType = types.find(t => t.id === typeId);

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: [80, 150]
  });

  const now = new Date();
  const fecha = now.toLocaleDateString();
  const hora = now.toLocaleTimeString();

  let y = 10;

  // Encabezado
  doc.setFontSize(12);
  doc.setFont("helvetica", "bold");
  doc.text("HOTEL APP", 40, y, { align: "center" }); y += 6;

  doc.setFontSize(10);
  doc.setFont("helvetica", "normal");
  doc.text("COMPROBANTE DE RESERVA", 40, y, { align: "center" }); y += 5;
  doc.setFontSize(8);
  doc.text(`Fecha: ${fecha}   Hora: ${hora}`, 40, y, { align: "center" }); y += 5;

  doc.setLineWidth(0.5);
  doc.line(5, y, 75, y); y += 4;

  // Datos
  doc.setFont("helvetica", "bold");
  doc.text("Datos de la Reserva", 10, y); y += 5;
  doc.setFont("helvetica", "normal");
  doc.text(`ID: ${reservation.id}`, 10, y); y += 5;
  doc.text(`Estado: ${status?.name || 'Desconocido'}`, 10, y); y += 5;

  doc.setFont("helvetica", "bold");
  doc.text("Cliente", 10, y); y += 5;
  doc.setFont("helvetica", "normal");
  doc.text(`Nombre: ${client?.first_name || ''} ${client?.last_name || ''}`, 10, y); y += 5;
  doc.text(`Cédula: ${client?.number_identification || ''}`, 10, y); y += 5;

  doc.setFont("helvetica", "bold");
  doc.text("Habitación", 10, y); y += 5;
  doc.setFont("helvetica", "normal");
  doc.text(`Número: ${room?.room_number || ''}`, 10, y); y += 5;
  doc.text(`Tipo: ${roomType?.name || 'N/A'}`, 10, y); y += 5;
  doc.text(`Precio x noche: $${room?.price_per_night || room?.cost || 0}`, 10, y); y += 5;

  doc.setFont("helvetica", "bold");
  doc.text("Fechas", 10, y); y += 5;
  doc.setFont("helvetica", "normal");
  doc.text(`Check-in: ${reservation.check_in_date}`, 10, y); y += 5;
  doc.text(`Check-out: ${reservation.check_out_date}`, 10, y); y += 5;

  doc.setFont("helvetica", "bold");
  doc.text("Total", 10, y); y += 5;
  doc.setFont("helvetica", "normal");
  doc.text(`$${reservation.total}`, 10, y); y += 5;

  if (reservation.note) {
    doc.setFont("helvetica", "bold");
    doc.text("Nota", 10, y); y += 4;
    doc.setFont("helvetica", "normal");
    const splitNote = doc.splitTextToSize(reservation.note, 60);
    doc.text(splitNote, 10, y); y += splitNote.length * 4;
  }

  doc.setLineWidth(0.3);
  doc.line(5, y, 75, y); y += 5;

  doc.setFont("helvetica", "italic");
  doc.setFontSize(9);
  doc.text("Gracias por su reserva", 40, y, { align: "center" });

  doc.save(`reserva_${reservation.id}.pdf`);
}

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