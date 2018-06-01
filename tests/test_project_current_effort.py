# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime
import doctest
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT
from trytond.tests.test_tryton import ModuleTestCase
from trytond.transaction import Transaction


class TestCase(ModuleTestCase):
    'Test module'
    module = 'project_current_effort'

    def setUp(self):
        super(TestCase, self).setUp()
        self.timesheet_work = POOL.get('timesheet.work')
        self.timesheet_line = POOL.get('timesheet.line')
        self.project_work = POOL.get('project.work')
        self.company = POOL.get('company.company')
        self.employee = POOL.get('company.employee')
        self.effort = POOL.get('project.work.current_effort')

    def test_efforts(self):
        'Test efforts'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            company, = self.company.search([
                    ('rec_name', '=', 'Dunder Mifflin'),
                    ])

            t_work, = self.timesheet_work.create([{
                        'name': 'Work 1',
                        'company': company.id,
                        'timesheet_available': True,
                        }])
            p_work, = self.project_work.create([{
                        'name': 'Work 1',
                        'company': company.id,
                        'work': t_work.id,
                        'effort_duration': datetime.timedelta(hours=1),
                        }])
            self.assertEqual(p_work.current_effort,
                datetime.timedelta(hours=1))
            self.assertEqual(p_work.remain_duration,
                datetime.timedelta(hours=1))

            employee, = self.employee.search([('company', '=', company.id)])

            self.timesheet_line.create([{
                        'employee': employee.id,
                        'company': company.id,
                        'work': t_work.id,
                        'duration': datetime.timedelta(minutes=30),
                        }])

            self.assertEqual(p_work.current_effort,
                datetime.timedelta(minutes=90))
            self.assertEqual(p_work.remain_duration,
                datetime.timedelta(minutes=60))

            self.effort.create([{
                        'work': t_work.id,
                        'remain_duration': datetime.timedelta(hours=1),
                        }])

            self.assertEqual(p_work.current_effort,
                datetime.timedelta(hours=1, minutes=30))
            self.assertEqual(p_work.remain_duration,
                datetime.timedelta(hours=1))


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite and not isinstance(test, doctest.DocTestCase):
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
