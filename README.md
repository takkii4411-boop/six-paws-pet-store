# Six Paws — Pet Store ERP Customizations (Odoo 19)

![Odoo](https://img.shields.io/badge/Odoo-19.0-purple) ![Modules](https://img.shields.io/badge/Custom%20Modules-4-blue) ![License](https://img.shields.io/badge/License-LGPL--3-green)

An e-commerce/resale platform for pet-products built on Odoo 19. **My work: the `pet_profile` master-data module and the `sales_customization` pet-based product filtering in Sale Orders** — co-built with the team; the **portal** and **product_customization** modules are team deliverables bundled here for full-suite context.

```
six-paws-pet-store/
├── pet_profile/            # Pet master data (breed, type, DOB, owner, photos…) ← MY WORK
├── pet_profile_portal/     # Portal-side access for customers to manage pets (team)
├── product_customization/  # Pet-specific product personalization (team)
└── sales_customization/    # Filter products in SO lines by selected pet ← MY WORK
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
