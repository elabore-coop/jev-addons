{
    'name': 'JEV lot custom',
    'version': '16.0.1.0.0',
    'description': 'customization of lot for JEV',
    'summary': '',
    'author': '',
    'website': '',
    'license': 'AGPL-3',
    'category': '',
    'depends': [
        'stock','botanical_list'
    ],
    'data': [
        'views/stock_lot_views.xml',
        'views/stock_quant_views.xml',
        'views/stock_tg_views.xml',
        'views/uom_uom_views.xml',
        'security/ir.model.access.csv',
        #'wizard/product_replenish_views.xml',
        #'wizard/stock_change_product_qty_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}
