# Database Migrations

This directory contains SQLite database migration scripts for schema updates.

## Migration File Naming Convention

Migration files should be named using the following pattern:
```
{version}_{description}.sql
```

Example:
- `001_initial_schema.sql`
- `002_add_workspace_category.sql`
- `003_add_annotation_visibility.sql`

## Migration File Structure

Each migration file should contain:

```sql
-- Migration: {version} - {description}
-- Date: YYYY-MM-DD
-- Author: {name}

-- Up migration (apply changes)
-- ============================================================================

ALTER TABLE workspaces ADD COLUMN new_column TEXT;

-- ============================================================================
-- Down migration (revert changes) - Optional, for reference
-- ============================================================================

-- ALTER TABLE workspaces DROP COLUMN new_column;
```

## Applying Migrations

Migrations are applied automatically by the `SQLiteConnectionManager` when the database is initialized.

To manually apply migrations:

```python
from codeindex.web.database.connection import get_workspace_manager
from codeindex.web.database.migrations.migrator import apply_migrations

manager = get_workspace_manager()
apply_migrations(manager)
```

## Current Schema Version

The current schema version is tracked in the `schema_version` table. Check the version with:

```python
manager = get_workspace_manager()
version = manager.get_schema_version()
print(f"Current schema version: {version}")
```

## Creating a New Migration

1. Determine the next version number by checking existing migrations
2. Create a new file: `{next_version}_{description}.sql`
3. Write the SQL statements to apply the changes
4. Test the migration locally before committing
5. Update this README if there are breaking changes

## Migration Guidelines

- **Keep migrations small and focused** - One logical change per migration
- **Test migrations** - Verify they work on a fresh database and existing data
- **Document breaking changes** - If migration requires manual steps, document them
- **No data loss** - Always backup data before migrations in production
- **Idempotent** - Migrations should be safe to run multiple times (use IF NOT EXISTS, etc.)

## Initial Schema (Version 0)

The initial schema (version 0) is defined in `../schema.sql` and includes:
- `workspaces` table with full-text search
- `annotations` table with FTS5 index
- Triggers for automatic FTS updates
- Views for common queries
