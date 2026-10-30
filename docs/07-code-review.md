# Sección 7 — Code review con checklist

> Texto destinado al **informe PDF**.

## 7.1 Enfoque

Se aplicó una **checklist de revisión de código** sobre el estado
`estado-refactorizado`, con criterios verificables (no opiniones): cada ítem
tiene un estado, una evidencia y un comentario. La checklist cubre legibilidad,
estructura, reglas de negocio, pruebas y documentación.

**Métricas del estado revisado:**

| Archivo | Líneas | Rol |
|---|---|---|
| `src/servicios.py` | 204 (antes: 285) | Lógica de negocio |
| `src/repositorio.py` | 54 | Persistencia JSON |
| `src/requisitos.py` | 17 | Regla de documentos por tipo |
| `src/constantes.py` | 10 | Estados y códigos de retorno |
| `src/modelos.py` | 19 | Entidades |
| `src/main.py` | 21 | Demostración |
| `tests/test_solicitudes.py` | 94 | 11 pruebas |

## 7.2 Checklist de revisión

| # | Criterio | Estado | Evidencia / comentario |
|---|---|---|---|
| 1 | ¿Los nombres describen la intención? | ✅ | `buscar_solicitud`, `faltantes`, `RequisitosDocumentales`; quedan `puede` (línea ~96) y `f` en el repositorio como deuda menor |
| 2 | ¿Hay código duplicado? | ✅ | El bloque de búsqueda (5 copias) quedó en `buscar_solicitud()`; sin duplicación evidente |
| 3 | ¿Cada método hace una sola cosa? | ⚠️ | `aprobar()` todavía imprime, valida, persiste y decide; se mejoró (perdió 16 líneas con el Parameter Object) pero no está resuelto del todo |
| 4 | ¿Las reglas de negocio tienen una única fuente de verdad? | ✅ | Documentos por tipo: `RequisitosDocumentales.REQUISITOS`; estados: `constantes.py`; transiciones: aún en `cambiar_estado()` (ver ítem 10) |
| 5 | ¿Los magic numbers están eliminados? | ✅ | `RESULTADO_*` y `ESTADO_*` en `constantes.py`; no quedan `-1/-2` ni strings de estado sueltos |
| 6 | ¿La persistencia está separada del negocio? | ✅ | `RepositorioSolicitudes` (Move Method); el servicio no importa `json` ni `os` |
| 7 | ¿Las pruebas automatizadas existen y pasan? | ✅ | `py -m unittest discover -s tests` → 11/11 OK |
| 8 | ¿Se cubren caminos de error? | ✅ | Legajo inexistente, tipo inválido, solicitud inexistente, doble resolución, transición inválida |
| 9 | ¿El README permite a alguien nuevo ejecutar el proyecto? | ✅ | Incluye comando, estructura, tags y declaración de IA |
| 10 | ¿La matriz de transiciones es modificable sin riesgo? | ❌ | `cambiar_estado()` (servicios.py) sigue con `if/elif` anidados: smell #8 pendiente |
| 11 | ¿Las entidades expresan su comportamiento? | ❌ | `modelos.py` sigue siendo Data Class (smell #6): la lógica vive en el servicio |
| 12 | ¿La persistencia está probada? | ⚠️ | No tiene tests propios (requeriría `tempdir`); documentado como deuda consciente |

## 7.3 Hallazgos de la revisión

**Fortalezas verificables:**
- Los 4 refactorings exigidos aplicados y verificados con salida idéntica.
- 11 pruebas automáticas en verde que cubren las 6 operaciones.
- Reglas de negocio centralizadas (requisitos y estados) en un solo lugar.
- Estructura modular: 7 archivos con responsabilidades identificables.

**Deuda pendiente consciente (3 hallazgos abiertos):**

| Hallazgo | Riesgo | Decisión |
|---|---|---|
| #10: matriz de transiciones con `if/elif` | Alto si cambian las reglas | No se refactorizó: fuera del alcance mínimo exigido (4 refactorings) y priorizaron los smells de mayor riesgo |
| #11: entidades Data Class | Medio | Igual que el anterior; exige rediseñar el modelo |
| #12: persistencia sin tests | Bajo para este alcance | Se documenta como mejora futura |

**Conclusión de la revisión:** el código cumple los criterios esenciales de
calidad interna tras el refactor; los 3 hallazgos abiertos están
documentados, justificados y con riesgo acotado. Ninguno afecta la
funcionalidad observable del sistema.

## 7.4 Reproducción de la revisión

```bash
py -m unittest discover -s tests -v   # 11/11 OK
py src/main.py                        # demostración completa
git log --oneline                     # trazabilidad por etapa
git diff estado-inicial estado-refactorizado --stat
```
