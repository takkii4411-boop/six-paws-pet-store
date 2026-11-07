# -*- coding: utf-8 -*-
{
    'name': 'Pet Sale Customization',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Pet-based product filtering in Sales Orders',
    'description': """
        Pet-based Sales Customization
        =============================
        - Select pet on Sale Order
        - Filter products based on pet type, age, and size
        - Prevent incompatible products
    """,
    'author': "Navabrind",
    'company': 'Navabrind',
    'maintainer': 'Navabrind',
    'website': "https://navabrindsol.com/",
    'category': 'Sales/Product',
    'license': 'AGPL-3',
    'sequence': 1,

    'depends': [
        'sale',
        'sale_management',
        'product',
        'pet_profile',
        'product_customization'
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
}
