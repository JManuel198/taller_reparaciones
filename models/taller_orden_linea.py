from odoo import fields, models, api, _

class TallerOrdenLinea(models.Model):
    _name = 'taller.orden.linea'
    _description = 'Lineas de orden'

    orden_id = fields.Many2one(
        comodel_name='taller.orden',
        string='Orden'
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Producto',
        help='Productos consumidos en la reparación'
    )

    quantity = fields.Integer(string='Cantidad')

    price_unit = fields.Float(string='Precio unitario')

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id,
        string='Moneda'
    )

    subtotal = fields.Monetary(
        string='Subtotal',
        readonly=True,
        compute='_compute_subtotal',
        store=True,
        currency_field='currency_id'
    )

    # Compute subtotal
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.price_unit
    
    # Compute precio de venta de productos
    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.price_unit = line.product_id.lst_price
