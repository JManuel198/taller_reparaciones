from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class TallerOrden(models.Model):
    _name = 'taller.orden'
    _description = 'Ordenes del taller'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        readonly=True,
        copy=False,
        default=lambda self: _('New'),
        required=True,
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
    )

    vehicle_id = fields.Many2one(
        comodel_name='fleet.vehicle',
        required=True,
    )

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('quote', 'Cotización'),
        ('in_progress', 'En Reparación'),
        ('completed', 'Completado'),
        ('canceled', 'Cancelado'),
        ('invoiced', 'Facturado')
    ], default='draft', tracking=True)

    # Botones de estado

    def action_confirm_quote(self):
        self.state = 'quote'
        # Añadir que si no hay producto, no permite confirmar borrador

    def action_start_repair(self):
        self.state = 'in_progress'

    def action_mark_completed(self):
        self.state = 'completed'

        # contenedor de movimientos
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'origin': self.name,
        })
        # iterar cada producto 
        for line in self.line_ids:
            product = line.product_id
            # si el producto es consumible, se mueve a cliente, si es servicio no.
            if product.type == 'consu':
                self.env['stock.move'].create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id':picking.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                })

        picking.action_confirm() # confirmar
        picking.action_assign() # asignar stock
        picking.button_validate() # validar y restar del On Hand

    def action_mark_cancel(self):
        self.state = 'canceled'

    def action_mark_invoiced(self):
        self.state = 'invoiced'

    line_ids = fields.One2many(
        comodel_name='taller.orden.linea',
        inverse_name='orden_id',
        string='Lineas de ordenes'
    )

    date = fields.Datetime(required=True, default=fields.Datetime.now)
    notes = fields.Text()

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company,
    )

    # Secuencia de ordenes
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Si viene como New (el default), asigna secuencia
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('taller.orden') or _('New')
        return super().create(vals_list)


