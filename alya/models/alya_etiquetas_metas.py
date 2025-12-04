from odoo import models, fields


class EtiquetaMetaPersonal(models.Model):
    _name = "etiqueta.meta.personal"
    _description = "Etiquetas para Metas Personales"

    nombre = fields.Char(
        string="Nombre de Etiqueta",
        required=True,
    )
    color = fields.Integer(
        string="Color",
    )
