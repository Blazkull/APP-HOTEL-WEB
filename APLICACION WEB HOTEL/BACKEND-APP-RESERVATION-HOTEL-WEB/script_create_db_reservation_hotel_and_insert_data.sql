create database db_reservation_hotel;
use db_reservation_hotel;


INSERT INTO usertype (name, description) VALUES
('Admin', 'Administrador del sistema'),
('Recepcionista', 'Empleado de recepción'),
('Gerente', 'Encargado general del hotel');

select *from user;
INSERT INTO user (username, email, password, user_type_id,active) VALUES
('admin1', 'admin1@hotel.com', 'hashed_password1', 1,true),
('recepcion1', 'recepcion1@hotel.com', 'hashed_password2', 2,true),
('recepcion2', 'recepcion2@hotel.com', 'hashed_password3', 2,true),
('gerente1', 'gerente1@hotel.com', 'hashed_password4', 3,true);

INSERT INTO roomstatus (name, description) VALUES
('Disponible', 'Habitación disponible'),
('Ocupada', 'Habitación actualmente ocupada'),
('Limpieza', 'Habitación en proceso de limpieza'),
('Mantenimiento', 'Habitación en mantenimiento');

INSERT INTO roomtype (name, description) VALUES
('Estándar', 'Sencilla, cama doble/individual, ideal estancias cortas.'),
('Doble Sup.', 'Amplia, cama doble grande/dobles, comodidades extra.'),
('Suite Jr.', 'Espaciosa, zona estar separada, familias/largas.'),
('Suite Pres.', 'Lujosa, múltiples estancias, alta gama, exclusiva.');

INSERT INTO room (room_number, price_per_night, capacity, room_type_id, room_status_id,active) VALUES
('101', 50, 1, 1, 1,true),
('102', 60, 1, 1, 1,true),
('103', 80, 2, 2, 1,true),
('104', 90, 2, 2, 2,true),
('201', 120, 3, 3, 1,true),
('202', 130, 3, 3, 3,true),
('203', 140, 3, 3, 1,true),
('204', 150, 3, 3, 4,true),
('301', 200, 4, 4, 1,true),
('302', 210, 4, 4, 1,true),
('303', 220, 4, 4, 2,true),
('304', 230, 4, 4, 3,true),
('401', 250, 2, 2, 1,true),
('402', 260, 2, 2, 4,true),
('403', 270, 1, 1, 1,true),
('404', 280, 1, 1, 3,true),
('501', 300, 3, 3, 1,true),
('502', 310, 3, 3, 2,true),
('503', 320, 4, 4, 1,true),
('504', 330, 4, 4, 1,true);


INSERT INTO reservationstatus (name, description) VALUES
('Pendiente', 'Reserva pendiente de confirmación'),
('Confirmada', 'Reserva confirmada'),
('Cancelada', 'Reserva cancelada'),
('Completada', 'Reserva completada exitosamente');

INSERT INTO client (first_name, last_name, phone, email, number_identification,active) VALUES
('Juan', 'Pérez', '555-0001', 'juan.perez1@email.com', 'ID001',true),
('Ana', 'Gómez', '555-0002', 'ana.gomez2@email.com', 'ID002',true),
('Luis', 'Martínez', '555-0003', 'luis.martinez3@email.com', 'ID003',true),
('María', 'López', '555-0004', 'maria.lopez4@email.com', 'ID004',true),
('Carlos', 'Díaz', '555-0005', 'carlos.diaz5@email.com', 'ID005',true),
('Laura', 'Fernández', '555-0006', 'laura.fernandez6@email.com', 'ID006',true),
('Pedro', 'Ramírez', '555-0007', 'pedro.ramirez7@email.com', 'ID007',true),
('Lucía', 'Torres', '555-0008', 'lucia.torres8@email.com', 'ID008',true),
('Andrés', 'Flores', '555-0009', 'andres.flores9@email.com', 'ID009',true),
('Sofía', 'Cruz', '555-0010', 'sofia.cruz10@email.com', 'ID010',true),
('Miguel', 'Ruiz', '555-0011', 'miguel.ruiz11@email.com', 'ID011',true),
('Valentina', 'Morales', '555-0012', 'valentina.morales12@email.com', 'ID012',true),
('Ricardo', 'Sánchez', '555-0013', 'ricardo.sanchez13@email.com', 'ID013',true),
('Daniela', 'Ortega', '555-0014', 'daniela.ortega14@email.com', 'ID014',true),
('Javier', 'Castro', '555-0015', 'javier.castro15@email.com', 'ID015',true),
('Camila', 'Silva', '555-0016', 'camila.silva16@email.com', 'ID016',true),
('Fernando', 'Vargas', '555-0017', 'fernando.vargas17@email.com', 'ID017',true),
('Isabella', 'Ríos', '555-0018', 'isabella.rios18@email.com', 'ID018',true),
('Pablo', 'Méndez', '555-0019', 'pablo.mendez19@email.com', 'ID019',true),
('Sara', 'Navarro', '555-0020', 'sara.navarro20@email.com', 'ID020',true),
('Alberto', 'Peña', '555-0021', 'alberto.pena21@email.com', 'ID021',true),
('Julia', 'Campos', '555-0022', 'julia.campos22@email.com', 'ID022',true),
('Diego', 'Luna', '555-0023', 'diego.luna23@email.com', 'ID023',true),
('Marta', 'Herrera', '555-0024', 'marta.herrera24@email.com', 'ID024',true),
('Héctor', 'Aguilar', '555-0025', 'hector.aguilar25@email.com', 'ID025',true),
('Victoria', 'Salazar', '555-0026', 'victoria.salazar26@email.com', 'ID026',true),
('Esteban', 'Medina', '555-0027', 'esteban.medina27@email.com', 'ID027',true),
('Paula', 'Vega', '555-0028', 'paula.vega28@email.com', 'ID028',true),
('Santiago', 'Paredes', '555-0029', 'santiago.paredes29@email.com', 'ID029',true),
('Daniel', 'Soto', '555-0030', 'daniel.soto30@email.com', 'ID030',true),
('Gabriela', 'Cordero', '555-0031', 'gabriela.cordero31@email.com', 'ID031',true),
('José', 'Beltrán', '555-0032', 'jose.beltran32@email.com', 'ID032',true),
('Andrea', 'Carrillo', '555-0033', 'andrea.carrillo33@email.com', 'ID033',true),
('Francisco', 'Mora', '555-0034', 'francisco.mora34@email.com', 'ID034',true),
('Natalia', 'Acosta', '555-0035', 'natalia.acosta35@email.com', 'ID035',true),
('Roberto', 'Escobar', '555-0036', 'roberto.escobar36@email.com', 'ID036',true),
('Alejandra', 'Villarreal', '555-0037', 'alejandra.villarreal37@email.com', 'ID037',true),
('Óscar', 'Ramos', '555-0038', 'oscar.ramos38@email.com', 'ID038',true),
('Patricia', 'Miranda', '555-0039', 'patricia.miranda39@email.com', 'ID039',true),
('Ernesto', 'Montoya', '555-0040', 'ernesto.montoya40@email.com', 'ID040',true);

INSERT INTO reservation (user_id, reservation_status_id, client_id, room_id, check_in_date, check_out_date, note, total) VALUES
(1, 2, 1, 1, '2025-05-01', '2025-05-05', 'Reserva de prueba 1', 200),
(2, 1, 2, 2, '2025-05-02', '2025-05-06', 'Reserva de prueba 2', 240),
(3, 2, 3, 3, '2025-05-03', '2025-05-04', 'Reserva de prueba 3', 80),
(4, 3, 4, 4, '2025-05-04', '2025-05-08', 'Reserva de prueba 4', 360),
(1, 4, 5, 5, '2025-05-05', '2025-05-07', 'Reserva de prueba 5', 240),
(2, 2, 6, 6, '2025-05-06', '2025-05-09', 'Reserva de prueba 6', 150),
(3, 1, 7, 7, '2025-05-07', '2025-05-11', 'Reserva de prueba 7', 220),
(4, 3, 8, 8, '2025-05-08', '2025-05-12', 'Reserva de prueba 8', 330),
(1, 2, 9, 9, '2025-05-09', '2025-05-13', 'Reserva de prueba 9', 260),
(2, 1, 10, 10, '2025-05-10', '2025-05-14', 'Reserva de prueba 10', 180),
(3, 4, 11, 11, '2025-05-11', '2025-05-15', 'Reserva de prueba 11', 280),
(4, 2, 12, 12, '2025-05-12', '2025-05-16', 'Reserva de prueba 12', 210),
(1, 3, 13, 13, '2025-05-13', '2025-05-17', 'Reserva de prueba 13', 350),
(2, 2, 14, 14, '2025-05-14', '2025-05-18', 'Reserva de prueba 14', 240),
(3, 1, 15, 15, '2025-05-15', '2025-05-19', 'Reserva de prueba 15', 190),
(4, 3, 16, 16, '2025-05-16', '2025-05-20', 'Reserva de prueba 16', 300),
(1, 4, 17, 17, '2025-05-17', '2025-05-21', 'Reserva de prueba 17', 250),
(2, 2, 18, 18, '2025-05-18', '2025-05-22', 'Reserva de prueba 18', 200),
(3, 1, 19, 19, '2025-05-19', '2025-05-23', 'Reserva de prueba 19', 220),
(4, 3, 20, 20, '2025-05-20', '2025-05-24', 'Reserva de prueba 20', 330),
(1, 2, 21, 1, '2025-05-21', '2025-05-25', 'Reserva de prueba 21', 150),
(2, 1, 22, 2, '2025-05-22', '2025-05-26', 'Reserva de prueba 22', 280),
(3, 4, 23, 3, '2025-05-23', '2025-05-27', 'Reserva de prueba 23', 180),
(4, 2, 24, 4, '2025-05-24', '2025-05-28', 'Reserva de prueba 24', 240),
(1, 3, 25, 5, '2025-05-25', '2025-05-29', 'Reserva de prueba 25', 270),
(2, 1, 26, 6, '2025-05-26', '2025-05-30', 'Reserva de prueba 26', 190),
(3, 4, 27, 7, '2025-05-27', '2025-05-31', 'Reserva de prueba 27', 250),
(4, 2, 28, 8, '2025-05-28', '2025-06-01', 'Reserva de prueba 28', 300),
(1, 3, 29, 9, '2025-05-29', '2025-06-02', 'Reserva de prueba 29', 330),
(2, 4, 30, 10, '2025-05-30', '2025-06-03', 'Reserva de prueba 30', 220),
(3, 1, 31, 11, '2025-05-31', '2025-06-04', 'Reserva de prueba 31', 250),
(4, 2, 32, 12, '2025-06-01', '2025-06-05', 'Reserva de prueba 32', 270),
(1, 4, 33, 13, '2025-06-02', '2025-06-06', 'Reserva de prueba 33', 200),
(2, 1, 34, 14, '2025-06-03', '2025-06-07', 'Reserva de prueba 34', 320),
(3, 3, 35, 15, '2025-06-04', '2025-06-08', 'Reserva de prueba 35', 240),
(4, 2, 36, 16, '2025-06-05', '2025-06-09', 'Reserva de prueba 36', 270),
(1, 1, 37, 17, '2025-06-06', '2025-06-10', 'Reserva de prueba 37', 220),
(2, 4, 38, 18, '2025-06-07', '2025-06-11', 'Reserva de prueba 38', 350),
(3, 2, 39, 19, '2025-06-08', '2025-06-12', 'Reserva de prueba 39', 300),
(4, 1, 40, 20, '2025-06-09', '2025-06-13', 'Reserva de prueba 40', 250);
