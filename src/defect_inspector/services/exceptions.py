"""Excepciones de dominio desacopladas de transporte en Capa 2."""

from __future__ import annotations


class DefectInspectorError(Exception):
    """Excepción base de dominio para el servicio de inspección."""


class DomainValidationError(DefectInspectorError):
    """Parámetro de negocio o entrada inválida enviada por el cliente."""


class UnsupportedImageFormatError(DefectInspectorError):
    """Formato o tipo MIME de imagen no admitido por el servicio."""


class ModelNotReadyError(DefectInspectorError):
    """El modelo MaaS no está cargado o listo en memoria."""


class InspectionProcessingError(DefectInspectorError):
    """Fallo interno inesperado durante la ejecución del pipeline."""
