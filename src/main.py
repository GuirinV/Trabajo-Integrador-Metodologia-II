"""Demostracion del sistema base: Gestion de Solicitudes Academicas."""

from servicios import ServicioSolicitudes


def main():
    servicio = ServicioSolicitudes()

    print("\n===== 1) Alta de alumno =====")
    servicio.alta_alumno("A-1001", "Veronica Guirin", "Programacion", "vguirin@alumnos.utn.edu.ar")

    print("\n===== 2) Solicitud de EQUIVALENCIA =====")
    s1 = servicio.crear_solicitud("A-1001", "EQUIVALENCIA")
    servicio.adjuntar_documento(s1.id, "Plan de estudio", "PDF", True)
    servicio.aprobar(s1.id)  # falla: falta el syllabus

    print("\n===== 3) Se adjunta el syllabus y se aprueba =====")
    servicio.adjuntar_documento(s1.id, "Syllabus", "PDF", True)
    servicio.aprobar(s1.id)

    print("\n===== 4) Solicitud de CERTIFICADO rechazada =====")
    s2 = servicio.crear_solicitud("A-1001", "CERTIFICADO")
    servicio.rechazar(s2.id, "No abono la tasa administrativa")

    print("\n===== 5) Listado y detalle =====")
    servicio.listar_solicitudes_de_alumno("A-1001")
    servicio.ver_detalle(s2.id)


if __name__ == "__main__":
    main()
