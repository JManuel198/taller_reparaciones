from odoo import fields, models

class ProductoComboComponentes(models.Model):
    _name = 'product.combo.component'
    _description = 'Componente de combo'
    
    combo_id = fields.Many2one(
        comodel_name='product.product',
        string='combo',
        required=True,
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Componente',
        required=True
    )

    quantity = fields.Float(
        string='Cantidad por combo', 
        default=1
    )