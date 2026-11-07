# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pet_ids = fields.Many2many(
        'pet.profile',
        string='Pets',
        domain="[('partner_id', '=', partner_id), ('active', '=', True)]",
        help="Select pets for which products are being purchased"
    )

    @api.onchange('partner_id')
    def _onchange_partner_clear_pets(self):
        self.pet_ids = [(5, 0, 0)]

    def _get_pet_type_ids(self):
        return self.pet_ids.mapped('pet_type_id')

    def _get_breed_ids(self):
        return self.pet_ids.mapped('breed_id')