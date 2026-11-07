from warnings import filters

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class PetPortal(CustomerPortal):

    @http.route(['/my/pets', '/my/pets/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_pets(self, page=1, search=None, sortby=None, filterby=None,**kw):
        PetModel = request.env['pet.profile']
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        searchbar_sortings = {
            'all': {'label': 'All Pets', 'domain': []},
            'new': {'label': 'Newest', 'order': 'create_date desc'},
            'name': {'label': 'Name (A-Z)', 'order': 'name asc'},
            'type': {'label': 'Pet Type (A-Z)', 'order': 'pet_type_id asc'},
            'old': {'label': 'Oldest', 'order': 'create_date asc'},
        }

        if not sortby:
            sortby = 'new'

        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': 'All Pets', 'domain': []},
            'valid': {'label': 'Valid Vaccination', 'domain': [('vaccination_status', '=', 'valid')]},
            'Expired Vaccination': {'label': 'Expired Vaccination','domain': [('vaccination_status', '=', 'expired')]},
            'Expiring Soon': {'label': 'Expiring Soon', 'domain': [('vaccination_status', '=', 'expiring')]},
        }

        if not filterby:
            filterby = 'all'

        domain += searchbar_filters[filterby]['domain']


        if search: domain += ['|', ('name', 'ilike', search), ('pet_type_id.name', 'ilike', search)]

        pet_count = PetModel.sudo().search_count(domain)
        rpg = 4
        pager = portal_pager(url="/my/pets", total=pet_count, page=page, step=rpg,
                             url_args={'search': search, 'sortby': sortby,'filterby': filterby })
        pets = PetModel.sudo().search(domain, limit=rpg, offset=pager['offset'], order=order)
        vals = {'pets': pets, 'page_name': 'pet_portal', 'pager': pager,
                'search': search, 'sortby': sortby, 'searchbar_sortings': searchbar_sortings,'searchbar_filters':searchbar_filters,'filterby': filterby }

        return request.render('pet_profile_portal.portal_my_pets', vals)

    @http.route(['/my/pets/new'], type='http', auth='user', website=True)
    def portal_pet_create(self):
        pet_types = request.env['pet.type'].sudo().search([])
        breeds = request.env['pet.breed'].sudo().search([])
        return request.render('pet_profile_portal.portal_pet_form', {
            'pet_types': pet_types,
            'breeds': breeds,
            'page_name': 'pet_form',

        })

    @http.route(['/my/pets/save'], type='http', auth='user', methods=['POST'], website=True)
    def portal_pet_save(self, **post):
        vals = {
            'name': post.get('name'),
            'partner_id': request.env.user.partner_id.id,
            'pet_type_id': int(post.get('pet_type_id')) if post.get('pet_type_id') else False,
            'breed_id': int(post.get('breed_id')) if post.get('breed_id') else False,
            'gender': post.get('gender'),
            'date_of_birth': post.get('date_of_birth'),
        }

        pet_id = post.get('pet_id')

        if pet_id:
            pet = request.env['pet.profile'].sudo().browse(int(pet_id))
            if pet.exists():
                pet.write(vals)
        else:
            request.env['pet.profile'].sudo().create(vals)

        return request.redirect('/my/pets')

    @http.route(['/my/pets/<int:pet_id>/edit'], type='http', auth='user', website=True)
    def portal_pet_edit(self, pet_id):
        pet = request.env['pet.profile'].sudo().search([
            ('id', '=', pet_id),
            ('partner_id', '=', request.env.user.partner_id.id)
        ], limit=1)

        if not pet:
            return request.render("website.404")

        pet_types = request.env['pet.type'].sudo().search([])
        return request.render('pet_profile_portal.portal_pet_form', {
            'pet': pet,
            'pet_types': pet_types,
            'breeds': pet.pet_type_id.breed_ids,
            'page_name': 'pet_form',
        })

    @http.route(['/my/pets/<int:pet_id>/delete'], type='http', auth='user', website=True)
    def portal_pet_delete(self, pet_id):
        pet = request.env['pet.profile'].sudo().search([
            ('id', '=', pet_id),
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        pet.unlink()
        return request.redirect('/my/pets')
