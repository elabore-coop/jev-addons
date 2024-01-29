# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class BotanicalCatalogueSection(models.Model):
    _name = "botanical.catalogue.section"
    _description = "Botanical catalogue section"
    _rec_name = 'code'

    code = fields.Char('Section')
    name = fields.Char('Complete name')
    description = fields.Char('Description')



