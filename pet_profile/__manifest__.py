# -*- coding: utf-8 -*-

{
    'name': "Pet Profile Management",
    'summary': "Comprehensive pet profile management system for tracking pets, breeds, and vaccinations",
    'description': """
        Pet Profile Management System
        ==============================

        This module provides complete pet profile management functionality including:
        * Pet profile creation and management
        * Pet type and breed cataloging
        * Vaccination record tracking
        * Owner association
        * Age calculation and tracking
        * Medical notes and special requirements

        Features:
        ---------
        * Automatic pet code generation (PP00001 format)
        * Support for multiple pet types (Dog, Cat, Bird, etc.)
        * Breed management per pet type
        * Comprehensive vaccination tracking
        * Image upload for pets
        * Microchip number tracking
        * Weight and physical characteristics
        * Integration with mail and activity tracking

        Perfect for veterinary clinics, pet care centers, and pet-focused businesses.
    """,
    'version': '19.0.1.0.0',
    'author': "Navabrind",
    'company': 'Navabrind',
    'maintainer': 'Navabrind',
    'website': "https://navabrindsol.com/",
    'category': 'Services/Pet Management',
    'license': 'AGPL-3',

    'depends': [
        'base',
        'stock',
        'mail',
        'auth_signup'
    ],

    'data': [
        # Data
        'data/sequence.xml',
        'data/data.xml',

        # Security
        'security/ir.model.access.csv',

        # Views
        'views/pet_profile.xml',
        'views/pet_profile.xml',
        'views/pet_type.xml',
        'views/menu.xml',



    ],

    'images': [
        'static/description/icon.png',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
