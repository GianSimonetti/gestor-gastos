---
name: conventional-commit
description: Crea commits o genera mensajes de commit con Conventional Commits cuando el usuario pide crear, hacer o generar un commit, o redactar o generar su mensaje.
---

# Conventional Commit

Antes de decidir el mensaje, inspeccioná exclusivamente lo preparado para el commit con `git diff --staged`. Si no hay cambios staged, detenete y avisá; no inventes el mensaje ni prepares archivos automáticamente.

Elegí el tipo que mejor represente esos cambios:

- `feat`: agrega una capacidad.
- `fix`: corrige un comportamiento.
- `docs`: modifica documentación.
- `refactor`: reorganiza código sin cambiar su comportamiento.
- `test`: agrega o modifica pruebas.
- `chore`: realiza mantenimiento o tareas auxiliares.

Usá `tipo(scope): descripción` cuando un scope breve identifique claramente el área afectada; en otro caso, usá `tipo: descripción`.

La descripción debe estar en minúscula, ser breve e imperativa, no terminar en punto y tener como máximo 72 caracteres. No uses textos genéricos como `cambios`, `update` o `arreglos`.

Si hay un cambio incompatible, agregá un cuerpo separado por una línea en blanco con `BREAKING CHANGE: <detalle>`.

Si el usuario pidió solo el mensaje, devolvelo sin crear el commit. Si pidió crear el commit, usá exactamente el mensaje resultante y no hagas push.
