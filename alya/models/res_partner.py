from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    meta_ids = fields.One2many(
        "meta.personal",
        "partner_id",
        string="Metas personales",
    )

    meta_count = fields.Integer(
        string="Cantidad de metas",
        compute="_compute_meta_count",
        readonly=True,
    )

    @api.depends("meta_ids")
    def _compute_meta_count(self):
        for partner in self:
            partner.meta_count = len(partner.meta_ids)
