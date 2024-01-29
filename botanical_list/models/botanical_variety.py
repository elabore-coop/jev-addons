# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class BotanicalVariety(models.Model):
    _name = "botanical.variety"
    _description = "Botanical variety"
    _rec_name = "complete_name"

    complete_name = fields.Char('Complete name')
    commercial_name = fields.Char('Commercial name')
    latin_name = fields.Char('Latin name')
    life_cycle = fields.Selection([('perennial', 'Perennial'), ('perennial_biennial', 'Perennial biennial'), ('biennial', 'Biennial'), ('annual','Annual')])
    description = fields.Text('Description')
    gardening_advice = fields.Char('Gardening advice')
    notes = fields.Char('Notes')
    characteristic = fields.Char('Characteristic')

    species_id = fields.Many2one('botanical.species', string = "Botanical species")
    catalogue_section_id = fields.Many2one("botanical.catalogue.section", string = "Catalogue section")

    product_ids = fields.Many2many('product.template', string = "Products")
