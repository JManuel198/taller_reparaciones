from odoo import fields, models

class ProductComboComponent(models.Model):
    _name = 'product.combo.component'
    _description = 'Componente de combo'
    
    product_id = fields.Many2one(comodel_name='product.product')

    combo_id = fields.Many2one(comodel_name='product.product', string="Combo")

    quantity = fields.Float(default=1)