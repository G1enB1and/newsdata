CREATE OR REPLACE VIEW slug_from_path AS
SELECT(REPLACE(log.path, '/article/', '')) AS
slug FROM log
WHERE log.path != '/';
