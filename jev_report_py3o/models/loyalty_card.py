# -*- coding: utf-8 -*-

from odoo import api, fields, models

class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    points_int = fields.Integer('Rounded points', compute='_compute_rounded_points')

    @api.depends('points')
    def _compute_rounded_points(self):
        for card in self:
            if card.points :
                card.points_int = int(card.points)
            else:
                card.points_int = False