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
        ('quote', 'Cotización'),
        ('in_progress', 'En Reparación'),
        ('completed', 'Completado'),
        ('canceled', 'Cancelado'),
        ('invoiced', 'Facturado')
    ], string='Estado', default='draft', traking=True)

    # Botones de estado

    def action_confirm_quote(self):
        self.state = 'quote'

    def action_start_repair(self):
        self.state = 'in_progress'
    
    def action_mark_completed(self):
        self.state = 'completed'

    def action_mark_cancel(self):
        self.state = 'canceled'

    def action_mark_invoiced(self):
        self.state = 'invoiced'
        # Luego la lógica para la factura


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

