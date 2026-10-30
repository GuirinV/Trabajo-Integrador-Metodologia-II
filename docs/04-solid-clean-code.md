# Sección 4 — Principios SOLID y Clean Code

> Texto destinado al **informe PDF**. Referencias de línea verificadas contra el
> commit `etapa-diagnostico` (78d2c99).

## 4.1 Principios SOLID aplicados al sistema base

| Principio | Definición operativa | Violación en el código | Plan de arreglo (etapa 5) |
|---|---|---|---|
| **S** — Responsabilidad Única | Una clase debe tener una sola razón para cambiar | `ServicioSolicitudes` (`servicios.py` 10-285) mezcla reglas de negocio, reportes por consola y persistencia JSON: son 4 responsabilidades | Extraer la persistencia a una clase `RepositorioSolicitudes` y dejar al servicio solo con reglas de negocio |
| **O** — Abierto/Cerrado | Abierto a extensión, cerrado a modificación | Los tipos de solicitud están hardcodeados en `crear_solicitud` (línea 39) y los documentos requeridos en un `if/elif` dentro de `aprobar` (137-142): agregar un tipo exige modificar esas líneas | Centralizar los requisitos en una estructura de datos (diccionario tipo → documentos) que se pueda ampliar sin tocar la lógica |
| **L** — Sustitución de Liskov | Los subtipos deben poder sustituir a sus tipos sin alterar el comportamiento | No se detecta violación actual: no hay jerarquías de clases aún (las entidades no heredan). Se documenta como **no aplicable en el estado inicial** y se vigila al introducir subclases | Mantener la vigilancia al refactorizar; no introducir herencia sin necesidad |
| **I** — Inversión de Dependencias | Los de alto nivel no deben depender de bajo nivel; ambos dependen de abstracciones | El servicio instancia y maneja directamente la persistencia (`self.guardar_datos()` llamado en 9 lugares): la lógica de negocio depende de un detalle concreto (archivo JSON) | El servicio dependerá de una interfaz/repositorio simple; la implementación JSON queda detrás |
| **D** — Segregación de Interfaces | Interfaces pequeñas y específicas | No hay interfaces explícitas; al introducir el repositorio, la regla a respetar es que no exponga métodos que quien lo usa no necesita | El repositorio expone solo guardar/cargar/buscador, sin mezclar reglas |

**Nota para el informe:** Liskov y Segregación se marcan honestamente como "no
aplicables todavía" en un sistema sin jerarquías ni interfaces. Decir que un
principio no aplica *y argumentar por qué* demuestra más comprensión que
rellenar la tabla.

## 4.2 Clean Code aplicado al sistema base

| Regla de Clean Code | Violación detectada | Ejemplo en el código | Cómo queda después del refactor |
|---|---|---|---|
| **Nombres con intención** | Nombres que no expresan la regla | `puede` (línea 95), `f` para el archivo (268), `a`/`s`/`d` como únicos identificadores en bucles | `transicion_valida`, `archivo`, `alumno`/`solicitud`/`documento` |
| **Funciones cortas y con un objetivo** | Métodos que hacen demasiado | `aprobar` (124-162): 39 líneas con 6 tareas | `aprobar` orquesta; la validación de documentos pasa a un método dedicado |
| **No repetir código (DRY)** | Bloques idénticos en varios métodos | Búsqueda de solicitud ×5 (67-70, 87-90, 125-128, 168-171, 215-218) | Un único `buscar_solicitud(id)` |
| **Código antes que comentarios** | Comentarios de sección que reemplazan nombres | Bloques `# ----- APROBAR -----` (17-19, 27-29, 63-65...) | Los nombres de métodos ya describen la intención; se eliminan los separadores ruidosos |
| **Sin números mágicos / estados codificados** | Valores sin nombre repartidos en el código | `return -1/-2/0/1` (131-183), estados como strings libres | Constantes con nombre y/o estados centralizados |
| **Los datos viven con su comportamiento** | Entidades que solo guardan datos | `modelos.py` 1-23 (Data Class) | Reglas como `solicitud.puede_adjuntar()` pasan a la entidad |

## 4.3 Correspondencia principios → refactorizaciones (etapa 5)

Para que el informe no quede "definiciones colgadas", cada principio se resuelve
con un refactoring concreto del catálogo exigido:

| Principio/regla a resolver | Refactoring de la etapa 5 |
|---|---|
| DRY (búsqueda ×5) y Responsabilidad Única | **Extract Method** → `buscar_solicitud(id)` y método de validación de documentos |
| God Class: separar persistencia del negocio | **Move Method** → `guardar_datos`/`cargar_datos` se mudan a `RepositorioSolicitudes` |
| Complejidad de `aprobar` (reglas del tipo + faltantes) | **Introduce Parameter Object** → objeto `RequisitosDocumentales` con los documentos del tipo |
| Reglas duplicadas en 3 métodos | **Rename/Move** de la validación de estado a un solo lugar (4º refactoring a definir) |

## 4.4 Conclusión de la etapa 4

El sistema viola S, O, I y D (L es no aplicable sin jerarquías), y al menos
cuatro reglas de Clean Code. Las violaciones no son teóricas: todas coinciden
con los code smells de la etapa 3 y todas tienen un refactorings de salida
mapeado. A continuación se ejecutan dichos refactorings preservando el
comportamiento externo.
