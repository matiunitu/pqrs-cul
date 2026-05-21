-- =============================================
-- ACTUALIZACIÓN DE TABLAS: estado (0/1), created_at, updated_at
-- =============================================

-- Tabla roles: agregar estado, created_at, updated_at
ALTER TABLE roles
  ADD COLUMN IF NOT EXISTS estado SMALLINT DEFAULT 1,
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Tabla facultades
ALTER TABLE facultades
  ADD COLUMN IF NOT EXISTS estado SMALLINT DEFAULT 1,
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Tabla programas
ALTER TABLE programas
  ADD COLUMN IF NOT EXISTS estado SMALLINT DEFAULT 1,
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Tabla dependencias
ALTER TABLE dependencias
  ADD COLUMN IF NOT EXISTS estado SMALLINT DEFAULT 1,
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Tabla tipospqrs
ALTER TABLE tipospqrs
  ADD COLUMN IF NOT EXISTS estado SMALLINT DEFAULT 1,
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Tabla prioridades
ALTER TABLE prioridades
  ADD COLUMN IF NOT EXISTS estado SMALLINT DEFAULT 1,
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Tabla usuarios: agregar password_hash, estado int (0/1), updated_at
ALTER TABLE usuarios
  ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255),
  ADD COLUMN IF NOT EXISTS estado SMALLINT DEFAULT 1,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Tabla pqrs: agregar updated_at
ALTER TABLE pqrs
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Tabla respuestas: agregar updated_at
ALTER TABLE respuestas
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- =============================================
-- FUNCIÓN: auto-actualizar updated_at
-- =============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers para updated_at automático
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_usuarios_updated_at') THEN
    CREATE TRIGGER trg_usuarios_updated_at
      BEFORE UPDATE ON usuarios
      FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_pqrs_updated_at') THEN
    CREATE TRIGGER trg_pqrs_updated_at
      BEFORE UPDATE ON pqrs
      FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_roles_updated_at') THEN
    CREATE TRIGGER trg_roles_updated_at
      BEFORE UPDATE ON roles
      FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  END IF;
END $$;

-- =============================================
-- INSERTAR ROLES BASE (3 mínimos)
-- =============================================
INSERT INTO roles (nombre_rol, descripcion, estado) VALUES
  ('admin',      'Acceso total al sistema',                    1),
  ('docente',    'Gestión de PQRS propias y respuestas',       1),
  ('estudiante', 'Crear y consultar sus propias PQRS',         1)
ON CONFLICT DO NOTHING;

-- =============================================
-- USUARIO DE PRUEBA: nelson / admin / 1234
-- La contraseña se establece via script Python
-- password "1234" -> bcrypt hash se inyecta desde auth_controller
-- =============================================
-- Insertar usuario nelson con rol admin (id_rol=1), programa demo (id_programa=1)
-- NOTA: Ejecutar primero seed_auth_user.py para crear el hash bcrypt correcto
