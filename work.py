#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta

__all__ = ['Work', 'WorkCurrentEffort']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'

    current_effort = fields.Function(fields.Float('Current Effort'),
        'get_current_effort')

    remain_hours = fields.Function(fields.Float('Remain Hours',
        digits=(16, 2)), 'get_remain_hours', searcher='search_remain_hours')

    current_efforts = fields.One2Many('project.work.current_effort', 'work',
        'Current Efforts')

    def get_current_effort(self, name):
        if not self.current_efforts:
            return self.effort
        return (self.hours or 0) + (self.current_efforts[0].remain_hours or 0)

    def get_remain_hours(self, name):
        if not self.current_efforts:
            return (self.effort or 0) - (self.hours or 0)
        return self.current_efforts[0].remain_hours


class WorkCurrentEffort(ModelSQL, ModelView):
    '''Work Schedule'''
    __name__ = 'project.work.current_effort'
    _rec_name = 'date'


    remain_hours = fields.Float('Remain Hours', digits=(16, 2), required=True)
    work = fields.Many2One('project.work', 'Work', required=True, select=True)
    date = fields.Function(fields.DateTime('Date'), 'get_date')

    def get_date(self, name):
        return self.create_date

    @classmethod
    def __setup__(cls):
        super(WorkCurrentEffort, cls).__setup__()
        cls._order.insert(0, ('create_date', 'DESC'))
