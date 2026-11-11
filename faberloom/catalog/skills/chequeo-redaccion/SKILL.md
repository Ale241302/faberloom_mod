---
name: "chequeo-redaccion"
description: "Revisar un texto antes de entregarlo o publicarlo (correo, listing, A+, empaque, redes, informe): separa lo que bloquea, lo que se sugiere y lo que no se toca."
---

# Chequeo de redacción

Revisar un texto antes de que salga. El objetivo es encontrar dos cosas: lo que **no puede salir** (un claim sin respaldo) y lo que **suena a escrito por IA** (fórmulas, relleno, cierres que resumen, adjetivos sin respaldo).

Este chequeo no reescribe por su cuenta la voz de una pieza. Las decisiones de marca son del CEO aunque no estén en la KB. Un revisor que borra lo que no entiende destruye posicionamiento.

## 1. Establecer el tipo de pieza primero

El tipo define el rigor y quién decide. No arrancar sin saberlo.

| Tipo | Ejemplos | Modo |
|---|---|---|
| Marketing | Listing, A+, empaque, redes, landing, eslogan | **Flexible.** Lo de estilo solo se sugiere; decide el CEO |
| Correo / mensaje | Correo B2B, WhatsApp, respuesta a review | Estilo se aplica directo (el CEO revisa el borrador completo igual) |
| Informe / doc | Informe, memo, estudio, one-pager | Estilo se aplica directo, con el pase humanizador de `presentar-resultados` |
| Texto de búsqueda | Título Amazon, search terms backend | Solo nivel Bloquea. Las reglas de voz no aplican |

En marketing, parte del trabajo es evocar y posicionar. Un adjetivo sin cifra en un informe es relleno; en un listing puede ser la marca hablando.

## 2. Tres niveles

Cada hallazgo lleva un nivel. Nunca se mezclan.

| Nivel | Qué cubre | Cómo actúa |
|---|---|---|
| **Bloquea** | Claim sin fuente, claim médico, cifra de rendimiento, palabras prohibidas por compliance ("tested", "certified", "rated", "guaranteed"), marca de tercero sin atribución, contradicción entre partes de la pieza | Corrige o frena. No negociable |
| **Sugiere** | Estilo: eslogan genérico, repetición, adjetivo sin respaldo visible, fórmula de IA, cierre que resume | En marketing: propone con motivo y **no aplica**. En correo e informe: aplica |
| **No toca** | Decisiones de marca (ver §3) | Ni se marca |

## 3. Lo que no se toca

- **Posicionamiento declarado.** Ejemplo: Costa Rica como "one of Latin America's advanced engineering ecosystems".
- **Eslóganes y taglines aprobados**, estén en el texto o en las imágenes. Ejemplo: "Built for the ones who never sit down".
- **Marcas técnicas y lo que implican.** ThinBoom™, LeapCore™, NanoSpread™, Arch System™, PORON® XRD®. La marca técnica ya contiene su especificación. Un adjetivo junto a una marca técnica ("responsive ThinBoom™") se valida contra la ficha de esa tecnología. **Nunca** se agrega el material al copy ("supercritical TPU") para respaldar el adjetivo.
- **Atenuaciones que exige compliance.** "Designed to help", "individual results vary", notas de desgaste, "material data, not a test of the finished insole". No se tratan como rodeos.
- **Decisiones CEO registradas** en el documento de la pieza (tabla de revisión, reglas aplicadas).

Fuentes de esta lista: `SKILL_HUMANIZE_BRAND` (voz, taglines), `POL_NUNCA_TRADUCIR` (marcas técnicas), `ENT_COMP_CLAIMS` y `POL_CLAIMS_SCANNER` (atenuaciones), y el propio documento de la pieza.

## 4. Regla del dato ausente

Si algo parece no tener respaldo, primero buscarlo en la KB. **Si no está, se pregunta; no se borra.** Que no esté en la KB no significa que no exista. Excepción: un claim de rendimiento o de salud sin fuente es nivel Bloquea hasta que aparezca la fuente.

## 5. Chequeos

### Capa 1 — automáticos (todos los tipos salvo texto de búsqueda)

La lista vive en `POL_ANTIPATRONES_REDACCION` (KB, `kb/4_gobernanza/POL_/`; en esta PC: `C:\Users\ale13\OneDrive\Documents\DeepSeek-Harnees\mwt-knowledge-hub\kb\4_gobernanza\POL_\`, donde ese archivo **todavía no está**). Es la misma lista que usan las skills que redactan (`SKILL_HUMANIZE_COMMS`, `SKILL_HUMANIZE_BRAND`). No mantener una lista aparte aquí: si aparece un patrón nuevo, se da de alta en la POL.

1. **Pasada determinista.** Correr el script sobre el texto:
   `python C:\Users\ale13\OneDrive\Documents\DeepSeek-Harnees\mwt-knowledge-hub\scripts\check_redaccion.py --tipo <correo|informe|marketing> <archivo>`
   Ese script **no existe en esta PC**: la carpeta `scripts` del hub tiene `check_claims.py` y `check_color.py`, pero no el de redacción. Si falta, aplicar la lista de la POL a mano y decirlo en el reporte.
2. **Confirmar lo marcado.** El script marca candidatos; el juicio confirma o descarta cada uno. Los patrones marcados "juicio" en la POL (tríada de adjetivos, oración que anuncia lo que la siguiente demuestra, metáfora sensorial) se revisan leyendo.
3. **Reportar con el id** del patrón (AP-E6, AP-C2) para que las correcciones se puedan contar.

Resumen de la lista (detalle, ejemplos y umbrales en la POL):

| Grupo | Ids | Umbral |
|---|---|---|
| Fórmulas: cortesía, relleno, cierre que resume, adverbio vacío, autopromoción | AP-F1 a AP-F6 | Cero |
| Estructura: "no es X, es Y", "donde X se encuentra con Y", tríada, oración >25 palabras, raya larga, gerundio de comentario al final, conectores en serie, negrita repetitiva, título en negrita que repite, anuncio y demostración, emojis, exclamación múltiple | AP-E1 a AP-E12 | Por patrón |
| Contenido: importancia inflada, atribución vaga o inferencia presentada como hecho, metáfora sensorial | AP-C1 a AP-C3 | AP-C2 es nivel **Bloquea** |

Coincidir con un patrón no prueba que el texto sea de IA. Los umbrales evitan prohibir de más.

### Capa 2 — preguntas cerradas por tipo

**Marketing**

| Pregunta | Nivel |
|---|---|
| ¿Cada claim de la descripción o del A+ está también en los bullets o en la ficha del producto? | Bloquea |
| ¿Aparece alguna palabra prohibida por compliance o algún claim médico fuera de donde lo permite `ENT_COMP_CLAIMS`? | Bloquea |
| ¿Toda comparación nombra contra qué compara? | Bloquea si es cifra o escaneo; Sugiere si es retórica |
| ¿La apertura es un eslogan que podría decir cualquier marca? (salvo que sea un eslogan aprobado) | Sugiere |
| ¿La misma idea aparece dos veces dentro del mismo bullet o párrafo? | Sugiere |
| ¿Hay metáfora sensorial sin dato ("feel the difference with every step")? | Sugiere |

**Correo**

| Pregunta | Nivel |
|---|---|
| ¿El punto está en la primera línea? | Sugiere (aplica) |
| ¿Anticipa la emoción del lector ("entiendo que esto puede afectar…")? | Sugiere (aplica) |
| ¿Promete algo sin fecha ni acción? | Sugiere (aplica) |
| ¿Cierra con un paso concreto, una fecha o una pregunta? | Sugiere (aplica) |
| ¿Apertura y cierre respetan el perfil de voz (`SKILL_HUMANIZE_COMMS`)? | Sugiere (aplica) |

No insertar imperfecciones intencionales ni conectores obligatorios: una imperfección fija por mensaje es en sí misma una firma de IA.

**Informe**

Aplicar la auditoría del hilo y el pase humanizador de `presentar-resultados`. En informes, afirmar la conclusión arriba es correcto: no se marca como sobreexplicación.

## 6. Formato del reporte

```
tipo: <marketing|correo|informe|búsqueda> · pieza: <nombre> · veredicto: PASA | BLOQUEADA (n) | PASA CON SUGERENCIAS (n)

BLOQUEA
  <dónde> — <texto> → <corrección> · <motivo y fuente>

SUGIERE  (marketing: decide CEO)
| Dónde | Actual | Propuesta | Motivo |

PREGUNTAS  (dato ausente en KB)
  <dónde> — <qué falta>
```

Lo que está en nivel No toca no aparece en el reporte.

Preguntar al CEO de a una pregunta, no en lista.

## 7. Después de la decisión

1. Aplicar solo lo aprobado.
2. Registrar en el documento de la pieza una tabla de revisión: antes, después, motivo y quién decidió.
3. Si el CEO rechazó una sugerencia porque era decisión de marca, agregar esa decisión a la lista de §3 del documento de la pieza. Si el CEO aportó un dato que faltaba (por ejemplo, el material de una marca técnica), anotar que debe entrar a la ficha del producto.

## Caso de referencia — listing Goliath, 2026-09-27

Pase hecho con criterio de informe sobre una pieza de marketing. Se aplicaron 5 cambios sin preguntar; solo 1 era obligatorio.

| Hallazgo | Nivel correcto | Qué pasó |
|---|---|---|
| NanoSpread "manage moisture and temperature" en la descripción; el bullet solo dice humedad | **Bloquea** | Correcto: se quitó "temperature" (claim sin fuente, contradicción con el bullet) |
| "one of Latin America's advanced engineering ecosystems" | **No toca** | Error: se borró. Era posicionamiento. CEO lo restituyó |
| "responsive" junto a ThinBoom™ | **No toca** | Error doble: se borró y después se agregó "supercritical TPU". ThinBoom™ ya es TPU supercrítico |
| "Built for the ones who never sit down" abriendo la descripción | **Sugiere** | Se cambió sin preguntar. CEO lo aprobó porque el eslogan ya va en las imágenes |
| "hold its shape" dos veces en el bullet 2 | **Sugiere** | Se cambió sin preguntar |
| "Same person… with Goliath" sin decir contra qué | **Bloquea** (es un escaneo) | Correcto: quedó como pregunta abierta |
| Título y backend | Solo **Bloquea** | Correcto: fuera del pase de voz. "best" en backend marcado para compliance/SEO |

Lección: en marketing el revisor no borra. Bloquea lo que compliance no permite y propone lo demás.