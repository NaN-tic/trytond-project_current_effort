# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.modules.company.tests import create_company, set_company


class ProjectCurrentEffortTestCase(ModuleTestCase):
    'Test Project Current Effort module'
    module = 'project_current_effort'

    @with_transaction()
    def test_efforts(self):
        'Test efforts'
        pool = Pool()
        Party = pool.get('party.party')
        TimesheetWork = pool.get('timesheet.work')
        TimesheetLine = pool.get('timesheet.line')
        ProjectWork = pool.get('project.work')
        Employee = pool.get('company.employee')
        Effort = pool.get('project.work.current_effort')

        party, = Party.create([{
                    'name': 'Pam Beesly',
                    }])
        company = create_company()
        with set_company(company):
            t_work, = TimesheetWork.create([{
                        'name': 'Work 1',
                        'company': company.id,
                        'timesheet_available': True,
                        }])
            p_work, = ProjectWork.create([{
                        'name': 'Work 1',
                        'company': company.id,
                        'work': t_work.id,
                        'effort_duration': datetime.timedelta(hours=1),
                        }])
            self.assertEqual(p_work.current_effort,
                datetime.timedelta(hours=1))
            self.assertEqual(p_work.remain_duration,
                datetime.timedelta(hours=1))

            employee, = Employee.create([{
                        'party': party.id,
                        'company': company.id,
                        }])

            TimesheetLine.create([{
                        'employee': employee.id,
                        'company': company.id,
                        'work': t_work.id,
                        'duration': datetime.timedelta(minutes=30),
                        }])

            self.assertEqual(p_work.current_effort,
                datetime.timedelta(minutes=90)) # 1:30
            self.assertEqual(p_work.remain_duration,
                datetime.timedelta(minutes=60)) # 1:00

            Effort.create([{
                        'work': t_work.id,
                        'remain_duration': datetime.timedelta(hours=1),
                        }])

            self.assertEqual(p_work.current_effort,
                datetime.timedelta(hours=1, minutes=30))
            self.assertEqual(p_work.remain_duration,
                datetime.timedelta(hours=1))


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProjectCurrentEffortTestCase))
    return suite
