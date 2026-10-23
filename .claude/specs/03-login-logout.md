---
# Spec: Login and Logout

## Overview
This feature implements the authentication flow for Spendly, allowing registered users to sign in to their accounts and securely sign out. It establishes the session management necessary for all subsequent features that require a logged-in user (like profiles and expense tracking).

## Depends on
- 01-database-setup
- 02-registration

## Routes
- `GET /login` — Renders the login page — public
- `POST /login` — Authenticates user and starts session — public
- `GET /logout` — Ends session and redirects to landing — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `login.html` — Update to include a functional login form.

## Files to change
- `app.py` — Implement login and logout route logic.
- `database/db.py` — Add a helper function to fetch a user by email.

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
- Use Flask `session` for managing user state.

## Definition of done
- [ ] User can successfully log in with valid credentials and is redirected to the profile page.
- [ ] User sees an error message when attempting to log in with an incorrect password.
- [ ] User sees an error message when attempting to log in with an unregistered email.
- [ ] User is redirected to the landing page after clicking logout.
- [ ] Accessing `/logout` while not logged in redirects the user to the login page.
---
