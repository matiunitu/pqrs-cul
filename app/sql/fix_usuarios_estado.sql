-- =============================================
-- FIX: Añadir columna faltante y actualizar usuarios a estado = 1 (Activo)
-- Fecha: 2026-05-19
-- Descripción: Asegura que la columna `tipo_documento` exista y corrige
--              los valores de `estado` para que los usuarios aparezcan activos.
-- =============================================

-- 1) Agregar columna tipo_documento si no existe (valor por defecto 'CC')
ALTER TABLE usuarios
  ADD COLUMN IF NOT EXISTS tipo_documento VARCHAR(10) DEFAULT 'CC';

UPDATE usuarios
SET tipo_documento = 'CC'
WHERE tipo_documento IS NULL OR TRIM(tipo_documento) = '';

ALTER TABLE usuarios
  ALTER COLUMN tipo_documento SET NOT NULL;

-- 2) Asegurar que la columna estado exista y que tenga valor por defecto 1
ALTER TABLE usuarios
  ADD COLUMN IF NOT EXISTS estado SMALLINT DEFAULT 1;

-- 3) Actualizar todos los usuarios para que tengan estado = 1 (Activo)
UPDATE usuarios SET estado = 1 WHERE estado IS NULL OR estado = 0;

ALTER TABLE usuarios
  ALTER COLUMN estado SET NOT NULL;

-- 4) Verificación rápida: devuelve el conteo de usuarios activos
-- SELECT COUNT(*) as total_usuarios_activos FROM usuarios WHERE estado = 1;
