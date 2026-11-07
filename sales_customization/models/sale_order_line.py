# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_domain = fields.Char(
        compute='_compute_product_domain',
        compute_sudo=True,
        store=False,
    )

    @api.depends(
        'order_id.pet_ids',
        'order_id.pet_ids.pet_type_id',
        'order_id.pet_ids.breed_id',
        'order_id.company_id',
    )
    def _compute_product_domain(self):
        for line in self:
            base_domain = [('sale_ok', '=', True)]
            base_domain += [('company_id', 'in', [False, line.company_id.id])]
            if not line.order_id or not line.order_id.pet_ids:
                line.product_domain = str(base_domain)
                continue

            pet_type_ids = line.order_id.pet_ids.mapped('pet_type_id').ids
            breed_ids = line.order_id.pet_ids.mapped('breed_id').ids

            pet_domain = []
            if pet_type_ids:
                pet_domain.append(('pet_type_id', 'in', pet_type_ids))
            if breed_ids:
                pet_domain.append(('breed_id', 'in', breed_ids))

            full_domain = base_domain + pet_domain
            line.product_domain = str(full_domain)
