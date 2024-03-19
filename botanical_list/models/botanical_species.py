# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class BotanicalSpecies(models.Model):
    _name = "botanical.species"
    _description = "Botanical Species"
    #_rec_name = 'name'

    name = fields.Char('Commercial name')
    description = fields.Char('Description')
    gardening_advice = fields.Char('Gardening advice')
    default_pmg = fields.Float('default TSW')
    family_id = fields.Many2one("botanical.family", string = "Botanical family")

