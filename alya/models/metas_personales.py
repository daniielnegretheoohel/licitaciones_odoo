from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError

class MetaPersonal(models.Model):
    _name = "meta.personal"
    _description = "Metas de Desarrollo Personal"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "prioridad desc, fecha_limite asc"

    nombre = fields.Char(required=True, tracking=True)
    descripcion = fields.Text(tracking=True)

    categoria = fields.Selection([
        ('profesional', 'Desarrollo Profesional'),
        ('personal', 'Desarrollo Personal'),
        ('financiero', 'Metas Financieras'),
        ('salud', 'Salud y Bienestar'),
        ('aprendizaje', 'Aprendizaje')
    ], required=True)

    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_progreso', 'En Progreso'),
        ('en_pausa', 'En Pausa'),
        ('completado', 'Completado'),
        ('no_logrado', 'No Logrado')
    ], default='borrador', tracking=True)

    prioridad = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta'),
    ], default='1', tracking=True)

    fecha_limite = fields.Date(tracking=True)

    etiqueta_ids = fields.Many2many('etiqueta.meta.personal')

    recomendacion_ids = fields.One2many(
        'recomendacion.inteligente', 'meta_id'
    )

    actividad_ids = fields.One2many(
        'seguimiento.actividad', 'meta_id'
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Contacto",
        help="Contacto asociado a esta meta",
    )


    actividad_count = fields.Integer(
        compute="_compute_actividad_count", store=True
    )

    recomendacion_count = fields.Integer(
        compute="_compute_recomendacion_count", store=True
    )

    dias_restantes = fields.Integer(
        compute="_compute_dias_restantes", store=True
    )

    show_boton_completado = fields.Boolean(
        compute="_compute_show_boton_completado", store=False
    )


    def action_avanzar(self):
        for r in self:
            if r.estado == 'borrador':
                r.estado = 'en_progreso'
            elif r.estado == 'en_progreso':
                r.estado = 'en_pausa'
            elif r.estado == 'en_pausa':
                r.estado = 'completado'

    def action_retroceder(self):
        for r in self:
            if r.estado == 'completado':
                r.estado = 'en_pausa'
            elif r.estado == 'en_pausa':
                r.estado = 'en_progreso'
            elif r.estado == 'en_progreso':
                r.estado = 'borrador'
            elif r.estado == 'no_logrado':
                r.estado = 'en_progreso'

    def action_marcar_completado(self):
        for r in self:
            if r.estado != 'completado':
                r.estado = 'completado'

    def action_marcar_varias_completadas(self):
        for r in self:
            if r.estado in ['borrador', 'en_progreso', 'en_pausa']:
                r.estado = 'completado'


    def action_meta_personal_report(self):
        return self.env.ref('alya.action_meta_personal_report').report_action(self)

    def open_actividades(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actividades',
            'res_model': 'seguimiento.actividad',
            'view_mode': 'list,form',
            'domain': [('meta_id', '=', self.id)],
            'context': {'default_meta_id': self.id},
        }

    def open_recomendaciones(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Recomendaciones',
            'res_model': 'recomendacion.inteligente',
            'view_mode': 'list,form',
            'domain': [('meta_id', '=', self.id)],
            'context': {'default_meta_id': self.id},
        }

    def create(self, vals):
        record = super().create(vals)
        record.message_post(body="🎯 Meta creada correctamente.")
        return record

    def write(self, vals):
        estados_antes = {rec.id: rec.estado for rec in self}
        res = super().write(vals)
        if 'estado' in vals:
            for rec in self:
                antes = estados_antes[rec.id]
                despues = rec.estado
                if antes != despues:
                    rec.message_post(
                        body=f"🔄 Estado cambiado: <b>{antes}</b> → <b>{despues}</b>"
                    )

        return res

    def unlink(self):
        for rec in self:
            if rec.estado == 'completado':
                raise UserError("No puedes eliminar metas completadas.")
        return super().unlink()

    _sql_constraints = [
        (
            'unique_nombre_meta',
            'unique(nombre)',
            'Ya existe una meta con ese nombre.'
        )
    ]

    @api.depends('estado')
    def _compute_show_boton_completado(self):
        for r in self:
            r.show_boton_completado = (r.estado != 'completado')

    @api.depends('actividad_ids')
    def _compute_actividad_count(self):
        for r in self:
            r.actividad_count = len(r.actividad_ids)

    @api.depends('recomendacion_ids')
    def _compute_recomendacion_count(self):
        for r in self:
            r.recomendacion_count = len(r.recomendacion_ids)

    @api.depends('fecha_limite')
    def _compute_dias_restantes(self):
        for r in self:
            if r.fecha_limite:
                r.dias_restantes = (r.fecha_limite - date.today()).days
            else:
                r.dias_restantes = 0

    @api.constrains('fecha_limite')
    def _check_fecha_limite(self):
        for r in self:
            if r.fecha_limite and r.fecha_limite < fields.Date.today():
                raise ValidationError("La fecha límite no puede ser en el pasado.")

    @api.constrains('estado', 'actividad_ids')
    def _check_actividades_para_completar(self):
        for r in self:
            if r.estado == 'completado' and not r.actividad_ids:
                raise ValidationError(
                    "No puedes marcar una meta como completada sin registrar al menos una actividad."
                )

    @api.model
    def default_get(self, fields):
        vals = super().default_get(fields)
        vals['prioridad'] = '1'
        return vals
