from odoo import models, fields, api, _


class CustomerPaymentReportWizard(models.TransientModel):
    _name = "customer.payment.report.wizard"
    _description = "Customer Payment Detail Report"

    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')

    def action_print_report(self):
        report_date_from = self.date_from.strftime('%d-%b-%Y')
        report_date_to = self.date_to.strftime('%d-%b-%Y')
        print("report_date_to", report_date_to)
        print("report_date_from", report_date_from)

        query = """
                      SELECT
                          move.partner_id,
                          partner.name AS partner_name,
                          MIN(move.create_date) AS first_sales_date,
                          COUNT(move.id) AS total_sale_count,
                          pmt.amount AS total_paid_amount,
                          SUM(move.amount_total) AS total_amount,
                          (SUM(move.amount_total) - pmt.amount) AS balance_amount
                      FROM
                          account_move AS move
                      LEFT JOIN res_partner AS partner ON move.partner_id = partner.id
                      LEFT JOIN (
                          SELECT
                              pmt.partner_id,
                              SUM(pmt.amount) AS amount
                          FROM
                              account_payment AS pmt
                          WHERE
                              pmt.payment_type = 'inbound'
                          GROUP BY
                              pmt.partner_id
                      ) AS pmt ON move.partner_id = pmt.partner_id
                      WHERE
                          move.move_type = 'out_invoice'
                           AND DATE(move.date) BETWEEN '%s' AND '%s'
                      GROUP BY
                          move.partner_id, partner.name, pmt.amount
                  """ % (report_date_from, report_date_to)

        self._cr.execute(query)
        payment_data = self._cr.dictfetchall()
        print(payment_data)

        data = {
            'ids': self.ids,
            'model': self._name,
            'date_from': report_date_from,
            'date_to': report_date_to,
            'vals': payment_data
        }
        print('data', data)

        action = self.env.ref('customer_payment.customer_payment_report_print_id').report_action(self, data=data)

        return action
