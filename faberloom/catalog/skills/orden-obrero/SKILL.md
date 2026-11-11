---
name: "orden-obrero"
description: "Redacta órdenes cerradas para Kimi Swarm, DeepSeek y Astra y recibe sus entregas; usar después de interrogatorio-encargo en todo estudio de mercado."
---

# Orden a obrero (F1) y recepción de la entrega (F2)

v1.2 · 2026-10-28 · agrega los módulos «Paquete de entrega» y «Modelo económico» para Astra, el límite de una revisión adversaria por versión y la verificación de hallazgos antes de aplicarlos (REV-BR-02 y 03, FootMaster Brasil).
v1.1 · 2026-10-25 · nace de las lecciones del estudio global de plantillas; corregido con la revisión adversaria de Astra (hallazgos 1–12, faltantes 1–12). Estructura: núcleo común en toda orden + módulos que se activan solo si cambian una decisión.

| Obrero | Para qué | Dónde corre |
|---|---|---|
| Kimi K2.6 Swarm | Investigación masiva: censos, precios por país y canal, identidad de marcas | Kimi Work, carpeta que fije la orden |
| DeepSeek | Extracción mecánica de fuentes fijas: APIs, páginas dadas, archivos | PC del CEO, `C:\Users\alvar\Documents\<estudio>\...` |
| Astra (ChatGPT / Codex) | Auditoría adversaria por riesgo material; revisión de paquetes antes de enviarlos a un tercero | `C:\Users\alvar\Documents\Codex\<fecha>\...` |

## Requisitos previos

1. **Acta válida.** `decisiones.md` y `encargo.yaml` pasan la validación de F0 (id, versión, decisiones aplicables cerradas, perímetro). La orden cita esa versión. Si falta, se detiene solo la producción dependiente; se pueden emitir órdenes preliminares de verificación.
2. **Insumos.** Registro de insumos del CEO al día (regla 7 del interrogatorio). Una orden no pide al obrero un dato que el CEO ya entregó validado, salvo que el objetivo sea verificarlo de forma independiente.
3. **Contrato público.** Antes de redactar una orden externa, construir un contrato público con lista explícita de campos permitidos. Excluir datos CEO-ONLY, sus valores derivados y anexos restringidos. El permiso de consulta interna no autoriza exportación. Validar el texto final y sus adjuntos contra la clasificación; si hay duda sobre un campo, omitirlo y registrar la omisión sin reproducir su valor. Si el CEO autoriza expresamente que el obrero lea material CEO-ONLY, la orden lo rotula, prohíbe copiar sus valores a textos para terceros y exige que el análisis vaya en una sección final marcada CEO-ONLY.

## Núcleo de toda orden

1. **Encabezado:** obrero, número, fecha, versión del encargo, rol con verbos de la tarea (extraer, investigar o auditar).
2. **Para qué sirve:** decisión que alimenta, en 2–3 líneas.
3. **Alcance:** perímetro versionado; vocabularios cerrados con correspondencia al texto original (país ISO 3166 alfa-2, canales, tipos, macro mercado según el estudio). Listas declaradas como cerradas o ejemplificativas.
4. **Cambios de alcance:** un candidato material no previsto (ej. una plataforma dominante fuera de la lista) se registra en `CAMBIOS_ALCANCE.csv` con evidencia, impacto y tareas dependientes. No se incluye ni se descarta en silencio; las tareas independientes siguen.
5. **Unidad y equivalencia:** unidad de observación, marco muestral y regla de equivalencia (producto o especificación, presentación, canal, condición comercial). Cuotas solo si cambian la decisión; la disponibilidad desigual se reporta como hallazgo, no se rellena.
6. **Esquema:** columnas en orden con tipo y unidad. Toda fila lleva `id_observacion, id_censo, ronda, criterio_seleccion`. Toda afirmación material lleva `id_evidencia`, fuente, fecha efectiva y fecha de consulta. La confianza (A/B/C, definición versionada en la orden) va por afirmación cuando identidad, existencia, importe, unidad o vigencia tienen evidencias distintas.
7. **Tres archivos:** `DATOS.csv` (observaciones identificadas; campos ausentes como nulos tipados), `FALTANTES.csv` (faltante por id_observacion y campo) y `COBERTURA.csv` (consulta, universo consultado, fecha, evidencia, estado `sin_resultados_online | bloqueado | no_relevado`). No se crea una observación para decir que no se encontró nada. "Sin resultados online" no es "canal vacío".
8. **Transformaciones:** separar dato crudo, normalización, controles y análisis. La orden enumera las fórmulas y sumas de control permitidas; lo demás está prohibido.
9. **Prohibido:** inventar, interpolar, rellenar un rol con otro (vendedor ≠ escaparate ≠ titular ≠ fabricante ≠ importador ≠ distribuidor), deducir cantidad por imagen o importe, evadir bloqueos, usar sesión autenticada o cambiar preferencias de cuenta sin autorización registrada, usar fuentes internas no autorizadas.
10. **Entrega congelada:** carpeta exacta; manifiesto generado desde los archivos (filas por capa, dominio, estado y origen) con hash; ledger de correcciones (id, valor original, regla, valor nuevo, evidencia); `ENTREGA.md` con la plantilla de abajo, regenerada si cambian los datos.
11. **Aceptación:** reporte de pruebas ejecutadas (tipos, unidades, URL que corresponde al producto, cuadre manifiesto–datos–relato). Un checklist marcado no sustituye resultados. Si inventario, consolidado y relato no cuadran, la entrega se rechaza.

## Módulos (activar solo si aplican)

| Módulo | Se activa cuando | Reglas |
|---|---|---|
| **Precios** | El estudio usa importes | `tipo_importe = exacto | desde | rango | cotizacion`, variante, vendedor, unidad comercial, cantidad mínima, condición o promo. Separar producto, envío e impuestos si se identifican. Un "desde" sin variante comparable no entra en bandas ni medianas. Unidad: `unidad_analisis, unidad_envase, cantidad_unidades_analisis` con evidencia textual; sin cantidad no hay importe unitario; dos piezas complementarias no son dos unidades. Precio en moneda local + `moneda` ISO 4217; moneda mostrada distinta del mercado objetivo se conserva y se señala. |
| **Varios dominios / marketplaces** | Se observan dominios que pueden compartir catálogo (ej. Amazon.sa y Amazon.ae) | Registrar `pais_destino, dominio_observado, pais_oferta, id_producto, vendedor, presentacion, moneda_visible`. Coincidencias disparan revisión, no fusión. Si vienen de la misma oferta sin evidencia local independiente: `grupo_dependencia`, fuera del conteo independiente por mercado. |
| **Varios censos** | Hay que combinar fuentes con criterios distintos | No concatenar para estimar una distribución común. Conservar `id_censo`, criterio y unidad; construir estratos equivalentes o presentar separado. Toda armonización declara inclusiones, exclusiones, deduplicación, ponderación y sensibilidad. |
| **Identidad** | Propiedad, contraparte o grupo económico afectan el resultado | Roles separados con fuente, fecha y alcance (registros de marca USPTO/EUIPO/WIPO/INPI, sanitarios INVIMA/ANVISA/COFEPRIS/DIGEMID, tributarios, aduanas). No inferir identidad por nombre parecido ni por dos fuentes que copian el mismo registro. |
| **Navegador** | Falta evidencia por bloqueo, renderizado o respuesta vacía | Escalar con presupuesto y criterio de parada. Registrar país objetivo, moneda mostrada, estado anónimo o autenticado (sin datos personales). Cambio de cuenta autorizado: estado inicial, cambio y restauración comprobada. Sin acceso: declarar el límite, nunca inferir ausencia. |
| **Extracción fija / API** | DeepSeek sobre fuente fija | Adaptador por fuente: paginación, límite, particionado, campos estimados y cobertura conceptual. Respuesta exitosa no prueba completitud. `consultas.csv` y `log.md` que cuadren; advertencias de alcance (ej. partida arancelaria aproximada) viajan al manifiesto y a toda conclusión. |
| **Auditoría** | Hay afirmaciones materiales con riesgo | Muestra reproducible (id, semilla, estratos) dimensionada por heterogeneidad y materialidad; resultados correcto / error / no_verificable con denominadores total y verificable. Cada corrección propuesta se valida antes de aplicarse; reauditar filas corregidas y el estrato con error sistemático. No se encadena otra auditoría por defecto. |
| **Datos pagos** | Un hueco podría cerrarse pagando | Consulta requerida, cobertura comprobada, requisitos de acceso, fecha y límites. Lo no probado se rotula hipótesis de cierre. No contratar; la autorización de gasto es aparte. |
| **Paquete de entrega** | Piezas listas para salir a un tercero (`entrega-tercero`) | Tareas en orden de riesgo: (1) acuerdo de protección: ejecutabilidad en la jurisdicción de la contraparte y fidelidad cláusula por cláusula entre idiomas; (2) coherencia: cifras de la pieza contra el modelo, compromisos anteriores (juicios, revisiones) cumplido / parcial / incumplido con cita; (3) correo: orden, pedidos, coherencia con la secuencia; (4) consultas a especialistas: idioma, preguntas faltantes, preguntas que inducen la respuesta; (5) material CEO-ONLY autorizado en sección final aparte; (6) veredicto `ENVIAR | ENVIAR CON CAMBIOS | NO ENVIAR`, lo que bloquea separado de lo que puede esperar, y secuencia de envío. Entrega: `INFORME`, `HALLAZGOS.csv` (`id, pieza, ubicacion, cita, veredicto, severidad(bloquea/importante/menor), propuesta, fuente_url, fecha_consulta`), redline bilingüe solo donde cambia, correo propuesto completo, `ENTREGA.md`. Revisión técnica, no asesoría legal: lo que solo confirma un abogado se rotula. |
| **Modelo económico** | La pieza trae un modelo o panel con código | Extraer el motor y ejecutarlo con los valores por defecto; reproducir cada cifra publicada y la identidad del puente contable; probar casos límite (aprobaciones desmarcadas, una marca fuera, demanda baja, crédito largo); listar diferencias entre vistas (pública y privada) por supuesto y por resultado; revisar que nada privado esté cargado en la vista pública aunque esté oculto. |

Para Astra: rol adversario, qué atacar en orden de importancia, veredictos `SOSTIENE | DEBILITA | REFUTA | NO_VERIFICABLE` con cita, y los artefactos que pida su orden específica.

**Límite de revisiones.** Una revisión adversaria por versión que sale de MWT. Una segunda solo si la primera encontró bloqueos y estos cambiaron el texto material. El juicio (`SKILL_COURT`) se reserva para decisiones del CEO discutibles, no para pulir.

## Plantilla de ENTREGA (la escribe el obrero)

```
# ENTREGA — <estudio> · <versión del encargo> · <fecha> · <obrero>
1. Decisiones que alimentan estos datos
2. Manifiesto generado: carpeta, archivo, hash, filas por capa, dominio, estado y origen
3. Método: rondas, módulos activados, auditoría (muestra, denominadores, resultados), ledger de correcciones
4. Criterio de confianza usado (versión)
5. Sesgos y dependencias vigentes, con su efecto operativo por id
6. Cobertura y faltantes; hipótesis de cierre con datos pagos
7. Cambios de alcance pendientes de decisión
8. Pruebas de aceptación ejecutadas y resultado
```

## Recepción de la entrega (Claude)

1. Cuadrar manifiesto, parciales y consolidado; revisar entradas, salidas y reemplazos.
2. Aplicar solo correspondencias y cálculos aprobados y reversibles, conservando el dato crudo y el diff. Discrepancias de unidad, rol o evidencia vuelven al obrero, registradas por id.
3. Convertir moneda solo si el marco lo pide, con la tabla pública recibida.
4. Comparar entre mercados solo observaciones equivalentes; una mediana de muestra no es una mediana de mercado. Mostrar sensibilidad por marco, tipo y canal.
5. Cotejar contra su evidencia todas las afirmaciones que sostienen decisiones, también las de confianza A o B: abrir la fuente y confirmar que dice lo citado. Reabrir una fuente para cotejar es validación; extraer datos nuevos es otra orden.
6. Pedir auditoría a Astra cuando el riesgo material lo justifique, con orden específica de este skill.
7. **Hallazgos de una revisión:** antes de aplicar, verificar cada hallazgo que cambia una decisión (abrir la fuente primaria o reproducir el código). Presentar al CEO una tabla: hallazgo, verificado / no verificable, qué hago. Adoptar la redacción del obrero cuando es mejor que la propia y decirlo. Lo que no se pudo verificar queda rotulado para el especialista, no se aplica como hecho.

## Formato

Español. Órdenes cortas, en tablas cuando hay listas. Nombres de archivo y carpetas exactos. Activar solo los módulos que cambian una decisión: cada campo exigido debe alimentar una decisión o permitir una prueba de cumplimiento.