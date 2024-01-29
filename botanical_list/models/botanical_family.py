# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class BotanicalFamily(models.Model):
    _name = "botanical.family"
    _description = "Botanical family"

    name = fields.Char('Family name')


