# Six Paws — Pet Store ERP Customizations (Odoo 19)

![Odoo](https://img.shields.io/badge/Odoo-19.0-purple) ![Modules](https://img.shields.io/badge/Custom%20Modules-4-blue) ![License](https://img.shields.io/badge/License-LGPL--3-green)

An e-commerce/resale platform for pet-products built on Odoo 19 — **client-driven customizations**: **pet profiles**, a **customer portal for pets**, **pet-aware product customization**, and **pet-based product filtering in Sales Orders**.

```
six-paws-pet-store/
├── pet_profile/            # Pet master data (breed, type, DOB, owner, photos…)
├── pet_profile_portal/     # Portal-side access for customers to manage pets
├── product_customization/  # Pet-specific product personalization
└── sales_customization/    # Filter products in SO lines by selected pet
```

## Highlights

- **Pet Profile module** — a full pet master model with sequences, types/breeds data, owner linkage and images.
- **Portal access** — customers log into the website portal and manage their own pets (create/update), boosting self-service.
- **Pet-based selling flow** — in a Sale Order, selecting a pet auto-filters sellable products relevant to that pet (species/breed-driven domain filters), making treat/food/product ordering contextual.
- **Product customization** — pet-specific attributes/variants for personalized products.

## Dependencies

`sale, sale_portal(websites), portal, product, stock, mail` (per-module)

## License

LGPL-3 (as declared in module manifests).
