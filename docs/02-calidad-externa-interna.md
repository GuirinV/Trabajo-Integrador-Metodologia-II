# Sección 2 — Calidad externa vs. calidad interna

> Texto destinado al **informe PDF**.

## Definiciones

- **Calidad externa:** aquella que percibe el **usuario final** al utilizar el
  sistema. Se evalúa ejecutándolo: funcionalidad, confiabilidad, usabilidad,
  eficiencia.
- **Calidad interna:** aquella que percibe el **desarrollador** que hereda o
  mantiene el código. Se evalúa leyéndolo: legibilidad, estructura,
  mantenibilidad, testabilidad, bajo acoplamiento y ausencia de duplicación.

## Evaluación del sistema base

| Eje | Externa (usuario) | Interna (desarrollador) |
|---|---|---|
| Funcionalidad | ✅ Cumple las 6 operaciones definidas en la etapa 1 (crear, adjuntar, cambiar estado, aprobar/rechazar, listar, detalle) | ⚠️ La lógica de negocio (documentos obligatorios por tipo) está hardcodeada con `if/elif` dentro de `aprobar()` |
| Confiabilidad | ⚠️ Los IDs se generan con `len(solicitudes) + 1`: si una solicitud se eliminara, podrían repetirse | ⚠️ Código duplicado entre `aprobar()` y `rechazar()` (búsqueda de la solicitud y chequeo de estado se repiten) |
| Usabilidad | ✅ Mensajes claros por consola y validación de transiciones inválidas con retroalimentación | ⚠️ Los métodos imprimen, validan y guardan a la vez: responsabilidades mezcladas |
| Mantenibilidad | — (el usuario no la percibe) | ❌ `servicios.py` concentra toda la lógica (método "dios"): alta, validación, transiciones, reportes y persistencia en un solo archivo |
| Testabilidad | — | ❌ No hay pruebas automatizadas y la persistencia está acoplada a la lógica de negocio, lo que dificulta aislar componentes |

## Conclusión de la etapa

El sistema es **funcionalmente aceptable** desde el punto de vista externo: cumple
con lo prometido al usuario y sus mensajes son comprensibles. En cambio, la
**calidad interna es deficiente**: concentra responsabilidades, duplica código y
acopla la persistencia con las reglas de negocio.

Esta brecha es justamente el objeto del TPI: en las etapas 3 y 4 se diagnosticará
la deuda técnica asociada a estos síntomas, y en la etapa 5 se aplicarán
refactorizaciones para mejorar la calidad interna **sin alterar la calidad externa**
(la demostración de la etapa 6 probará que el comportamiento ante el usuario no
cambió).
