# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

from Core.loadable import loadable, route, require_user
from Core.maps import Alliance, Updates


class stock(loadable):
    usage = " alliance"

    @route(r"(\S+)")
    @require_user
    def user_alliance(self, message, user, params):
        alliance = Alliance.load(params.group(1)) if params.group(1) is not None else None
        resources = 0
        scansneeded = ""
        tick = Updates.current_tick()
        # Alliance
        if alliance is not None:
            for planet in alliance.intel_planets:
                scan = planet.scan("P")
                if scan and (int(tick) <= scan.tick + 12):
                    resources += scan.planetscan.res_metal + scan.planetscan.res_crystal + scan.planetscan.res_eonium
                else:
                    scansneeded += "%d:%d:%d " % (planet.x, planet.y, planet.z)
            message.reply("Stocked resources: %d Added value: %d Need scans for (%s)" %(resources, int(round((resources / 100) - (resources / 150))), scansneeded))
            return
        else:
            message.reply("No alliance matching '%s' found" % (params.group(1)))
