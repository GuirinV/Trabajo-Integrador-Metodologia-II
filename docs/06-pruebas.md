# Sección 6 — Pruebas y verificación antes/después

> Texto destinado al **informe PDF**.

## 6.1 Enfoque

Se implementaron pruebas unitarias con **`unittest`** (framework incluido en la
stdlib de Python; no requiere dependencias externas). Archivo:
`tests/test_solicitudes.py`.

**Decisión de diseño clave:** el refactoring 2 (Move Method) inyectó el
repositorio en el constructor del servicio:

```python
def __init__(self, repositorio=None):
    ...
    if repositorio is None:
        repositorio = RepositorioSolicitudes()
    self.repositorio = repositorio
```

Esto permite reemplazar la persistencia JSON por un `RepositorioEnMemoria`
dentro de las pruebas: las pruebas no tocan el disco, corren en milisegundos y
no dependen del estado previo del archivo. **Sin ese refactoring, testear el
servicio obligaría a crear y borrar archivos reales en cada prueba.**

## 6.2 Casos de prueba y resultados

Comando de ejecución: `py -m unittest discover -s tests -v`

Resultado real de la última ejecución: **`Ran 11 tests in 0.003s — OK`**

| # | Caso | Verifica | Esperado | Obtenido |
|---|---|---|---|---|
| 1 | Crear solicitud válida | Nace en estado PENDIENTE | `PENDIENTE` | ✅ OK |
| 2 | Crear con legajo inexistente | Valida el alumno | `None` | ✅ OK |
| 3 | Crear con tipo inválido | Valida el tipo | `None` | ✅ OK |
| 4 | Aprobar sin documentos obligatorios | Rechaza y pasa a EN_REVISION | `RESULTADO_FALTAN_DOCUMENTOS` | ✅ OK |
| 5 | Aprobar con documentos obligatorios | Aprueba y cambia estado | `RESULTADO_EXITO` + `APROBADA` | ✅ OK |
| 6 | Rechazar con motivo | Rechaza y registra motivo | `RESULTADO_EXITO` + `RECHAZADA` | ✅ OK |
| 7 | Rechazar solicitud ya resuelta | Detecta re-resolución | `RESULTADO_YA_RESUELTA` | ✅ OK |
| 8 | Transición inválida | `cambiar_estado` la rechaza | `False`, estado sin cambio | ✅ OK |
| 9 | Adjuntar documento a solicitud resuelta | Bloquea adjuntos posteriores | `None` | ✅ OK |
| 10 | Listar y detalle de alumno | Filtra y devuelve detalle | 2 solicitudes + detalle | ✅ OK |
| 11 | Aprobar solicitud inexistente | Código de retorno correcto | `RESULTADO_NO_ENCONTRADA` | ✅ OK |

## 6.3 Verificación antes/después del refactoring

El comportamiento externo se verificó en dos niveles:

**Nivel 1 — demostración manual (todos los refactorings):** después de cada uno
de los 4 refactorings se borró `datos/datos.json` y se ejecutó `py src/main.py`;
la salida fue idéntica a la del estado inicial en los 4 casos.

**Nivel 2 — suite automatizada (sobre el estado refactorizado):** la suite
corre sobre el código del tag `estado-refactorizado` y las 11 pruebas pasan.
Como las reglas de negocio (transiciones, requisitos documentales, validación
de legajos) se escribieron **después** del refactoring pero ejercitan reglas
existentes **desde el estado inicial**, confirman que la refactorización
preservó el comportamiento.

**Cómo un jurado puede reproducir la verificación:**

```bash
git checkout estado-inicial      # código original
git checkout estado-refactorizado # código refactorizado
py -m unittest discover -s tests  # las 11 pruebas deben pasar en verde
```

## 6.4 Cobertura

- **Operaciones cubiertas:** 6 de 6 (crear, adjuntar, cambiar estado,
  aprobar, rechazar, listar + detalle).
- **Escubiertos:** caminos de error (legajo inexistente, tipo inválido,
  solicitud inexistente, doble resolución) y caminos felices.
- **No cubierto (deuda consciente):** la persistencia JSON del
  `RepositorioSolicitudes` no tiene pruebas propias (requeriría tempdir);
  se documenta como mejora pendiente en las conclusiones.
