## Propósito
Aplicación web responsive para que cada usuario autenticado administre sus gastos, participantes, dinero disponible y ahorros.
Permite crear tableros e incluir mediante código a otros usuarios o agregar participantes sin cuenta.

## Stack
- Frontend: React; paquetes gestionados con npm.
- Backend: Python 3.12, FastAPI y JWT; dependencias gestionadas con uv.
- Datos: SQLite y SQLAlchemy; evaluar Supabase si fuera necesario.
- Audio: pendiente de definir.
- Tests backend: pytest.

## Cómo correr
- Instalar backend: `cd backend && uv sync`.
- Levantar backend: `cd backend && uv run uvicorn app.main:app --reload`.
- Instalar frontend: `cd frontend && npm install`.
- Levantar frontend: `cd frontend && npm run dev`.
- Tests backend: `cd backend && uv run pytest`.
- Build frontend: `cd frontend && npm run build`.

## Qué NO hacer
- No implementar funcionalidades fuera del alcance solicitado, aunque aparezcan definidas en el PRD.
- No integrar automáticamente bancos, tarjetas, billeteras virtuales ni Mercado Pago.
- No crear aplicaciones móviles nativas para iOS o Android.
