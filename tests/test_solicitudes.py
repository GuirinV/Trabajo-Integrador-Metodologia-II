"""Pruebas automatizadas del sistema de Gestion de Solicitudes Academicas.

Corren con:  py -m unittest discover -s tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from constantes import (
    ESTADO_APROBADA,
    ESTADO_EN_REVISION,
    ESTADO_PENDIENTE,
    ESTADO_RECHAZADA,
    RESULTADO_EXITO,
    RESULTADO_FALTAN_DOCUMENTOS,
    RESULTADO_NO_ENCONTRADA,
    RESULTADO_YA_RESUELTA,
)
from servicios import ServicioSolicitudes


class RepositorioEnMemoria:
    """Repositorio de prueba: no toca el disco."""

    def guardar(self, alumnos, solicitudes):
        pass

    def cargar(self):
        return [], []


def crear_servicio():
    servicio = ServicioSolicitudes(repositorio=RepositorioEnMemoria())
    servicio.alta_alumno("A-1001", "Veronica Guirin", "Programacion", "v@utn.edu.ar")
    return servicio


class TestCrearSolicitud(unittest.TestCase):

    def test_crear_solicitud_valida(self):
        s = crear_servicio().crear_solicitud("A-1001", "EQUIVALENCIA")
        self.assertIsNotNone(s)
        self.assertEqual(s.estado, ESTADO_PENDIENTE)

    def test_crear_solicitud_con_legajo_inexistente(self):
        s = crear_servicio().crear_solicitud("NO-EXISTE", "EQUIVALENCIA")
        self.assertIsNone(s)

    def test_crear_solicitud_con_tipo_invalido(self):
        s = crear_servicio().crear_solicitud("A-1001", "TIPO-RARO")
        self.assertIsNone(s)


class TestAprobar(unittest.TestCase):

    def test_aprobar_sin_documentos_obligatorios_falla(self):
        s = crear_servicio()
        sol = s.crear_solicitud("A-1001", "CERTIFICADO")
        resultado = s.aprobar(sol.id)
        self.assertEqual(resultado, RESULTADO_FALTAN_DOCUMENTOS)
        self.assertEqual(s.buscar_solicitud(sol.id).estado, ESTADO_EN_REVISION)

    def test_aprobar_con_documentos_obligatorios_exito(self):
        s = crear_servicio()
        sol = s.crear_solicitud("A-1001", "EQUIVALENCIA")
        s.adjuntar_documento(sol.id, "Plan de estudio", "PDF", True)
        s.adjuntar_documento(sol.id, "Syllabus", "PDF", True)
        resultado = s.aprobar(sol.id)
        self.assertEqual(resultado, RESULTADO_EXITO)
        self.assertEqual(s.buscar_solicitud(sol.id).estado, ESTADO_APROBADA)


class TestRechazar(unittest.TestCase):

    def test_rechazar_con_motivo(self):
        s = crear_servicio()
        sol = s.crear_solicitud("A-1001", "CERTIFICADO")
        resultado = s.rechazar(sol.id, "No abono la tasa")
        self.assertEqual(resultado, RESULTADO_EXITO)
        self.assertEqual(s.buscar_solicitud(sol.id).estado, ESTADO_RECHAZADA)

    def test_rechazar_solicitud_ya_resuelta_falla(self):
        s = crear_servicio()
        sol = s.crear_solicitud("A-1001", "CERTIFICADO")
        s.rechazar(sol.id, "Motivo 1")
        resultado = s.rechazar(sol.id, "Motivo 2")
        self.assertEqual(resultado, RESULTADO_YA_RESUELTA)


class TestTransiciones(unittest.TestCase):

    def test_transicion_invalida_rechazada(self):
        s = crear_servicio()
        sol = s.crear_solicitud("A-1001", "CERTIFICADO")
        valido = s.cambiar_estado(sol.id, "NO_EXISTE")
        self.assertFalse(valido)
        self.assertEqual(s.buscar_solicitud(sol.id).estado, ESTADO_PENDIENTE)


class TestDocumentos(unittest.TestCase):

    def test_adjuntar_documento_a_solicitud_resuelta_falla(self):
        s = crear_servicio()
        sol = s.crear_solicitud("A-1001", "CERTIFICADO")
        s.rechazar(sol.id, "Motivo")
        doc = s.adjuntar_documento(sol.id, "Extra", "PDF", False)
        self.assertIsNone(doc)


class TestConsultas(unittest.TestCase):

    def test_listar_y_detalle_de_alumno(self):
        s = crear_servicio()
        s.crear_solicitud("A-1001", "CERTIFICADO")
        s.crear_solicitud("A-1001", "EQUIVALENCIA")
        solicitudes = s.listar_solicitudes_de_alumno("A-1001")
        self.assertEqual(len(solicitudes), 2)
        self.assertIsNotNone(s.ver_detalle(solicitudes[0].id))

    def test_aprobar_solicitud_inexistente(self):
        s = crear_servicio()
        self.assertEqual(s.aprobar(999), RESULTADO_NO_ENCONTRADA)


if __name__ == "__main__":
    unittest.main()
