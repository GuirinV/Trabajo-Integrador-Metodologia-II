# Sección 5 — Refactorizaciones aplicadas

> Texto destinado al **informe PDF**. Cada refactoring tiene su propio commit
> en el repositorio, de modo que el antes/después es verificable con Git.

## Criterio de seguridad aplicado a los 4 refactorings

**Un refactoring es un cambio de estructura sin cambio de comportamiento.**
Antes de cada commit se borró `datos/datos.json` y se volvió a ejecutar
`py src/main.py`: la salida de la demostración fue **idéntica** a la del estado
inicial en los cuatro casos (la única diferencia es la fecha del día, generada
por `datetime.now()`).

## 5.1 Extract Method — extraer `buscar_solicitud()`

| Campo | Contenido |
|---|---|
| **Commit** | `d4df731` |
| **Smell resuelto** | #1 Duplicated Code |
| **Principios** | DRY, Responsabilidad Única (etapa 4) |
| **Archivo** | `src/servicios.py` |

**Antes** — el mismo bloque de 4 líneas aparecía en 5 métodos
(`adjuntar_documento`, `cambiar_estado`, `aprobar`, `rechazar`, `ver_detalle`):

```python
solicitud = None
for s in self.solicitudes:
    if s.id == id_solicitud:
        solicitud = s
```

**Después** — un único método con la responsabilidad de buscar:

```python
def buscar_solicitud(self, id_solicitud):
    for s in self.solicitudes:
        if s.id == id_solicitud:
            return s
    return None
```

Cada llamante quedó en una línea: `solicitud = self.buscar_solicitud(id_solicitud)`.

**Impacto:** 5 copias → 1 fuente de verdad. Modificar la búsqueda ahora exige
tocar un solo lugar (el costo de mantenimiento del smell #1 pasó de "alto" a
"nulo").

## 5.2 Move Method — la persistencia se muda a `RepositorioSolicitudes`

| Campo | Contenido |
|---|---|
| **Commit** | `8eb2737` |
| **Smell resuelto** | #3 God Class / Mixed Responsibilities |
| **Principios** | S (Responsabilidad Única), I (Inversión de Dependencias) |
| **Archivos** | `src/repositorio.py` (nuevo), `src/servicios.py` |

**Antes** — `ServicioSolicitudes` (285 líneas) tenía `guardar_datos()` y
`cargar_datos()` en su interior: negocio, reportes y JSON en la misma clase.

**Después** — nace `RepositorioSolicitudes` con `guardar(alumnos, solicitudes)`
y `cargar()`; el servicio le delega mediante un método corto:

```python
def guardar(self):
    self.repositorio.guardar(self.alumnos, self.solicitudes)
```

**Impacto:** el servicio ya no importa `json` ni `os` ni conoce el formato del
archivo. Cambiar la persistencia (por ejemplo, por SQLite) no toca una sola
línea de reglas de negocio — eso es exactamente la Inversión de Dependencias.

## 5.3 Introduce Parameter Object — objeto `RequisitosDocumentales`

| Campo | Contenido |
|---|---|
| **Commit** | `de6a4ab` |
| **Smell resuelto** | #2 (parte de Long Method) y plan de arreglo del principio O |
| **Principios** | O (Abierto/Cerrado) |
| **Archivos** | `src/requisitos.py` (nuevo), `src/servicios.py` |

**Antes** — `aprobar()` contenía el `if/elif` hardcodeado de documentos
requeridos por tipo (16 líneas dentro del método):

```python
requeridos = []
if solicitud_encontrada.tipo == "EQUIVALENCIA":
    requeridos = ["plan de estudio", "syllabus"]
elif solicitud_encontrada.tipo == "CERTIFICADO":
    requeridos = ["probante de pago"]
else:
    requeridos = []
# ... más la lógica de comparación de faltantes
```

**Después** — la regla de negocio vive en un solo objeto con una única fuente
de verdad:

```python
class RequisitosDocumentales:
    REQUISITOS = {
        "EQUIVALENCIA": ["plan de estudio", "syllabus"],
        "CERTIFICADO": ["probante de pago"],
        "RECLAMO": [],
    }

    def __init__(self, tipo):
        self.tipo = tipo
        self.documentos = self.REQUISITOS.get(tipo, [])

    def faltantes(self, documentos_adjuntos):
        nombres_adjuntos = [d.nombre.lower() for d in documentos_adjuntos]
        return [r for r in self.documentos if r not in nombres_adjuntos]
```

Y en `aprobar()`:

```python
requisitos = RequisitosDocumentales(solicitud_encontrada.tipo)
faltantes = requisitos.faltantes(solicitud_encontrada.documentos)
```

**Impacto:** el método `aprobar` perdió 16 líneas de detalle. Agregar un tipo
de solicitud nuevo = agregar **una línea** al diccionario `REQUISITOS`, sin
modificar ningún método (cerrado a modificación, abierto a extensión).

## 5.4 Rename — constantes para estados y códigos de retorno

| Campo | Contenido |
|---|---|
| **Commit** | `8f9af1b` |
| **Smell resuelto** | #4 Magic Number y #5 Primitive Obsession |
| **Principios** | Clean Code: nombres con intención |
| **Archivos** | `src/constantes.py` (nuevo), `src/servicios.py` |

**Antes** — estados como cadenas libres y códigos numéricos sin nombre:

```python
return -1          # ¿qué significa?
return -2
solicitud.estado = "APROBADA"    # una mayúscula de más rompe todo en silencio
```

**Después** — `src/constantes.py`:

```python
ESTADO_PENDIENTE = "PENDIENTE"
ESTADO_EN_REVISION = "EN_REVISION"
ESTADO_APROBADA = "APROBADA"
ESTADO_RECHAZADA = "RECHAZADA"

RESULTADO_NO_ENCONTRADA = -1
RESULTADO_YA_RESUELTA = -2
RESULTADO_FALTAN_DOCUMENTOS = 0
RESULTADO_EXITO = 1
```

**Impacto:** el código se auto documenta. Un typo en un estado (por ejemplo
`"APROBADAA"`) ahora es imposible: se escribe el nombre de la constante y el
intérprete avisa si no existe.

## 5.5 Resumen de cobertura

| Requisito de la consigna | Refactoring aplicado | Commit |
|---|---|---|
| Extract Method | `buscar_solicitud()` | `d4df731` |
| Move Method | `RepositorioSolicitudes` | `8eb2737` |
| Introduce Parameter Object | `RequisitosDocumentales` | `de6a4ab` |
| 4to refactoring a elección | Rename (constantes) | `8f9af1b` |

**Smells resueltos de los 10 diagnosticados:** #1, #2 (parcial), #3, #4, #5 y
los efectos del #7. Permanecen deliberadamente #6 (Data Class), #8 (Complex
Conditional en `cambiar_estado`), #9 y #10: se documentan en las conclusiones
(etapa 8) como deuda pendiente consciente — refactorizar todo es innecesario
para el objetivo del trabajo y refactorizar *mal* es peor que no refactorizar.
