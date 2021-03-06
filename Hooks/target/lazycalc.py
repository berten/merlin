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

import re

import tinyurl
from Core.config import Config
from Core.loadable import loadable, route, require_user
from Core.maps import Updates, Planet


class lazycalc(loadable):
    usage = " <coords> <fi|co|fr|de|cr|bs>"
    class_translation = {"fi": "Fighter",
                     "co": "Corvette",
                     "fr": "Frigate",
                     "de": "Destroyer",
                     "cr": "Cruiser",
                     "bs": "Battleship"}

    @route(r"([. :\-\d,]+)\s+([a-zA-Z]+)", access="half")
    @require_user
    def execute(self, message, user, params):
        tick = Updates.current_tick()
        url = Config.get("URL", "bcalc")
        i = 1
        coords, clazz = params.groups()
        for coord in re.findall(loadable.coord, coords):
            planet = Planet.load(coord[0], coord[2], coord[4])
            if planet:
                scan = planet.scan("A")

                if scan and (int(tick) <= scan.tick + 12):
                    url = scan.addPlanetToCalc(url, False, i, self.class_translation[clazz] if clazz in self.class_translation.keys() else None)
                else:
                    message.reply("Missing a scan for %d:%d:%d" % (
                        planet.x, planet.y, planet.z))
                    return
            i = i + 1

        message.reply("Calc: %s" % (
        tinyurl.create_one("%s&att_fleets=%d" % (url, i - 1))))
