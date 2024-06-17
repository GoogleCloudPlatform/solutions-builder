# Changelog

## 2.0.0

### Refactor CLI structure

- Changed `sb component add` to `sb new component ...` commands.
- Added `sb terraform *` as alias of `sb infra *` commands.
  - `sb terraform apply --all` to init an apply all terraform stages.
- Added `sb init` to restore `sb.yaml`.
- Added `sb replay` to re-install components according to a `sb.yaml` file.
- Added template path supports for local folder and remote Git repo.
- Updated `sb new` to support external path.
- Updated template_root to load other modules dynamically.

### Misc updates

- Added support for Python 3.10.x, 3.11.x
- Moved `task_dispatch_service` to `experimnets` folder.

## 1.18.0

- Adding support for Python 3.11.x
- Upgraded Copier to >=9.2.0
- Migrated from `run_auto` to both `run_copy` and `run_update`.
- Updated `blank_service` template with a sample API endpoint in FastAPI.
- Misc fixes in CLI.
