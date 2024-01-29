# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Product(models.Model):
    _inherit = 'product.template'

    variety_ids = fields.Many2many('botanical.variety', string = "Varieties")

