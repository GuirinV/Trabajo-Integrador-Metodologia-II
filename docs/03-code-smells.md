# Sección 3 — Deuda técnica y code smells

> Texto destinado al **informe PDF**. Verificación: números de línea contra el
> commit `estado-inicial`.

## 3.1 Code smells detectados (10)

| # | Code smell (catálogo) | Ubicación |
|---|---|---|
| 1 | Duplicated Code | `servicios.py` 67-70, 87-90, 125-128, 168-171, 215-218 |
| 2 | Long Method | `servicios.py` 124-162 (`aprobar`) |
| 3 | Mixed Responsibilities (God Class) | `servicios.py` 10-285 (clase `ServicioSolicitudes`) |
| 4 | Magic Number / String | `servicios.py` 131, 134, 157, 162, 174, 177, 183 |
| 5 | Primitive Obsession | `servicios.py` 48, 74, 96-105, 155, 159, 179 |
| 6 | Data Class | `modelos.py` 1-23 |
| 7 | Feature Envy | `servicios.py` 241-270 (`guardar_datos`) |
| 8 | Complex Conditional | `servicios.py` 95-105 (`cambiar_estado`) |
| 9 | Redundant Code | `servicios.py` 136 y 141-142 (`aprobar`) |
| 10 | Duplicated Validation | `servicios.py` 74, 132, 175 |

## 3.2 Detalle y justificación

### 1. Duplicated Code — el mismo bloque de búsqueda repetido 5 veces

```python
# Aparece idéntico en: adjuntar_documento, cambiar_estado, aprobar, rechazar, ver_detalle
solicitud = None
for s in self.solicitudes:
    if s.id == id_solicitud:
        solicitud = s
```

**Justificación:** el mismo bloque de 4 líneas se repite en cinco métodos. Si se
modifica la búsqueda (por ejemplo, para buscar también por legajo), hay que
acordarse de cambiar los cinco lugares: si se olvida uno, aparece un
comportamiento inconsistente. El costo de mantenimiento se multiplica.

### 2. Long Method — `aprobar()` hace todo en 39 líneas

```python
def aprobar(self, id_solicitud):   # línea 124, hasta la 162
```

**Justificación:** un solo método busca la solicitud, valida el estado, calcula
los documentos requeridos por tipo, detecta faltantes, cambia el estado, persiste
e imprime. Nadie puede entenderlo de un vistazo ni testear una parte aislada;
hay que leer las 39 líneas enteras para saber qué pasa si falla.

### 3. Mixed Responsibilities (God Class) — `ServicioSolicitudes` concentra todo

```python
class ServicioSolicitudes:        # servicios.py, línea 10, ~276 líneas
```

**Justificación:** la clase hace alta de alumnos, validaciones, reglas de
negocio (transiciones, requisitos documentales), reportes por consola y
persistencia JSON. Son al menos 4 responsabilidades distintas: cualquier cambio
en la persistencia puede romper una regla de negocio y viceversa.

### 4. Magic Number — códigos de retorno sin significado

```python
return -1   # líneas 131 y 174: solicitud no encontrada
return -2   # líneas 134 y 177: ya resuelta
return 0    # línea 157: faltan documentos
return 1    # líneas 162 y 183: operación exitosa
```

**Justificación:** quien llama a `aprobar()` debe recordar que `-1` significa
"no existe" y `0` "faltan documentos". No hay forma de saberlo leyendo la
firma del método, y confundir `-1` con `0` produce errores silenciosos.

### 5. Primitive Obsession — estados y tipos como cadenas de texto libres

```python
solicitud.estado = "APROBADA"          # líneas 74, 132, 159, 175, 179
if tipo != "EQUIVALENCIA" and ...      # línea 39
```

**Justificación:** los estados (`"PENDIENTE"`, `"APROBADA"`...) y los tipos se
manejan como strings escritos a mano en todo el archivo. Un simple
`"APROBADAA"` o `"aprobada"` (sin mayúscula) rompe las comparaciones sin que el
intérprete avise nada. Además hace que la ejecución dependa de cadenas exactas
en múltiples lugares.

### 6. Data Class — entidades sin comportamiento

```python
class Solicitud:               # modelos.py, líneas 16-23
    def __init__(self, ...):
        self.id = ...
        self.estado = ...
        self.documentos = []
```

**Justificación:** `Alumno`, `Documento` y `Solicitud` solo guardan atributos
públicos; toda la lógica que les corresponde (¿puede cambiar de estado?, ¿puede
adjuntar documentos?, ¿está completa?) vive en el servicio. Es el síntoma
clásico de que el modelo no expresa el dominio: los objetos son "datos
muertos" y el servicio hace de intermediario de su información.

### 7. Feature Envy — `guardar_datos` husmea en todos los atributos ajenos

```python
datos["alumnos"].append({
    "legajo": a.legajo, "nombre": a.nombre, ...   # líneas 246-249
})
"legajo": s.legajo_alumno, "estado": s.estado, ... # líneas 259-262
```

**Justificación:** el método accede sistemáticamente a los internos de `Alumno`
y `Solicitud` para armar el diccionario. Cada atributo que se agregue a una
entidad obliga a recordar modificar este método: el servicio "envidia" los
datos de las clases que debería delegar (una entidad podría serializarse a sí
misma).

### 8. Complex Conditional —cadena de `if/elif` para las transiciones

```python
if solicitud.estado == "PENDIENTE" and nuevo_estado == "EN_REVISION":
    puede = True
elif solicitud.estado == "EN_REVISION" and (nuevo_estado == "APROBADA" or ...):
    puede = True
elif solicitud.estado == "PENDIENTE" and (nuevo_estado == "APROBADA" or ...):
    puede = True
```

**Justificación:** la matriz de transiciones válidas está embebida en
condicionales anidados. Agregar un estado nuevo obliga a revisar y reescribir
toda la cadena: si se agrega un `elif` de más, ciertas transiciones inválidas
quedan permitidas sin que se note fácilmente.

### 9. Redundant Code — inicialización repetida dentro de `aprobar()`

```python
requeridos = []                            # línea 136
if solicitud_encontrada.tipo == "EQUIVALENCIA":
    requeridos = ["plan de estudio", "syllabus"]
elif ...:
    requeridos = ["probante de pago"]
else:
    requeridos = []                        # líneas 141-142: ya estaba vacío
```

**Justificación:** el `else` repite exactamente el valor de la línea 136. Es
código muerto que distrae: quien lo lee puede suponer que ahí "algo debería
ponerse" y buscar una lógica inexistente.

### 10. Duplicated Validation — el chequeo "ya fue resuelta" repetido

```python
if solicitud.estado == "APROBADA" or solicitud.estado == "RECHAZADA":   # 74, 132, 175
```

**Justificación:** la misma regla de negocio ("una solicitud resuelta no se
toca") está escrita en tres métodos con idéntica forma. Si la regla cambia
(por ejemplo, se permite reabrir), hay que modificar los tres lugares: la regla
de negocio vive dispersa en lugar de tener una única fuente de verdad.

## 3.3 Deuda técnica

**Definición (para el informe):** la deuda técnica es el costo adicional que
implica mantener o evolucionar el sistema en su estado actual. No se mide en
dinero, sino en **esfuerzo de mantenimiento futuro**: cada hora que un
desarrollador debe gastar en comprender, buscar o corregir cosas que un código
diseñado no le costaría.

La tabla sigue una regla: *si no hay un cambio posible en las reglas de negocio
que no multiplique el esfuerzo por la cantidad de lugares donde está escrita la
regla, hay deuda*.

| Code smell | Esfuerzo de mantenimiento que genera | Escenario concreto que lo activa | Riesgo |
|---|---|---|---|
| 1. Duplicated Code (búsqueda ×5) | Cambiar un lugar obliga a cambiar 5 | Agregar búsqueda de solicitud por legajo o por fecha | Alto |
| 2. Long Method (`aprobar`) | Hay que leer 39 líneas para entender cualquier efecto | Modificar qué documentos exige cada tipo | Alto |
| 3. God Class | Cualquier cambio toca la clase entera | Cambiar el formato del JSON sin romper reglas | Alto |
| 4. Magic Numbers | Requiere leer el cuerpo para saber qué devuelve | Reutilizar `aprobar()` desde otra pantalla | Medio |
| 5. Primitive Obsession | Un string mal escrito falla en silencio | Agregar un estado `ANULADA` en todos los archivos | Alto |
| 6. Data Class | La lógica del dominio está dispersa en el servicio | Preguntar "¿puede reabrirse?" hay que buscarla en el servicio | Alto |
| 7. Feature Envy | Cada atributo nuevo obliga a revisar la persistencia | Agregar `telefono` al alumno: se olvida serializarlo y se pierde el dato | Medio |
| 8. Complex Conditional | La matriz de transiciones se reescribe completa | Habilitar reapertura de solicitudes rechazadas | Alto |
| 9. Redundant Code | Ruido que confunde al lector | Cualquier lectura del método `aprobar` | Bajo |
| 10. Duplicated Validation | La regla "resuelta no se toca" cambia en 3 lugares | Permitir adjuntar documentos a una solicitud aprobada | Medio |

**Balance de la deuda (para el informe):**

- **6 smells de riesgo alto**, 3 de riesgo medio y 1 bajo: el riesgo se concentra en la **duplicación** y
  en la **concentración de responsabilidades**, que son justamente las que
  multipliquan el costo ante cualquier cambio de reglas de negocio.
- **Deuda principal:** la regla de negocio no tiene una única fuente de verdad
  (está escrita en hasta 5 lugares). Eso convierte cualquier modificación en una
  búsqueda manual propensa al olvido.
- **Deuda secundaria:** la falta de pruebas automatizadas hace que el costo
  sea mayor todavía, porque no hay red de seguridad que avise si un cambio
  rompió algo (se ataca en la etapa 6).

**Conclusión de la etapa 3:** existe deuda técnica acumulada de riesgo alto en
duplicación y distribución de responsabilidades. El plan de sanación propuesto:
etapa 4 (aplicar SOLID y Clean Code como marco normativo), etapa 5 (ejecutar
refactorizaciones concretas sobre los smells 1, 2, 3 y 8) y etapa 6 (verificar
con pruebas que el comportamiento externo no cambió).

## 3.4 Resumen de cobertura

- **Cantidad:** 10 code smells (mínimo exigido: 8).
- **Categorías cubiertas:** duplicación (1, 10), complejidad (2, 8),
  distribución de responsabilidades (3, 6, 7), legibilidad (4, 5, 9).
- **Hallazgo extra (riesgo, no smell):** el ID se genera con
  `len(self.solicitudes) + 1` (`servicios.py` línea 43): si se eliminara una
  solicitud, dos solicitudes podrían compartir ID. Se documenta como bug
  latente a corregir en la etapa de refactoring.
