-- 1. Создаем одну дефолтную должность (Администратор)
INSERT INTO main_job ("jobName", "deputy_id") VALUES 
('Администратор системы', NULL);

-- 2. Создаем один дефолтный отдел (Администрация)
INSERT INTO main_department ("departmentName", "headId_id") VALUES 
('Техническая поддежка', NULL);

-- 3. Создаем одну дефолтную функцию (Управление системой)
INSERT INTO main_functions ("funcName", "consistent_id") VALUES 
('Управление системой', NULL);

-- 4. Создаем один дефолтный deputy (Администрирование)
INSERT INTO main_deputy ("deputyName", "deputyDescription", "compulsory") VALUES 
('Администрирование', 'Функции администрирования системы', TRUE);

-- 5. Обновляем ссылку deputy в job
UPDATE main_job SET "deputy_id" = 1 WHERE "jobId" = 1;

-- 6. Обновляем ссылку consistent в functions
UPDATE main_functions SET "consistent_id" = 1 WHERE "funcId" = 1;

-- 7. Связываем deputy с функцией (many-to-many)
INSERT INTO main_deputy_deputy_functions ("deputy_id", "functions_id") VALUES 
(1, 1);

-- 8. Связываем отдел с должностью (many-to-many)
INSERT INTO main_department_jobslist ("department_id", "job_id") VALUES 
(1, 1);

-- 9. Создаем админского пользователя
-- Пароль: admin123 (хеш Django для удобства тестирования)
INSERT INTO main_employee (
    "firstName", "lastName", "patronymic", 
    "login", "password", 
    "jobid_id", "position", "departmentid_id", "email"
) VALUES (
    'Роман', 'Белых', 'Александрович',
    'admin', 
    'bellxz011', 
    1,  -- jobid (Администратор)
    5,  -- position (админский уровень)
    1,  -- departmentid (Администрация)
    'admin@example.com'
);

-- 10. Обновляем headId в department
UPDATE main_department SET "headId_id" = 1 WHERE "departmentId" = 1;

-- 11. Создаем одну запись трудозатрат для админа (опционально)
INSERT INTO main_laborcosts (
    "employee_id", "department_id", "function_id", "deputy_id",
    "compulsory", "worked_hours", "comment", "date"
) VALUES (
    1, 1, 1, 1,
    TRUE, 8.00, 'Администрирование системы', NOW()
);

-- 12. Создаем одну запись в логах (опционально)
INSERT INTO main_logs (
    "level", "message", "created_at", "module"
) VALUES (
    'INFO', 'Система инициализирована', NOW(), 'system'
);