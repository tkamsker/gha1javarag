# Data Model

## Overview
This section describes the data model of the system, including entities, attributes, and relationships.


### User

**Attributes:**

| Name | Type | Description |
|------|------|-------------|
| user_id | integer | Primary key, unique identifier for user |
| username | string | Username for login |
| password | string | Hashed login password |
| role | string | Role of the user (admin, doctor, receptionist, worker, patient) |

**Relationships:**

| Entity | Type | Description |
|--------|------|-------------|
| Doctor | one-to-one | A user may have doctor profile if role is doctor |
| Patient | one-to-one | A user may have patient profile if role is patient |
| Receptionist | one-to-one | A user may have receptionist profile if role is receptionist |
| Worker | one-to-one | A user may have worker profile if role is worker |
