-- Sample SQL queries for testing

-- Find user by username
SELECT u.id, u.username, u.email, u.created_at
FROM users u
WHERE u.username = ? AND u.is_active = TRUE;

-- Get user with roles
SELECT u.id, u.username, u.email, r.name as role_name
FROM users u
LEFT JOIN user_roles ur ON u.id = ur.user_id
LEFT JOIN roles r ON ur.role_id = r.id
WHERE u.id = ?;

-- Count active users
SELECT COUNT(*) as active_count
FROM users
WHERE is_active = TRUE;

-- Find users by role
SELECT u.id, u.username, u.email
FROM users u
INNER JOIN user_roles ur ON u.id = ur.user_id
INNER JOIN roles r ON ur.role_id = r.id
WHERE r.name = ?
ORDER BY u.created_at DESC;

-- Update user last login
UPDATE users
SET updated_at = CURRENT_TIMESTAMP
WHERE id = ?;
