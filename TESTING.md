## Testing

### Backend (pytest)

Run:

```bash
cd backend
uv sync --extra dev
uv run pytest
```

Markers:

```bash
uv run pytest -m unit
uv run pytest -m integration
```

### Frontend (Vitest)

Run:

```bash
cd frontend
npm install --ignore-scripts
npm run test
npm run lint
```

