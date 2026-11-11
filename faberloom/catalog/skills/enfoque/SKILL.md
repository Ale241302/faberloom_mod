---
name: "enfoque"
description: "Revisa un encargo antes de ejecutarlo para encontrar lo que cambia el resultado y termina en un prompt ejecutable. Usar al invocar /enfoque."
---

# Enfoque

Revisa el encargo antes de ejecutarlo. Busca una mejora que cambie el resultado, no más trabajo. Puedes inspeccionar el material en solo lectura. No ejecutes ni modifiques nada, y no descargues nada de los buzones del usuario sin pedírselo primero.

## Identificar el encargo

- Toma el encargo del texto que acompaña a `/enfoque`.
- Si no hay texto o dice "la última que trabajamos", usa la tarea más reciente de esta conversación.
- Si en esta conversación no hay ninguna, búscala en los chats anteriores. Si sigue sin estar clara, pregunta cuál es y detente.

## Revisión

1. **Uso y riesgo.** Para qué servirá el resultado y qué pasa si está mal. Si hay poca incertidumbre y las consecuencias son menores o reversibles, dilo y pasa al prompt final.
2. **Oficio.** En una línea, qué profesional concreto haría este trabajo y qué haría distinto.
3. **Cambios decisivos.** Máximo 3 en total, cada uno con la decisión o el resultado que cambia. Revisa siempre qué quitar; si no sobra nada, dilo.
4. **Evidencia.** Qué material crudo hace falta, cuál inspeccionaste y cuál falta. Señala los hechos decisivos con su respaldo, los supuestos importantes y lo desconocido.
5. **Comprobación y límite.** Cómo aceptar el resultado, con una prueba que pueda fallar por motivos distintos a los del proceso de producción. Qué no podrá comprobarse todavía y cuándo dejar de profundizar.

## Cierre

Termina con un prompt ejecutable en un bloque de código: objetivo original, material, pasos mínimos, criterio de aceptación, límite de esfuerzo y punto exacto del visto bueno. Señala cualquier cambio de objetivo. No inventes requisitos, datos ni umbrales.

Detente ahí y espera el visto bueno. No ejecutes el prompt en este mismo paso.
