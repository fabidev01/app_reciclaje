-- Crear tabla Rol
CREATE TABLE Rol (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(35) NOT NULL,
    descripcion TEXT
) ENGINE=InnoDB; -- Especificar el motor InnoDB para soportar claves foráneas

-- Crear tabla Permiso
CREATE TABLE Permiso (
    id_permiso INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(35) NOT NULL
) ENGINE=InnoDB;

-- Crear tabla Rol_Permiso
CREATE TABLE Rol_Permiso (
    id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol),
    FOREIGN KEY (id_permiso) REFERENCES Permiso(id_permiso)
) ENGINE=InnoDB;

-- Crear tabla Usuario
CREATE TABLE Usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(35) NOT NULL,
    correo VARCHAR(50) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    balance_puntos INT NOT NULL,
    fecha_registro DATE NOT NULL,
    contraseña VARCHAR(200) NOT NULL,
    ip VARCHAR(45) ,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
) ENGINE=InnoDB;

-- Crear tabla Material_Reciclable
CREATE TABLE Material_Reciclable (
    id_material_reciclable INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(35) NOT NULL,
    puntos_por_unidad INT NOT NULL,
    co2_por_unidad FLOAT NOT NULL,
    unidad_medida VARCHAR(10) NOT NULL
) ENGINE=InnoDB;

-- Crear tabla Punto_Reciclaje
CREATE TABLE Punto_Reciclaje (
    id_punto_reciclaje INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(35) NOT NULL,
    capacidad_maxima INT NOT NULL,
    hora_apertura TIME NOT NULL,
    hora_cierre TIME NOT NULL,
    latitud DECIMAL(10,8) NOT NULL,
    longitud DECIMAL(11,8) NOT NULL,
    estado_punto VARCHAR(15) NOT NULL
) ENGINE=InnoDB;

-- Crear tabla Material_Punto_Reciclaje
CREATE TABLE Material_Punto_Reciclaje (
    id_material_reciclable INT NOT NULL,
    id_punto_reciclaje INT NOT NULL,
    condiciones_especificas TEXT,
    PRIMARY KEY (id_material_reciclable, id_punto_reciclaje),
    FOREIGN KEY (id_material_reciclable) REFERENCES Material_Reciclable(id_material_reciclable),
    FOREIGN KEY (id_punto_reciclaje) REFERENCES Punto_Reciclaje(id_punto_reciclaje)
) ENGINE=InnoDB;

-- Crear tabla Registro_Reciclaje
CREATE TABLE Registro_Reciclaje (
    id_registro_reciclaje INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_punto_reciclaje INT NOT NULL,
    id_material_reciclable INT NOT NULL,
    cantidad_kg FLOAT NOT NULL,
    puntos_obtenidos INT NOT NULL,
    co2_reducido FLOAT NOT NULL,
    fecha_registro DATE NOT NULL,
    nombre_subtipo VARCHAR(35) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_punto_reciclaje) REFERENCES Punto_Reciclaje(id_punto_reciclaje),
    FOREIGN KEY (id_material_reciclable) REFERENCES Material_Reciclable(id_material_reciclable)
) ENGINE=InnoDB;

-- Crear tabla Catalogo_Recompensa
CREATE TABLE Catalogo_Recompensa (
    id_catalogo_recompensa INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(35) NOT NULL,
    puntos_coste INT NOT NULL,
    disponible BOOLEAN NOT NULL,
    stock INT NOT NULL,
    descuento FLOAT NOT NULL,
    categoria VARCHAR(35) NOT NULL,
    ruta_imagen VARCHAR(255) NULL
) ENGINE=InnoDB;

-- Crear tabla Donacion
CREATE TABLE Donacion (
    id_donacion INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(35) NOT NULL,
    entidad_donacion VARCHAR(35) NOT NULL,
    monto_donacion FLOAT NOT NULL,
    ruta_imagen VARCHAR(255) NULL
) ENGINE=InnoDB;

-- Crear tabla Canje_Recompensa
CREATE TABLE Canje_Recompensa (
    id_canje_recompensa INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_catalogo_recompensa INT NOT NULL,
    estado VARCHAR(35) NOT NULL,
    fecha_canje DATE NOT NULL,
    puntos_descontados INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_catalogo_recompensa) REFERENCES Catalogo_Recompensa(id_catalogo_recompensa)
) ENGINE=InnoDB;

-- Crear tabla Canje_Donacion
CREATE TABLE Canje_Donacion (
    id_canje_donacion INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_donacion INT NOT NULL,
    estado VARCHAR(35) NOT NULL,
    fecha_canje DATE NOT NULL,
    puntos_descontados INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_donacion) REFERENCES Donacion(id_donacion)
) ENGINE=InnoDB;

-- Crear tabla Bitacora_Acceso
CREATE TABLE Bitacora_Acceso (
    id_bitacora_acceso INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    tipo_acceso VARCHAR(35) NOT NULL,
    fecha_acceso DATE NOT NULL,
    resultado VARCHAR(35) NOT NULL,
    detalle TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
) ENGINE=InnoDB;

-- Crear tabla Bitacora_Catalogo
CREATE TABLE Bitacora_Catalogo (
    id_bitacora_catalogo INT PRIMARY KEY AUTO_INCREMENT,
    ip VARCHAR(45) NULL,
    id_catalogo_recompensa INT NOT NULL,
    accion VARCHAR(35) NOT NULL,
    fecha_accion DATE NOT NULL,
    detalle TEXT,
    FOREIGN KEY (id_catalogo_recompensa) REFERENCES Catalogo_Recompensa(id_catalogo_recompensa)
) ENGINE=InnoDB;

-- Crear tabla Bitacora_Reciclaje
CREATE TABLE Bitacora_Reciclaje (
    id_bitacora_reciclaje INT PRIMARY KEY AUTO_INCREMENT,
    ip VARCHAR(45) NULL,
    id_registro_reciclaje INT NOT NULL,
    accion VARCHAR(35) NOT NULL,
    fecha_accion DATE NOT NULL,
    detalle TEXT,
    FOREIGN KEY (id_registro_reciclaje) REFERENCES Registro_Reciclaje(id_registro_reciclaje)
) ENGINE=InnoDB;

-- Crear tabla Bitacora_Canje
CREATE TABLE Bitacora_Canje (
    id_bitacora_canje INT PRIMARY KEY AUTO_INCREMENT,
    ip VARCHAR(45) NULL,
    id_canje_recompensa INT NOT NULL,
    id_catalogo_recompensa INT NOT NULL,
    accion VARCHAR(35) NOT NULL,
    fecha_accion DATE NOT NULL,
    detalle TEXT,
    FOREIGN KEY (id_canje_recompensa) REFERENCES Canje_Recompensa(id_canje_recompensa),
    FOREIGN KEY (id_catalogo_recompensa) REFERENCES Catalogo_Recompensa(id_catalogo_recompensa)
) ENGINE=InnoDB;

-- Crear tabla Impacto_Ambiental_Diario
CREATE TABLE Impacto_Ambiental_Diario (
    id_impacto_ambiental_diario INT AUTO_INCREMENT PRIMARY KEY,
    fecha_dia DATE NOT NULL,
    tipo_basura VARCHAR(35) NOT NULL,
    unidad_medida VARCHAR(10) NOT NULL,
    cantidad_reciclada_por_tipo FLOAT NOT NULL,
    co2_reducido_por_tipo FLOAT NOT NULL,
    CONSTRAINT uk_impacto_diario UNIQUE (fecha_dia, tipo_basura)
);

CREATE TABLE Usuario_Permiso (
    id_usuario INT NOT NULL,
    id_permiso INT NOT NULL,
    PRIMARY KEY (id_usuario, id_permiso),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_permiso) REFERENCES Permiso(id_permiso)
);