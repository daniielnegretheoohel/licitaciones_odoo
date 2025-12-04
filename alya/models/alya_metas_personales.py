from datetime import date

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class MetaPersonal(models.Model):
    _name = "meta.personal"
    _description = "Metas de Desarrollo Personal"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "prioridad desc, fecha_limite asc"

    # -------------------------------------------------------------------------
    # FIELDS
    # -------------------------------------------------------------------------
    nombre = fields.Char(
        required=True,
        tracking=True,
    )
    descripcion = fields.Text(
        tracking=True,
    )

    categoria = fields.Selection(
        [
            ("profesional", "Desarrollo Profesional"),
            ("personal", "Desarrollo Personal"),
            ("financiero", "Metas Financieras"),
            ("salud", "Salud y Bienestar"),
            ("aprendizaje", "Aprendizaje"),
        ],
        required=True,
    )

    estado = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("en_progreso", "En Progreso"),
            ("en_pausa", "En Pausa"),
            ("completado", "Completado"),
            ("no_logrado", "No Logrado"),
        ],
        default="borrador",
        tracking=True,
    )

    prioridad = fields.Selection(
        [
            ("0", "Baja"),
            ("1", "Media"),
            ("2", "Alta"),
        ],
        default="1",
        tracking=True,
    )

    fecha_limite = fields.Date(
        tracking=True,
    )

    etiqueta_ids = fields.Many2many(
        "etiqueta.meta.personal",
        string="Etiquetas",
    )

    recomendacion_ids = fields.One2many(
        "recomendacion.inteligente",
        "meta_id",
        string="Recomendaciones",
    )

    actividad_ids = fields.One2many(
        "seguimiento.actividad",
        "meta_id",
        string="Actividades",
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Contacto",
        help="Contacto asociado a esta meta.",
    )

    actividad_count = fields.Integer(
        compute="_compute_actividad_count",
        store=True,
    )

    recomendacion_count = fields.Integer(
        compute="_compute_recomendacion_count",
        store=True,
    )

    dias_restantes = fields.Integer(
        compute="_compute_dias_restantes",
        store=True,
    )

    show_boton_completado = fields.Boolean(
        compute="_compute_show_boton_completado",
    )

    _sql_constraints = [
        (
            "unique_nombre_meta",
            "unique(nombre)",
            "Ya existe una meta con ese nombre.",
        )
    ]


    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        vals.setdefault("prioridad", "1")
        return vals

    @api.depends("estado")
    def _compute_show_boton_completado(self):
        for record in self:
            record.show_boton_completado = record.estado != "completado"

    @api.depends("actividad_ids")
    def _compute_actividad_count(self):
        for record in self:
            record.actividad_count = len(record.actividad_ids)

    @api.depends("recomendacion_ids")
    def _compute_recomendacion_count(self):
        for record in self:
            record.recomendacion_count = len(record.recomendacion_ids)

    @api.depends("fecha_limite")
    def _compute_dias_restantes(self):
        today = date.today()
        for record in self:
            if record.fecha_limite:
                record.dias_restantes = (record.fecha_limite - today).days
            else:
                record.dias_restantes = 0


    @api.constrains("fecha_limite")
    def _check_fecha_limite(self):
        today = fields.Date.today()
        for record in self:
            if record.fecha_limite and record.fecha_limite < today:
                raise ValidationError(
                    "La fecha límite no puede ser en el pasado."
                )

    @api.constrains("estado", "actividad_ids")
    def _check_actividades_para_completar(self):
        for record in self:
            if record.estado == "completado" and not record.actividad_ids:
                raise ValidationError(
                    "No puedes marcar una meta como completada "
                    "sin registrar al menos una actividad."
                )

    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record.message_post(body="🎯 Meta creada correctamente.")
        return records

    def write(self, vals):
        estados_antes = {rec.id: rec.estado for rec in self}
        res = super().write(vals)
        if "estado" in vals:
            for rec in self:
                antes = estados_antes.get(rec.id)
                despues = rec.estado
                if antes != despues:
                    rec.message_post(
                        body=(
                            "🔄 Estado cambiado: "
                            f"<b>{antes}</b> → <b>{despues}</b>"
                        )
                    )
        return res

    def unlink(self):
        for record in self:
            if record.estado == "completado":
                raise UserError("No puedes eliminar metas completadas.")
        return super().unlink()

    def action_avanzar(self):
        for record in self:
            if record.estado == "borrador":
                record.estado = "en_progreso"
            elif record.estado == "en_progreso":
                record.estado = "en_pausa"
            elif record.estado == "en_pausa":
                record.estado = "completado"

    def action_retroceder(self):
        for record in self:
            if record.estado == "completado":
                record.estado = "en_pausa"
            elif record.estado == "en_pausa":
                record.estado = "en_progreso"
            elif record.estado == "en_progreso":
                record.estado = "borrador"
            elif record.estado == "no_logrado":
                record.estado = "en_progreso"

    def action_marcar_completado(self):
        for record in self:
            if record.estado != "completado":
                record.estado = "completado"

    def action_marcar_varias_completadas(self):
        for record in self:
            if record.estado in {"borrador", "en_progreso", "en_pausa"}:
                record.estado = "completado"

    def action_meta_personal_report(self):
        """Lanza el reporte PDF de meta personal."""
        return self.env.ref("alya.action_report_meta_personal").report_action(
            self
        )

    def open_actividades(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Actividades",
            "res_model": "seguimiento.actividad",
            "view_mode": "list,form",
            "domain": [("meta_id", "=", self.id)],
            "context": {"default_meta_id": self.id},
        }

    def open_recomendaciones(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Recomendaciones",
            "res_model": "recomendacion.inteligente",
            "view_mode": "list,form",
            "domain": [("meta_id", "=", self.id)],
            "context": {"default_meta_id": self.id},
        }
