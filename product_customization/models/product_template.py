from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    # -----------------------------
    # Pet Classification
    # -----------------------------
    visibility_online = fields.Boolean(string='Visibility Online')
    brand_id = fields.Many2one('product.brand', string="Brand")
    animal_type = fields.Selection([
        ('cat', 'Cat'),
        ('dog', 'Dog'),
        ('other', 'Other'),
    ], string='Animal Type')
    pet_type_id = fields.Many2one('pet.type', string='Pet Type')
    breed_id = fields.Many2one('pet.breed', string='Breed',
                               domain="[('pet_type_id', '=', pet_type_id)]")

    breed_size = fields.Selection([
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('all', 'All Sizes'),
    ], string='Breed Size')

    life_stage = fields.Selection([
        ('kitten', 'Kitten'),
        ('puppy', 'Puppy'),
        ('adult', 'Adult'),
        ('senior', 'Senior'),
        ('all', 'All Stages'),
    ], string='Life Stage')

    breed_specific = fields.Char(string='Breed Specific')
    recommended_age_range = fields.Char(string='Recommended Age Range')

    # -----------------------------
    # Nutrition
    # -----------------------------
    protein_source = fields.Char(string='Protein Source')
    nutritional_protein_pct = fields.Float(string='Protein (%)')
    nutritional_fat_pct = fields.Float(string='Fat (%)')
    nutritional_fibre_pct = fields.Float(string='Fibre (%)')
    kcal_per_kg = fields.Integer(string='Energy (kcal/kg)')
    allergen_flags = fields.Text(string='Allergen Information')
    # Import-only helper fields
    nutritional_protein_pct_import = fields.Float(store=False)
    nutritional_fat_pct_import = fields.Float(store=False)
    nutritional_fibre_pct_import = fields.Float(store=False)

    # -----------------------------
    # Physical Attributes
    # -----------------------------
    material = fields.Char(string='Material')
    form_factor = fields.Selection([
        ('dry', 'Dry'),
        ('wet', 'Wet'),
        ('clumping', 'Clumping'),
        ('liquid', 'Liquid'),
    ], string='Form Factor')

    texture = fields.Char(string='Texture / Shape')

    # -----------------------------
    # Marketing / Content
    # -----------------------------
    product_function = fields.Text(string='Product Function')

    benefits_text = fields.Text(
        string='Benefits',
        help='One benefit per line'
    )

    key_features_text = fields.Text(
        string='Key Features',
        help='One feature per line'
    )

    usage_instructions = fields.Text(string='Usage Instructions')
    contraindications = fields.Text(string='Contraindications')
    hazard_notes = fields.Text(string='Hazard Notes')
    storage_instruction = fields.Text(string='Storage Instructions')

    # -----------------------------
    # Certifications
    # -----------------------------
    certifications_text = fields.Text(
        string='Certifications & Compliance'
    )

    # -----------------------------
    # Commercial / Logistics
    # -----------------------------
    is_returnable = fields.Boolean(string='Returnable')
    return_policy_type = fields.Selection(
        [
            ('1', '1 Day'),
            ('2', '2 Days'),
            ('3', '3 Days'),
            ('4', '4 Days'),
            ('5', '5 Days'),
            ('6', '6 Days'),
            ('7', '7 Days'),
        ],
        string='Return Policy (Days)',
    )

    expiry_applicable = fields.Boolean(string='Expiry Applicable')
    fragile_item = fields.Boolean(string='Fragile Item')

    # -----------------------------
    # Subscription
    # -----------------------------
    recommended_for_subscription = fields.Boolean(
        string='Recommended for Subscription'
    )
    subscription_cycle = fields.Selection([
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ], string='Subscription Cycle')

    subscription_cycle_count = fields.Integer(
        string="Subscription Cycle Count",
        help="Total number of subscription deliveries"
    )
    length = fields.Float('Length', help="Length")
    height = fields.Float('Height', help="Height")
    breadth = fields.Float('Breadth', help="breadth")

    # UoM display fields
    length_uom_name = fields.Char(
        string='Length UoM',
        compute='_compute_dimension_uom_name',
        readonly=True
    )
    height_uom_name = fields.Char(
        string='Height UoM',
        compute='_compute_dimension_uom_name',
        readonly=True
    )
    breadth_uom_name = fields.Char(
        string='Breadth UoM',
        compute='_compute_dimension_uom_name',
        readonly=True
    )

    @api.depends('company_id')
    def _compute_dimension_uom_name(self):
        cm_uom = self.env.ref('uom.product_uom_cm', raise_if_not_found=False)
        for rec in self:
            rec.length_uom_name = cm_uom.name if cm_uom else 'cm'
            rec.height_uom_name = cm_uom.name if cm_uom else 'cm'
            rec.breadth_uom_name = cm_uom.name if cm_uom else 'cm'

    @api.model
    def create(self, vals):
        if 'weight' in vals:
            vals['weight'] = self._convert_grams_to_kg(vals['weight'])
        return super().create(vals)

    def write(self, vals):
        if 'weight' in vals:
            vals['weight'] = self._convert_grams_to_kg(vals['weight'])
        return super().write(vals)

    def _convert_grams_to_kg(self, value):
        if value in (None, '', False):
            return 0.0

        value = float(value)

        # If value looks like grams → convert to kg
        if value >= 1000:
            value = value / 1000

        # Round to 2 decimals (Odoo standard)
        return round(value, 2)


