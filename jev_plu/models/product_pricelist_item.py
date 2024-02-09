# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    plu = fields.Integer('PLU code', help="Indicate here which PLU code this pricing rule corresponds to")