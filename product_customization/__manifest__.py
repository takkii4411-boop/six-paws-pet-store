# -*- coding: utf-8 -*-
{
    'name': "Product Customization",
    'summary': "Extended product fields for pet food, nutrition, and marketing content",
    'description': """
        Product Customization for Pet Products
        =======================================

        This module extends Odoo product management to support
        pet-specific product attributes such as:
        * Animal type (Cat, Dog, Other)
        * Life stage (Kitten, Puppy, Adult, Senior)
        * Breed size classification
        * Detailed nutrition information (protein, fat, fiber, kcal)
        * Product benefits and key features
        * Certifications and compliance
        * Storage and usage instructions
        * Return policy configuration
        * Subscription recommendations
        * Physical dimensions and attributes

        It is designed as a focused product extension module and is
        fully compatible with Odoo 19 core product, website,
        and eCommerce functionality.
    """,
    'version': '19.0.1.0.0',
    'author': "Navabrind",
    'company': 'Navabrind',
    'maintainer': 'Navabrind',
    'website': "https://navabrindsol.com/",
    'category': 'Sales/Product',
    'license': 'AGPL-3',

    'depends': [
        'base',
        'stock',
        'product',
        'sale',
        'website_sale',
        'pet_profile',
    ],
    'data': [
        'security/ir.model.access.csv',
        # Views
        'views/product_template_form_view.xml',
        'controllers/show_no_views.xml'
    ],
    'assets': {
        'web.assets_frontend': [
        ],
    },

    'installable': True,
    'auto_install': False,
    'application': False,
}
