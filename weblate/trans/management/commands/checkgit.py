# -*- coding: utf-8 -*-
#
# Copyright © 2012 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.core.management.base import BaseCommand
from weblate.trans.models import SubProject
from optparse import make_option

class Command(BaseCommand):
    help = 'checks status of git repo'
    args = '<project/subproject>'
    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all',
            default=False,
            help='Check all projects'),
        )

    def handle(self, *args, **options):
        '''
        Shows status of git repository in given projects.
        '''
        if options['all']:
            for s in SubProject.objects.all():
                r = s.get_repo()
                print '%s:' % s
                print r.git.status()
        for arg in args:
            prj, subprj = arg.split('/')
            s = SubProject.objects.get(slug = subprj, project__slug = prj)
            r = s.get_repo()
            print '%s:' % s
            print r.git.status()


