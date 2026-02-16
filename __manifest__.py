{
    'name': 'Taller Reparaciones',
    'version': '18.0.1.3.0',
    'author': 'Manuel Jauregui',
    'category': 'Other',
    'depends': [
        'base',
        'contacts',
        'product',
        'account_fleet',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/orden_reparacion_views.xml',
        'data/sequence_ordenes.xml',
        'data/taller_reparaciones_menus.xml',
    ],
    'application': True
}