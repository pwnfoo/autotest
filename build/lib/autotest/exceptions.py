# -*- coding: utf-8 -*-
# This file is part of autotest project.
#
# autotest is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# autotest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with autotest.  If not, see <http://www.gnu.org/licenses/>.
"""
This module contains exceptions raised by autotest.



"""


class HotnessException(Exception):
    """The base exception class for all hotness-related errors"""


class SpecUrlException(HotnessException, ValueError):
    """Raised when a specfile's Source URLs don't work with autotest"""


class DownloadException(HotnessException, IOError):
    """Raised when a networking-related download error occurs"""
