from odoo import models, fields, api


class Supplier(models.Model):
    _name = "supplier.info"

    partner_id = fields.Many2one("res.partner")
    product_id = fields.Many2one("product.product")
    supplier_id = fields.Many2one("purchase.order")


class SupplierInfo(models.Model):
    _inherit = "purchase.order"

    supplier_info_ids = fields.One2many('supplier.info',
                                        'supplier_id', string="Supplier Info", readonly=True)

    @api.constrains("order_line")
    def supplier(self):
        for lines in self.order_line:
            for record in lines.product_id.seller_ids:
                if self.partner_id.id != record.partner_id.id:
                    self.supplier_info_ids.create({
                            'partner_id': record.partner_id.id,
                            'product_id': lines.product_id.id,
                            'supplier_id': self.id
                    })