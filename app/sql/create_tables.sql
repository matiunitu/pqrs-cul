CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE facultades (
    id_facultad SERIAL PRIMARY KEY,
    nombre_facultad VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE programas (
    id_programa SERIAL PRIMARY KEY,
    nombre_programa VARCHAR(100),
    descripcion TEXT,
    id_facultad INTEGER REFERENCES facultades(id_facultad)
);

CREATE TABLE dependencias (
    id_dependencia SERIAL PRIMARY KEY,
    nombre_dependencia VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE tipospqrs (
    id_tipospqrs SERIAL PRIMARY KEY,
    nombre_tipospqrs VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE estados (
    id_estado SERIAL PRIMARY KEY,
    nombre_estado VARCHAR(100)
);

CREATE TABLE prioridades (
    id_prioridad SERIAL PRIMARY KEY,
    nombre_prioridad VARCHAR(100),
    nivel INTEGER
);

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    documento VARCHAR(50),
    correo VARCHAR(100),
    telefono VARCHAR(20),
    id_rol INTEGER REFERENCES roles(id_rol),
    id_programa INTEGER REFERENCES programas(id_programa),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pqrs (
    id_pqrs SERIAL PRIMARY KEY,
    radicado VARCHAR(100),
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_limite TIMESTAMP,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_dependencia INTEGER REFERENCES dependencias(id_dependencia),
    id_tipospqrs INTEGER REFERENCES tipospqrs(id_tipospqrs),
    id_estado INTEGER REFERENCES estados(id_estado),
    id_prioridad INTEGER REFERENCES prioridades(id_prioridad)
);

CREATE TABLE respuestas (
    id_respuesta SERIAL PRIMARY KEY,
    mensaje TEXT,
    fecha_respuesta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_pqrs INTEGER NOT NULL REFERENCES pqrs(id_pqrs),
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario)
);

CREATE TABLE historial_estados (
    id_historial SERIAL PRIMARY KEY,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_pqrs INTEGER NOT NULL REFERENCES pqrs(id_pqrs),
    id_estado_anterior INTEGER REFERENCES estados(id_estado),
    id_estado_nuevo INTEGER REFERENCES estados(id_estado),
    cambiado_por INTEGER NOT NULL REFERENCES usuarios(id_usuario)
);
