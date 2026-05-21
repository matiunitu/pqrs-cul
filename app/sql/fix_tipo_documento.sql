-- Asegura que la columna tipo_documento exista, no sea nula y tenga un valor por defecto
ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS tipo_documento VARCHAR(10);

UPDATE usuarios
SET tipo_documento = 'CC'
WHERE tipo_documento IS NULL OR TRIM(tipo_documento) = '';

ALTER TABLE usuarios
    ALTER COLUMN tipo_documento SET DEFAULT 'CC';

ALTER TABLE usuarios
    ALTER COLUMN tipo_documento SET NOT NULL;
