#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta

__all__ = ['Work', 'WorkCurrentEffort']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'

    current_effort = fields.Function(fields.TimeDelta('Current Effort',
            'company_work_time'),
        'get_current_effort')

    remain_duration = fields.Function(fields.TimeDelta('Remain Duration',
            'company_work_time'),
        'get_remain_duration', searcher='search_remain_hours')

    current_efforts = fields.One2Many('project.work.current_effort', 'work',
        'Current Efforts')

    def get_current_effort(self, name):
        return self.timesheet_duration + self.remain_duration

    def get_remain_duration(self, name):
        if not self.current_efforts:
            return self.effort_duration - self.timesheet_duration
        return self.current_efforts[0].remain_duration


class WorkCurrentEffort(ModelSQL, ModelView):
    '''Work Schedule'''
    __name__ = 'project.work.current_effort'
    _rec_name = 'date'

    remain_duration = fields.TimeDelta('Remain Duration', 'company_work_time',
        required=True)
    work = fields.Many2One('project.work', 'Work', required=True, select=True)
    date = fields.Function(fields.DateTime('Date'), 'get_date')

    @classmethod
    def __setup__(cls):
        super(WorkCurrentEffort, cls).__setup__()
        cls._order.insert(0, ('create_date', 'DESC'))

    def get_date(self, name):
        return self.create_date
