# -*- coding: utf-8 -*-
# © 2018 Marina Domingues, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBrCnabPayment(TransactionCase):

    def setUp(self):
        super(TestBrCnabPayment, self).setUp()
        self.main_company = self.env.ref('base.main_company')
        self.currency_real = self.env.ref('base.BRL')
        self.main_company.write({
            'name': 'Trustcode',
            'legal_name': 'Trustcode Tecnologia da Informação',
            'cnpj_cpf': '92.743.275/0001-33',
            'zip': '88037-240',
            'street': 'Vinicius de Moraes',
            'number': '42',
            'district': 'Córrego Grande',
            'country_id': self.env.ref('base.br').id,
            'state_id': self.env.ref('base.state_br_sc').id,
            'city_id': self.env.ref('br_base.city_4205407').id,
            'phone': '(48) 9801-6226',
        })
        self.main_company.write({'inscr_est': '219.882.606'})
        self.revenue_account = self.env['account.account'].create({
            'code': '3.0.0',
            'name': 'Receita de Vendas',
            'user_type_id': self.env.ref(
                'account.data_account_type_revenue').id,
            'company_id': self.main_company.id
        })
        self.receivable_account = self.env['account.account'].create({
            'code': '1.0.0',
            'name': 'Conta de Recebiveis',
            'reconcile': True,
            'user_type_id': self.env.ref(
                'account.data_account_type_receivable').id,
            'company_id': self.main_company.id
        })

        self.default_ncm = self.env['product.fiscal.classification'].create({
            'code': '0201.20.20',
            'name': 'Furniture',
            'federal_nacional': 10.0,
            'estadual_imposto': 10.0,
            'municipal_imposto': 10.0,
            'cest': '123'
        })
        self.default_product = self.env['product.product'].create({
            'name': 'Normal Product',
            'default_code': '12',
            'fiscal_classification_id': self.default_ncm.id,
            'list_price': 15.0
        })
        self.partner_fisica = self.env['res.partner'].create(dict(
            name='Parceiro',
            company_type='person',
            is_company=False,
            street='Donicia',
            zip='88032-050',
            cnpj_cpf='066.212.049-30',
            district='Centro',
            number=45,
            property_account_receivable_id=self.receivable_account.id,
            country_id=self.env.ref('base.br').id,
            state_id=self.env.ref('base.state_br_sc').id,
            city_id=self.env.ref('br_base.city_4205407').id,
        ))

        order_line_data = [
            (0, 0,
                {
                    'product_id': self.default_product.id,
                    'product_uom': self.default_product.uom_id.id,
                    'product_uom_qty': 10.0,
                    'name': 'product test 5',
                    'price_unit': 100.00,
                    'cfop_id': self.env.ref(
                        'br_data_account_product.cfop_5101').id,
                    'icms_cst_normal': '40',
                    'icms_csosn_simples': '102',
                    'ipi_cst': '50',
                    'pis_cst': '01',
                    'cofins_cst': '01',
                }
             ),
            (0, 0,
                {
                    'product_id': self.service.id,
                    'product_uom': self.service.uom_id.id,
                    'product_uom_qty': 10.0,
                    'name': 'product test 5',
                    'price_unit': 100.00,
                    'cfop_id': self.env.ref(
                        'br_data_account_product.cfop_5101').id,
                    'pis_cst': '01',
                    'cofins_cst': '01',
                }
             )
        ]
