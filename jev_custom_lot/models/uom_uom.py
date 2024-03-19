# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockQuant(models.Model):
    _inherit = 'uom.uom'

    is_seeds = fields.Boolean('This product is sold per seed')
