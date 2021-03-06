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

from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django import template
from django.conf import settings

import re

import weblate
import weblate.trans

from weblate.trans.simplediff import htmlDiff
from weblate.trans.util import split_plural
from weblate.lang.models import Language
from weblate.trans.models import Project, SubProject, Dictionary
from weblate.trans.checks import CHECKS

register = template.Library()


def fmt_whitespace(value):
    value = re.sub(r'(  +| $|^ )', '<span class="hlspace">\\1</span>', value)
    return value

@register.filter
@stringfilter
def fmttranslation(value, language = None, diff = None):
    if language is None:
        language = Language.objects.get(code = 'en')
    plurals = split_plural(value)
    if diff is not None:
        diff = split_plural(diff)
    parts = []
    for idx, value in enumerate(plurals):
        value = escape(force_unicode(value))
        if diff is not None:
            diffvalue = escape(force_unicode(diff[idx]))
            value = htmlDiff(diffvalue, value)
        value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
        paras = re.split('\n', value)
        paras = [fmt_whitespace(p) for p in paras]
        if len(plurals) > 1:
            value = '<span class="pluraltxt">%s</span><br />' % language.get_plural_label(idx)
        else:
            value = ''
        value += u'<span class="hlspace">↵</span><br />'.join(paras)
        parts.append(value)
    value = '<hr />'.join(parts)
    return mark_safe(value)

@register.filter
@stringfilter
def fmttranslationdiff(value, other):
    return fmttranslation(value, other.translation.language, other.target)

@register.filter
@stringfilter
def site_title(value):
    return settings.SITE_TITLE

@register.simple_tag
def check_name(check):
    return CHECKS[check].name

@register.simple_tag
def check_description(check):
    return CHECKS[check].description

@register.simple_tag
def project_name(prj):
    return Project.objects.get(slug = prj).__unicode__()

@register.simple_tag
def subproject_name(prj, subprj):
    return SubProject.objects.get(project__slug = prj, slug = subprj).__unicode__()

@register.simple_tag
def language_name(code):
    return Language.objects.get(code = code).__unicode__()

@register.simple_tag
def dictionary_count(lang, project):
    return Dictionary.objects.filter(project = project, language = lang).count()
