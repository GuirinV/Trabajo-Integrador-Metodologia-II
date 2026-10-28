# Sección 1 — Descripción del sistema base

> Texto destinado al **informe PDF**.

## Sistema: Gestión de Solicitudes Académicas

El sistema permite a los alumnos de una institución educativa gestionar solicitudes
administrativas (equivalencias, certificados, reclamos). Cada solicitud recorre un
ciclo de vida con estados definidos y debe cumplir requisitos documentales antes de
ser resuelta.

### Entidades

| Entidad    | Atributos                          | Responsabilidad                              |
|------------|------------------------------------|----------------------------------------------|
| Alumno     | legajo, nombre, carrera, email     | Persona que presenta las solicitudes         |
| Solicitud  | id, tipo, estado, fecha_creación   | Registro de un trámite con su ciclo de vida  |
| Documento  | nombre, tipo, obligatorio          | Requisito adjunto que condiciona la aprobación |

### Estados de una solicitud

`PENDIENTE → EN_REVISION → APROBADA` o `RECHAZADA`

### Operaciones principales

| #  | Operación                        | Regla de negocio asociada                          |
|----|----------------------------------|----------------------------------------------------|
| 1  | Crear solicitud                  | Toda solicitud nace en estado PENDIENTE            |
| 2  | Adjuntar documento               | Solo sobre solicitudes no resueltas                |
| 3  | Cambiar estado                   | Solo se permiten transiciones válidas              |
| 4  | Aprobar / Rechazar               | Requiere los documentos obligatorios adjuntos      |
| 5  | Listar solicitudes de un alumno  | Filtrado por legajo                                |
| 6  | Consultar detalle                | Devuelve solicitud + documentos adjuntos           |

### Persistencia simulada

El sistema mantiene los datos en memoria y los serializa a un archivo JSON
(`datos/datos.json`) tras cada operación, simulando una base de datos sin depender
de infraestructura externa.

### Restricciones y alcance

- Aplicación de consola (sin interfaz gráfica).
- Sin usuarios ni autenticación: se identifica al alumno por su legajo.
- El "revisor" no se modela como entidad; las acciones de aprobar/rechazar se
  realizan desde el servicio.
