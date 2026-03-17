# Project Overview for AI Agents

This repository implements a small Enterprise Process Automation SaaS platform using
Flask. The goal is to provide a minimal yet complete example: backend APIs,
JWT authentication, admin/user roles, a simple dashboard, and a static demo
published via GitHub Pages.

## Big Picture Architecture

- **app/**: main package
  - `__init__.py` contains the factory creating the Flask app, initializing
db, jwt, migrations, and registering blueprints.
  - `models/` defines SQLAlchemy models (`User`, `Process`, `AuditLog`).
  - `routes/` holds blueprints for `auth_routes.py`, `process_routes.py`, and
    `admin_routes.py`. Most business logic is simple and inlined; a `services`
    directory exists but only has placeholders.
  - `utils/` has `logger.py` and `security.py` (password hashing).
  - `extensions.py` centralizes extensions such as `db`, `jwt`, `migrate`.

- **templates/** and **static/** support the Flask UI used locally. The
  templates rely on Bootstrap 5 and dynamic JS in `app/static/js/app.js` to
  consume the backend. Conditional rendering (admin cards) is controlled by
  JWT claims parsed in client-side JS.

- **docs/** is a separate folder containing a stripped-down, static demo of the
  login/dashboard. It is deployed to GitHub Pages via a workflow. The demo uses
  its own simplified JS (`docs/app.js`) that only simulates login (admin/admin).

- **Dockerfile** and **docker-compose.yml** orchestrate the Flask app and a PostgreSQL
  database. The database volume is `postgres_data`. The compose file sets up a
  restart policy and waits before creating tables (application checks
  `db.engine.table_names()` in `before_first` request). Default credentials are
  `admin/admin` created automatically.

## Key Developer Workflows

- **Local development**: run `docker-compose up --build` from workspace root. The
  app is available at `http://localhost:5000` and the database persists in a
  named volume. Modify code and restart the container for changes.

- **Database schema**: migrations are initialized but not used; the app calls
  `db.create_all()` on start if necessary.

- **Authentication**: JWT Extended stores `identity` as username and adds a
  `role` claim. Routes use `@jwt_required()` and check `get_jwt().get('role')`.

- **Static demo publish**: docs folder is built by `gh-pages` workflow. To
  update, edit `docs/index.html` or other assets, commit to `main`, and the
  workflow will republish to `gh-pages` which is served by GitHub Pages.
  Use a personal access token (`GH_PAT` secret) for deployment.

- **Logging and audit**: `audit_log` table stores user actions. Logs are created
  in route handlers with `logger.info()`; the `admin_routes.get_logs` returns
  all logs to admin users.

## Patterns and Conventions

- **Blueprints** are used for separation by feature. Each route file imports
  `db` and models directly; there is no service layer yet.

- **JWT** identities are simple strings (`User.username`) and additional claims
  added via `additional_claims_loader`.

- **Frontend code** is vanilla JS using `fetch`. Token parsing routines are
  defined in `static/js/app.js` and replicated in `docs/app.js` for the demo.

- **Static demo** intentionally avoids server dependencies. It does not import
  Jinja templates; the HTML must be fully self-contained. JavaScript logic is
duplicated in `docs/app.js` for interactivity.

- **GitHub Pages workflow** uses `peaceiris/actions-gh-pages@v4` with a PAT
  secret and publishes the `docs/` directory to the `gh-pages` branch. The
  repository name must not end with a hyphen; rename otherwise.

- **Configuration** is read from `.env` with `FLASK_ENV`, `SECRET_KEY`, etc.
  A `.env.example` is provided. Environment values are accessed via
  `app.config.from_envvar` or similar.

## Recommendations for AI Assistance

- When editing the backend, maintain consistency with the simple CRUD style
  already present. Use existing decorators and error handling patterns.

- For UI tasks, remember that local templates and static assets are served by
  Flask; the demo in `docs/` must not use Jinja or server APIs.

- Tests are not included; if adding tests, use `pytest` and place them under
  a new `tests/` directory mirroring the app structure.

- For migrations, either keep using `db.create_all()` or add Flask-Migrate
  commands (`flask db migrate`) and update Docker entrypoint accordingly.

- Avoid referencing paths or resources outside the repo root when running in
  containers; container's working directory is `/app` per Dockerfile.

- When updating GitHub workflows, modify `.github/workflows/pages.yml`. The
  workflow depends on `docs/` and the `GH_PAT` secret; changes often require
  recomputing the token scopes.

- Logging is configured by `app.utils.logger.setup_logger` with a standard
  format; use `logger.info` or `logger.error` accordingly.

- Familiarize yourself with `utils/security.py` for password hashing and
  authentication logic if modifying auth routes.

## Cross-Component Communication

- The frontend JavaScript talks to endpoints under `/api/`. Responses are JSON
  objects with `id`, `username`, `role`, etc. Error cases often return
  `{'msg': '...'}.` Frontend expects this format when displaying alerts.

- JWT claims are passed via Authorization header `Bearer <token>`. Expiry
  handling is done client-side by inspecting the `exp` claim in the base64
  payload.

- The app writes audit logs synchronously within route handlers; there is no
  asynchronous queue.

## Missing Pieces and Gaps

- There are no automated tests or lint configurations.
- Migrations are not applied automatically; the repo uses `db.create_all()`.
- The demo page uses hardcoded values and should not be modified to rely on
  backend APIs.

---

Feel free to ask for clarifications or details about any part of this
structure!
