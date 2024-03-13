{
    'name': 'JEV accounting custom',
    'version': '16.0.1.1.0',
    'description': 'customization of accounting app for JEV',
    'summary': '',
    'author': '',
    'website': '',
    'license': 'AGPL-3',
    'category': '',
    'depends': [
        'account','account_usability_akretion','sale','sale_stock'
    ],
    'data': [
        'views/account_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}
