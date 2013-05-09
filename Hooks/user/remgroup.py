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
 
# Module by Martin Stone

from Core.db import session
from Core.maps import Group
from Core.loadable import loadable, route, require_user

class remgroup(loadable):
    """Remove a user group. Moves users to Public unless an alternative is specified."""
    usage = " <name> [new group]"
    alias = "delgroup"
    access = 1 # Admin
    
    @route(r"(\S+)(?:\s+(\S+)+)", access = "remgroup")
    @require_user
    def execute(self, message, user, params):
        
        name = params.group(1).lower()

        g = Group.load(name)
        if not g:
            message.reply("Group '%s' does not exist." % (name))
            return
        if g.id in [1,2,3]:
            message.reply("Can't remove the %s group" % (g.name))
            return
        if g.admin_only and not user.is_admin:
            message.reply("You don't have access to delete the %s group." % (g.name,))
            return

        newgroup = params.group(2)
        if newgroup:
            ng = Group.load(newgroup.lower())
            if not ng:
                message.reply("Group '%s' does not exist." % (newgroup))
                return
            if ng.admin_only and not user.is_admin:
                message.reply("You don't have access to the %s group." % (ng.name,))
                return
        else:
            ng = Group.load(id=2)

        for u in g.users:
            u.group = ng

        session.delete(g)
        session.commit()
        message.reply("'%s' group has been deleted." % (g.name))
