# Sección 8 — Conclusiones y aprendizaje

> Texto destinado al **informe PDF**.
> ⚠️ **BORRADOR A PERSONALIZAR:** los pasajes marcados con ⚠️ deben revisarse y
> adaptarse con la experiencia real de quien presenta antes de entregar.

## 8.1 Conclusiones del trabajo

El TPI permitió recorrer el ciclo completo de mantenimiento de software sobre
un sistema real y funcional: desde la selección y descripción del sistema base,
pasando por el diagnóstico de su calidad, hasta el refactoring y su verificación
con pruebas.

**Resultados cuantitativos:**

| Métrica | Estado inicial | Estado final |
|---|---|---|
| Code smells diagnosticados | 10 | 6 resueltos / 4 documentados como deuda |
| Refactorings aplicados | 0 | 4 (Extract Method, Move Method, Parameter Object, Rename) |
| Pruebas automatizadas | 0 | 11 (todas en verde) |
| Archivos en `src/` | 2 (modelos, servicios) | 5 + 1 demo + 1 suite |
| Tamaño de `servicios.py` | 285 líneas (God Class) | 204 líneas con responsabilidades separadas |

**Principales conclusiones técnicas:**

1. **La calidad externa no necesitó cambios.** El usuario experimentó el mismo
   comportamiento antes y después; la demostración y las 11 pruebas lo
   confirman. Refactorizar es cambiar la estructura, no el comportamiento.
2. **La duplicación era la deuda más cara.** La regla de búsqueda estaba
   escrita en 5 lugares: cualquier cambio obligaba a 5 modificaciones
   sincronizadas. Extraer `buscar_solicitud()` la redujo a una sola fuente de
   verdad.
3. **Separar la persistencia del negocio habilitó las pruebas.** El
   `RepositorioSolicitudes` con inyección en el constructor hizo posible
   testear el servicio sin tocar el disco.
4. **Centralizar reglas de negocio ahorra riesgo futuro.** Los requisitos
   documentales ahora se agregan en una línea del diccionario `REQUISITOS`.

**Deuda pendiente consciente (ver sección 7):** la matriz de transiciones con
`if/elif`, las entidades Data Class y la falta de tests de persistencia
permanecen documentados y con riesgo acotado.

## 8.2 Aprendizaje personal

⚠️ **Personalizar con la experiencia real.** Borrador sugerido:

- **Concepto que más costó entender:** los principios SOLID, especialmente la
  Inversión de Dependencias. Al principio parecían abstracciones teóricas; se
  entendieron recién al ejecutar el Move Method y ver cómo el servicio dejó de
  depender del archivo JSON concreto. ⚠️ *Revisar: si te costó otro concepto,
  reemplazar.*

- **Lo más interesante:** descubrir que un "código que funciona" puede tener
  mala calidad interna al mismo tiempo. La calidad externa e interna son
  dimensiones distintas: el sistema aprobaba solicitudes (bien para el usuario)
  y al mismo tiempo era costoso de mantener (mal para el desarrollador). ⚠️
  *Personalizar con tu propia sensación.*

- **Aplicación en un trabajo real:** el TPI mostró que el refactoring no es un
  lujo académico: cada smell diagnosticado correspondía a un escenario concreto
  de costo (tocar 5 lugares para un cambio, perder un dato al agregar un
  atributo). En un equipo, esa deuda se paga con intereses. ⚠️ *Completar con
  lo que llevarías a tu empleo o futuros proyectos.*

- **Sobre el uso de IA:** se utilizó IA (OpenCode + Mimo) como herramienta de
  asistencia y guía, declarándolo según lo permitido por la cátedra. La
  autoría de las decisiones (selección del dominio, alcance, revisión de cada
  entregable y defensa) es propia; la IA aceleró la producción de código y
  documentos, pero cada resultado fue revisado, ejecutado y validado antes de
  aceptarse. ⚠️ *Ajustar el tono según lo que consideres justo decir.*

## 8.3 Cierre

El trabajo demostró que es posible mejorar la calidad interna de un sistema
de forma incremental y verificable, con un proceso trazable (etiquetas Git por
etapa) y sin alterar el comportamiento observable. La siguiente etapa de
evolución sería completar la deuda documentada en el code review y sumar
pruebas de persistencia.

---

⚠️ **Checklist antes de entregar:**
- [ ] Revisar y personalizar los 4 puntos de 8.2 con mi experiencia real
- [ ] Verificar que los números de 8.1 coincidan con el repo
- [ ] Pegar las secciones 1-8 en el informe PDF en orden
- [ ] Generar la carpeta `/docs/prompts/` con el registro final de prompts
- [ ] Subir el repo a GitHub
- [ ] Grabar el video de defensa (10-15 min, cámara y voz propias)
