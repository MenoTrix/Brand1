from odoo import models, fields, api

class Brand(models.Model):
    _inherit = "product.template"
    custom_value = fields.One2many(
        "brand.form", "brand_inherit", string="Brand", copy=True
    )
    brand_name = fields.Char(string="Brand Name")

    @api.constrains("custom_value")
    def add_brand(self):
        if self.custom_value:
            result = self.env["product.attribute"].search([("name", "=", "brand")])
            if not result:
                brand_attribute = self.env["product.attribute"].create(
                    {"name": "brand"}
                )
            else:
                brand_attribute = result[0]  # Retrieve the existing attribute

            existing_values = brand_attribute.value_ids.mapped("name")  # Retrieve existing attribute values
            for brand_form in self.custom_value:
                if brand_form.name not in existing_values:
                    val = self.env["product.attribute.value"].create(
                        {
                            "name": brand_form.name,
                            "attribute_id": brand_attribute.id,
                        }
                    )
                    self.attribute_line_ids.create(
                        {
                            "attribute_id": brand_attribute.id,
                            "product_tmpl_id": self.id,
                            "value_ids": [(4, val.id)],
                        }
                    )
                add_data = self.env["product.template.attribute.value"].create({
                    "name": "Meno",
                    # "product_template_variant_values_ids": ["testt", "test2"],
                    "product_attribute_value_id": brand_attribute.id,
                    "attribute_line_id": self.id,
                    "price_extra": 20
                })


class BrandForm(models.Model):
    _name = "brand.form"
    brand_inherit = fields.Many2one("product.template", string="Product")
    name = fields.Char(string="Brand Name")
    price = fields.Float(string="Brand Price")
    is_added = fields.Boolean(default=False)

