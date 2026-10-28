# TPI — Metodología de Sistemas II

**Trabajo Práctico Integrador:** diagnóstico y refactorización de un sistema de
Gestión de Solicitudes Académicas.

- **Autora:** Veronica Guirin
- **Materia:** Metodología de Sistemas II
- **Carrera:** Tecnicatura Universitaria en Programación (UTN) — modalidad a distancia
- **Lenguaje:** Python 3

## Descripción del sistema

Sistema de gestión de solicitudes académicas (equivalencias, certificados,
reclamos). Cada solicitud tiene un ciclo de vida (`PENDIENTE → EN_REVISION →
APROBADA / RECHAZADA`) y requiere documentos obligatorios para su aprobación.

## Cómo ejecutar

Requiere Python 3.8 o superior. No necesita dependencias externas.

```bash
python src/main.py
```

La demostración da de alta un alumno, crea dos solicitudes, adjunta documentos,
aprueba una y rechaza otra. Los datos se persisten en `datos/datos.json`.

## Estructura del repositorio

```
├── README.md
├── docs/
│   ├── 01-descripcion-sistema.md   ← texto para el informe PDF
│   └── prompts/                    ← registro de prompts usados con IA
├── src/
│   ├── modelos.py                  ← entidades: Alumno, Solicitud, Documento
│   ├── servicios.py                ← lógica de negocio y persistencia
│   └── main.py                     ← demostración por consola
└── datos/                          ← persistencia simulada (JSON)
```

## Etapas y tags del TPI

| Tag                  | Etapa                                            |
|----------------------|--------------------------------------------------|
| `estado-inicial`     | Sistema base seleccionado y descrito (etapa 1)   |
| `etapa-diagnostico`  | Deuda técnica y code smells (etapa 3)            |
| `estado-refactorizado` | Refactorizaciones aplicadas (etapa 5)           |
| `etapa-refactoring`  | Detalle del proceso de refactoring (etapa 5)     |
| `etapa-pruebas`      | Pruebas antes/después (etapa 6)                  |
| `etapa-docs`         | Documentación y code review (etapa 7)            |

## Declaración de uso de IA

Este trabajo fue desarrollado con asistencia de IA (OpenCode + Mimo), conforme a
lo permitido por la cátedra. El prompt inicial, el plan de trabajo y la autoría
final del código y el informe son responsabilidad de la autora.
