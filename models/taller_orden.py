from odoo import fields, models, api, _

class TallerOrden(models.Model):
    _name = 'taller.orden'
    _description = 'Ordenes del taller'

    name = fields.Char(
        readonly=True,
        copy=False,
        default=lambda self: _('New'),
        string='Orden ID',
        required=True
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        required=True
    )

    vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        string='Vehículo'
    )

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('cotizacion', 'Cotización'),
        ('en_reparacion', 'En Reparación'),
        ('listo', 'Listo'),
        ('facturado', 'Facturado')
    ], string='Estado', default='draft'
    )

    line_ids = fields.One2many(
        comodel_name='taller.orden.linea',
        inverse_name='orden_id',
        string='Lineas de ordenes'
    )

    date = fields.Datetime(required=True, default=fields.Date.today)
    notes = fields.Text()

    # Secuencia
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Si viene como New (el default), asigna secuencia
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('taller.orden') or _('New')
        return super().create(vals_list)

