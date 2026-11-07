# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions,_
from dateutil.relativedelta import relativedelta


class PetProfile(models.Model):
    _name = 'pet.profile'
    _description = 'Pet Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Pet Name', required=True, tracking=True)

    pet_code = fields.Char(
        string='Pet Unique Code',
        required=True,
        readonly=True,
        copy=False,
        default=lambda self: _('New'),
        tracking=True
    )

    partner_id = fields.Many2one('res.partner', string='Owner', required=True, tracking=True)

    # Basic Information
    pet_type_id = fields.Many2one('pet.type', string='Pet Type', required=True, tracking=True)
    breed_id = fields.Many2one('pet.breed', string='Breed', required=True,
                               domain="[('pet_type_id', '=', pet_type_id)]", tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Char(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ], string='Gender', tracking=True)

    weight = fields.Float(string='Weight (kg)', tracking=True)
    color = fields.Char(string='Color/Markings', tracking=True)
    image = fields.Binary(string='Photo', attachment=True)
    microchip_number = fields.Char(string='Microchip Number', tracking=True)
    special_notes = fields.Text(string='Special Notes/Medical Conditions')

    # Vaccination Information
    vaccination_ids = fields.One2many('pet.vaccination', 'pet_id', string='Vaccination Records')
    vaccination_card_ids = fields.Many2many(
        'ir.attachment',
        compute='_compute_vaccination_cards',
        string='Vaccination Cards',
        store=False
    )

    is_vaccinated = fields.Boolean(string='Is Vaccinated', compute='_compute_vaccination_status',
                                   store=True)
    vaccination_status = fields.Selection([
        ('none', 'No Vaccination'),
        ('expired', 'Expired'),
        ('expiring', 'Expiring Soon'),
        ('valid', 'Valid')
    ], string='Vaccination Status', compute='_compute_vaccination_status', store=True, tracking=True)
    last_vaccination_date = fields.Date(string='Last Vaccination',
                                        compute='_compute_vaccination_status', store=True)
    next_vaccination_due = fields.Date(string='Next Vaccination Due',
                                       compute='_compute_vaccination_status', store=True)

    # Emergency Contact
    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone')
    preferred_veterinarian = fields.Char(string='Preferred Veterinarian')
    vet_phone = fields.Char(string='Veterinarian Phone')
    vet_address = fields.Text(string='Veterinarian Address')

    # Status
    active = fields.Boolean(string='Active', default=True)

    def _compute_vaccination_cards(self):
        for pet in self:
            pet.vaccination_card_ids = pet.vaccination_ids.mapped('certificate_image')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('pet_code', _('New')) == _('New'):
                vals['pet_code'] = (
                        self.env['ir.sequence'].next_by_code('pet.profile')
                        or _('New')
                )
        return super().create(vals_list)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                delta = relativedelta(today, record.date_of_birth)

                if delta.years > 0:
                    age_str = f"{delta.years} year{'s' if delta.years > 1 else ''}"
                    if delta.months > 0:
                        age_str += f" {delta.months} month{'s' if delta.months > 1 else ''}"
                elif delta.months > 0:
                    age_str = f"{delta.months} month{'s' if delta.months > 1 else ''}"
                else:
                    age_str = f"{delta.days} day{'s' if delta.days > 1 else ''}"

                record.age = age_str
            else:
                record.age = 'Undefined'

    @api.depends('vaccination_ids', 'vaccination_ids.status', 'vaccination_ids.next_due_date')
    def _compute_vaccination_status(self):
        for record in self:
            if not record.vaccination_ids:
                record.is_vaccinated = False
                record.vaccination_status = 'none'
                record.last_vaccination_date = False
                record.next_vaccination_due = False
            else:
                # Get all valid vaccinations
                valid_vaccinations = record.vaccination_ids.filtered(
                    lambda v: v.status in ['valid', 'expiring']
                )

                record.is_vaccinated = bool(valid_vaccinations)

                # Get the most recent vaccination date
                sorted_vaccinations = record.vaccination_ids.sorted('vaccination_date', reverse=True)
                record.last_vaccination_date = sorted_vaccinations[0].vaccination_date

                # Get the earliest due date
                upcoming_vaccinations = record.vaccination_ids.filtered(
                    lambda v: v.next_due_date and v.next_due_date >= fields.Date.today()
                )
                if upcoming_vaccinations:
                    sorted_upcoming = upcoming_vaccinations.sorted('next_due_date')
                    record.next_vaccination_due = sorted_upcoming[0].next_due_date
                else:
                    record.next_vaccination_due = False

                # Determine overall status (worst case)
                if any(v.status == 'expired' for v in record.vaccination_ids):
                    record.vaccination_status = 'expired'
                elif any(v.status == 'expiring' for v in record.vaccination_ids):
                    record.vaccination_status = 'expiring'
                elif any(v.status == 'valid' for v in record.vaccination_ids):
                    record.vaccination_status = 'valid'
                else:
                    record.vaccination_status = 'none'

    @api.onchange('pet_type_id')
    def _onchange_pet_type_id(self):
        if self.pet_type_id:
            self.breed_id = False

    def validate_service_eligibility(self, service_type):
        """
        Validate if pet is eligible for a service based on vaccination status
        Returns: (eligible: bool, message: str)
        """
        self.ensure_one()

        # Services that require valid vaccination
        vaccination_required_services = ['grooming', 'boarding', 'daycare', 'training']

        if service_type in vaccination_required_services:
            if self.vaccination_status == 'expired':
                return False, _('This pet has expired vaccinations. Please update vaccination records before booking.')
            elif self.vaccination_status == 'none':
                return False, _('This pet has no vaccination records. Please upload vaccination card before booking.')
            elif self.vaccination_status == 'expiring':
                return True, _('Warning: Pet vaccinations are expiring soon. Please consider updating them.')
            else:
                return True, _('Pet is eligible for this service.')

        return True, _('No vaccination requirement for this service.')


class PetType(models.Model):
    _name = 'pet.type'
    _description = 'Pet Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Pet Type', required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    breed_ids = fields.One2many('pet.breed', 'pet_type_id', string='Breeds')
    active = fields.Boolean(string='Active', default=True)
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Pet type must be unique!')
    ]


class PetBreed(models.Model):
    _name = 'pet.breed'
    _description = 'Pet Breed'
    _order = 'pet_type_id, name'

    name = fields.Char(string='Breed Name', required=True, translate=True)
    pet_type_id = fields.Many2one('pet.type', string='Pet Type', required=True, ondelete='cascade')
    description = fields.Text(string='Description')
    average_weight = fields.Float(string='Average Weight (kg)')
    average_lifespan = fields.Integer(string='Average Lifespan (years)')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_type_unique', 'UNIQUE(name, pet_type_id)',
         'This breed already exists for this pet type!')
    ]


class PetVaccination(models.Model):
    _name = 'pet.vaccination'
    _description = 'Pet Vaccination Record'
    _order = 'vaccination_type'

    pet_id = fields.Many2one('pet.profile', string='Pet', required=True, ondelete='cascade')
    vaccination_type = fields.Selection([
        ('rabies', 'Rabies'),
        ('dhpp', 'DHPP (Distemper, Hepatitis, Parvovirus, Parainfluenza)'),
        ('bordetella', 'Bordetella (Kennel Cough)'),
        ('leptospirosis', 'Leptospirosis'),
        ('lyme', 'Lyme Disease'),
        ('fvrcp', 'FVRCP (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia)'),
        ('felv', 'FeLV (Feline Leukemia)'),
        ('other', 'Other')
    ], string='Vaccination Type', required=True)

    other_vaccination_name = fields.Char(string='Other Vaccination Name')

    vaccination_date = fields.Date(string='Vaccination Date', required=True,
                                   default=fields.Date.today)
    next_due_date = fields.Date(string='Next Due Date')

    veterinarian = fields.Char(string='Veterinarian Name')
    vet_license_number = fields.Char(string='Vet License Number')
    batch_number = fields.Char(string='Vaccine Batch Number')
    certificate_image = fields.Many2many(
        'ir.attachment',
        'pet_vaccination_certificate_rel',  # UNIQUE
        'vaccination_id',
        'attachment_id',
        string='Vaccination Certificate',
        help='Upload vaccination images or PDFs'
    )
    notes = fields.Text(string='Notes')

    status = fields.Selection([
        ('expired', 'Expired'),
        ('expiring', 'Expiring Soon'),
        ('valid', 'Valid')
    ], string='Status', compute='_compute_status', store=True)

    @api.depends('next_due_date')
    def _compute_status(self):
        today = fields.Date.today()
        for record in self:
            if record.next_due_date:
                delta = (record.next_due_date - today).days

                if delta < 0:
                    record.status = 'expired'
                elif delta <= 30:
                    record.status = 'expiring'
                else:
                    record.status = 'valid'
            else:
                record.status = 'expired'

    @api.constrains('vaccination_date', 'next_due_date')
    def _check_dates(self):
        for record in self:
            if record.next_due_date and record.vaccination_date:
                if record.next_due_date <= record.vaccination_date:
                    raise exceptions.ValidationError(
                        _('Next due date must be after vaccination date!')
                    )
