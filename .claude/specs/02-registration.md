---
# Spec: Registration

## Overview
This feature implements the user registration flow, allowing new users to create an account. It transitions the `/register` route from a simple template render to a functional form that validates input, hashes passwords, and persists users in the database. This is a foundational step for authentication and personalized expense tracking.

## Depends on
No previous steps (Initial setup is complete).

## Routes
- `GET /register` — Display the registration form — public
- `POST /register` — Process registration data, create user, and redirect to login — public

## Database changes
No database changes. The `users` table already contains `id`, `name`, `email`, `password_hash`, and `created_at`.

## Templates
- **Create:** None (register.html already exists)
- **Modify:** `templates/register.html` — update to include a `<form>` with `method="POST"` and action pointing to `/register`.

## Files to change
- `app.py` — add `POST /register` logic, update `GET /register` to handle potential flash messages.
- `database/db.py` — add a helper function `create_user(name, email, password_hash)` to handle the insertion.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- [ ] User can navigate to `/register` and see the form.
- [ ] Submitting the form with valid data creates a new user in the `users` table.
- [ ] Submitting the form with an existing email returns a clear error message (e.g., via Flask flash).
- [ ] Passwords are stored as hashes in the database, not plain text.
- [ ] After successful registration, the user is redirected to `/login`.
---
