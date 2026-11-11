---
name: "interrogatorio-encargo"
description: "Fase F0a del harness de estudios de mercado: interroga al solicitante una pregunta por vez antes de extraer datos y deja decisiones.md y encargo.yaml cerrados."
---

# Interrogatorio del encargo (F0a)

Adaptado de `grilling` / `grill-with-docs` de Matt Pocock (MIT). Se ejecuta antes de F0 en todo estudio de mercado. Sin las decisiones obligatorias aplicables cerradas no arranca la producción; el trabajo preliminar sí puede avanzar (regla 6).

v2.1 · 2026-10-25 · lecciones del estudio global de plantillas, corregidas con la revisión adversaria de Astra (hallazgos 2, 3, 4, 7, 13, 14).

## Principio rector (CEO, 2026-09-25)

Cada dato debe servir para priorizar y definir estrategia y acción. Lo que no cambia una decisión no entra. Toda pregunta, campo o tarea se justifica por la decisión que alimenta.

## Reglas

1. Árbol de decisiones: cada decisión abre las que dependen de ella. Antes de abrir una rama, registrar `aplica / no_aplica` y motivo.
2. Una sola pregunta o solicitud de insumo por turno (preferencia del CEO). Elegir la de la frontera con más decisiones colgando.
3. Tabla de opciones con columna MOTIVO y recomendación solo cuando hay alternativas reales. Para pedir un insumo basta una línea con para qué sirve.
4. Al recibir respuesta: confirmar en una línea ("✅ Qn cerrada: …"), registrar en `decisiones.md` con quién decidió y fecha, pasar a la siguiente.
5. Si la respuesta agrega un matiz ("A, pero…"), incorporarlo como decisión derivada (ej. 5b) y explicar en una tabla cómo queda.
6. **Quién obtiene los hechos.** Claude define decisiones, valida evidencia y analiza. Puede hacer verificaciones públicas puntuales (una norma, un registro, una cifra) para cerrar una pregunta. La recolección en volumen se delega a obreros con el skill `orden-obrero`. Antes del cierre se permiten inventario de insumos, prototipos mínimos y órdenes preliminares de verificación con alcance, destinatario y salida definidos; no inician la recolección productiva. Nunca preguntar al usuario algo que se puede averiguar.
7. **Insumos del CEO.** Antes de pedir, revisar los archivos autorizados que ya existen (proyecto, carpetas conectadas). Mantener un único registro por insumo con: decisión que alimenta, tarea dependiente y estado `recibido_validado | pendiente | no_disponible | pasó_a_decisión | no_aplica`. Pedir uno por turno, empezando por el que más pesa. Los pendientes bloquean solo las tareas que dependen de ellos. Si el usuario dice que un dato lo define él, pasa a decisión. Tener el CEO una versión de un dato no impide verificarlo de forma independiente.
8. Decisiones son del usuario: presentarlas y esperar respuesta.
9. Si el usuario pide evaluar factibilidad antes de decidir, hacerlo con verificación preliminar (regla 6) y mostrar estado (verificado | estimado | pendiente) antes de repetir la pregunta.
10. Pregunta no resoluble hablando (formato, apariencia de la herramienta): construir prototipo mínimo y reaccionar sobre él.
11. Conocimiento de un tercero (fabricante, clientes): pedirlo al CEO solo si tiene el documento; si no, preparar cuestionario para ese tercero (ordenado por importancia, una idea por pregunta) sin enviarlo.
12. Cierre: frontera vacía, resumen de decisiones con los riesgos materiales señalados una sola vez, y confirmación explícita del usuario. No se pide reconfirmación aparte por haber aceptado recomendaciones. El cierre bloquea solo la producción que depende de decisiones abiertas.

## Formato de pregunta (cuando hay alternativas)

```
✅ **Q(n-1) cerrada: <resumen en una línea>**

---

❓ **Qn · <título>**

| Opción | Cómo | MOTIVO |
|---|---|---|
| **A. …** | … | … |
| B. … | … | … |

➡️ Recomiendo **X**. <precisiones si hacen falta>

¿A o B?
```

## Núcleo del árbol (todo estudio)

| # | Decisión | Depende de | Por defecto |
|---|---|---|---|
| 1 | Decisión que resuelve el estudio (comercial / tamaño / prospección / posicionamiento de marca / plan) | — | ninguno: obligatoria |
| 2 | Unidad comercial y de análisis: producto, especificación, lote, contrato, periodo, alcance; segmentos | 1 | ninguno: obligatoria |
| 3 | Perímetro: países y canales, con lista versionada; cambios de perímetro van a `CAMBIOS_ALCANCE` | 1 | ninguno: obligatoria |
| 4 | Priorización: método pertinente a la decisión (matriz atractivo × capacidad, cuadrantes, ranking) o no_aplica | 1 | matriz si la decisión es elegir dónde o con quién |
| 5 | Formato de salida: artefacto mínimo aceptado y un solo glosario navegable (resolver con prototipo) | 1, 4 | el artefacto que el CEO ya usa |
| 6 | **Marco de datos** (ver abajo) | 1, 3 | ver tabla |
| 7 | **Insumos del CEO** (regla 7) | 1 | registro con estados |

## Perfiles sectoriales (activar solo si aplican)

| Perfil | Decisiones que agrega | Cuándo |
|---|---|---|
| Dotación / EPP | Regla de reposición (piso, norma, vida útil); cobertura de la norma; estratos formal grande / pyme / informal y tratamiento del informal | Calzado de seguridad u otro producto cuya compra la fija una norma |
| Fabricante representado | Producto en dos capas: tipo genérico (compartible) + tabla CEO-ONLY del fabricante | Cuando hay catálogo o precios propios del fabricante |
| Consumo en retail | Bandas de precio, canales, marcas comparables | Producto de consumo en tiendas y marketplaces |
| Servicios / B2B industrial | Unidad por contrato, periodo y alcance; o especificación, lote y condiciones | Cuando no hay precio de góndola |

## Marco de datos (decisión 6)

| Elemento | Qué se fija | Por defecto |
|---|---|---|
| Comparación | Nominal entre monedas, relativa dentro de cada mercado, o ambas | Relativa dentro del mercado; nominal solo si la decisión compara precios entre países |
| Tipo de cambio | Si aplica: el obrero entrega tabla pública con moneda origen y destino, dirección, tasa, fecha efectiva, fecha de consulta y fuente; se conservan los valores originales | `no_aplica` si la comparación es solo relativa |
| Comparabilidad | Regla de equivalencia (producto o especificación, presentación, canal, condición comercial) y cuotas solo si cambian la decisión | Equivalencia declarada; sin cuota fija |
| Vocabularios | Códigos de país, canales y tipos, con correspondencia al texto original | ISO 3166 alfa-2 + listas del estudio, versionadas |
| Fuentes internas | Por fuente: finalidad, alcance autorizado, fecha y referencia de autorización. Permiso de lectura no habilita exportación | Ninguna operativa (MWT ONE, contabilidad) salvo autorización registrada |
| Datos pagos | Presupuesto y autorización de gasto, separados | USD 0; los obreros solo declaran hipótesis de cierre |

Hechos que nunca se preguntan: fuentes públicas, normas, datos de empleo e importación, precios públicos.

## Trazabilidad del entregable

1. Cada afirmación material referencia evidencia puntual, fecha efectiva y fecha de consulta.
2. Un solo glosario navegable en el artefacto elegido: cada concepto con nombre propio, definición, dónde está y qué decisión alimenta.
3. Ningún nombre inventado aparece sin estar en el glosario.
4. Si hubo conversión de moneda, la tabla de tipos de cambio usada queda visible.

## Salida

1. `decisiones.md`: id del estudio, versión, y una fila por decisión con: número, decisión, opción, MOTIVO, autor, fecha, estado (cerrada / por defecto / no_aplica) y aplicabilidad. Guardar en el proyecto MWT KB (`claude/<dominio>/F0A_DECISIONES_<tema>_<fecha>.md`). Un archivo de instrucciones operativas no sustituye este acta.
2. `encargo.yaml`: con las mismas claves (id, versión, decisiones, aplicabilidad, `marco_datos`, perímetro versionado). F0 valida campo por campo y emite reporte de campos aceptados y rechazados; si falta el acta válida, se detiene solo la producción dependiente.
3. `insumos_ceo.md`: el registro único de la regla 7.
4. `cuestionario_<tercero>.md` si aplica la regla 11 (no se envía sin decisión del CEO).
5. Las órdenes a obreros se redactan después con `orden-obrero`, a partir de un contrato público derivado del encargo, nunca leyendo el encargo completo.

## Formato de respuesta

Español. Frases cortas. Tablas con MOTIVO solo para opciones reales. Cada dato con estado: verificado | estimado | pendiente. Sin jerga ni lógicas implícitas.