# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Odoo 19 custom addons directory for the "Six Paws" project. It contains custom modules extending Odoo's product, sales, and website functionality for a pet food and supplies business.

**Database**: `six_paws_db` (PostgreSQL on localhost:5432)
**Odoo Port**: 8069 (127.0.0.1)
**Main Module**: `product_customization` - Extends product management with pet-specific attributes

## Development Commands

### Running Odoo

Start Odoo with the configuration file:
```bash
cd /home/santosh/Documents/odoo19/source/odoo
./odoo-bin -c /home/santosh/Documents/odoo19/custom/six_paws/odoo.conf
```

Update module after changes:
```bash
./odoo-bin -c /home/santosh/Documents/odoo19/custom/six_paws/odoo.conf -u product_customization
```

Install module:
```bash
./odoo-bin -c /home/santosh/Documents/odoo19/custom/six_paws/odoo.conf -i product_customization
```

### Module Structure

Standard Odoo module layout:
- `__manifest__.py` - Module metadata, dependencies, and data files
- `__init__.py` - Python package initialization
- `models/` - Python model definitions (inherits and extends Odoo models)
- `views/` - XML view definitions (forms, trees, menus)
- `data/` - XML data files (sequences, default data)
- `security/` - Access control rules (ir.model.access.csv)
- `static/` - Static assets (images, JS, CSS)

## Architecture

### Module: product_customization

**Purpose**: Extends Odoo product management for pet food/supplies with nutrition info, pet classification, and subscription features.

**Dependencies**: `base`, `stock`, `product`, `sale`, `website_sale`

#### Core Models

**PetProfile** (`pet.profile`) - models/pet_profile.py:6
- Customer pet profiles with owner relationship
- Auto-generated unique pet codes via sequence
- Age computation from date of birth
- Vaccination tracking and status management
- Service eligibility validation based on vaccination status
- Inherits: `mail.thread`, `mail.activity.mixin`

**PetType** (`pet.type`) - models/pet_profile.py:179
- Master data for pet types (Dog, Cat, etc.)
- One-to-many relationship with breeds
- Enforces unique pet type names

**PetBreed** (`pet.breed`) - models/pet_profile.py:195
- Breed definitions linked to pet types
- Tracks average weight and lifespan
- Unique constraint per pet type

**PetVaccination** (`pet.vaccination`) - models/pet_profile.py:213
- Vaccination records per pet
- Auto-computed status: valid/expiring/expired
- Supports certificate image attachments (Many2many with ir.attachment)
- Validates that next_due_date > vaccination_date

**ProductTemplate** (extends `product.template`) - models/product_template.py:4
- Pet classification: animal_type, breed_size, life_stage
- Nutrition fields: protein_source, protein/fat/fiber percentages, kcal_per_kg
- Physical attributes: material, form_factor, texture
- Marketing content: benefits_text, key_features_text, usage_instructions
- Subscription support: recommended_for_subscription, subscription_cycle
- Weight auto-conversion: values >= 1000 treated as grams, converted to kg

#### Key Business Logic

**Vaccination Status Computation** - pet_profile.py:110
- Aggregates status from all pet vaccinations
- Returns worst-case scenario (expired > expiring > valid)
- Tracks last vaccination date and next due date

**Service Eligibility Validation** - pet_profile.py:156
- Services requiring vaccination: grooming, boarding, daycare, training
- Blocks expired/missing vaccinations with user-friendly messages

**Weight Handling** - product_template.py:165
- Intercepts create/write to convert grams to kilograms
- Values >= 1000 automatically divided by 1000

#### Views and Menus

Menu hierarchy in views/menu.xml:
```
Pet Portal (root)
├── Pets
│   ├── Pet Profiles
│   └── Vaccination Records
└── Configuration (restricted to base.group_system)
    ├── Pet Types
    └── Breeds
```

## Important Notes

- All models use tracking=True on key fields for audit trail
- Pet vaccination status auto-updates based on dates (30-day expiring threshold)
- Product weight fields expect values in kg but accept grams for convenience
- The module is application-level (`application: True` in manifest)
- No git repository is initialized in this directory
