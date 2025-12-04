from odoo import fields, models


class SeguimientoActividad(models.Model):
    _name = "seguimiento.actividad"
    _description = "Seguimiento de Actividades para Logro de Metas"

    meta_id = fields.Many2one(
        "meta.personal",
        string="Meta Relacionada",
        required=True,
    )

    fecha = fields.Datetime(
        string="Fecha y Hora",
        default=fields.Datetime.now,
    )

    tipo_actividad = fields.Selection(
        [
            ("actualizacion_progreso", "Actualización de Progreso"),
            ("aprendizaje", "Actividad de Aprendizaje"),
            ("hito", "Hito Alcanzado"),
            ("desafio", "Desafío Encontrado"),
        ],
        string="Tipo de Actividad",
    )

    descripcion = fields.Text(
        string="Descripción",
    )
