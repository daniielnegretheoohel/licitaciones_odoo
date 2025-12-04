from odoo import fields, models


class RecomendacionInteligente(models.Model):
    _name = "recomendacion.inteligente"
    _description = "Recomendaciones Inteligentes para Metas"

    meta_id = fields.Many2one(
        "meta.personal",
        string="Meta Relacionada",
        required=True,
        ondelete="cascade",
    )

    fecha = fields.Datetime(
        string="Fecha y Hora",
        default=fields.Datetime.now,
    )

    tipo_recomendacion = fields.Selection(
        [
            ("estrategia", "Estrategia"),
            ("recurso", "Recurso"),
            ("aprendizaje", "Aprendizaje"),
            ("motivacion", "Motivación"),
        ],
        string="Tipo de Recomendación",
    )

    descripcion = fields.Text(
        string="Descripción",
    )
