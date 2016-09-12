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

from Core.config import Config
from Core.maps import User
from Core.loadable import loadable, route, require_user
if Config.get("Twilio", "sid"):
    from twilio.rest import TwilioRestClient

class forcecall(loadable):
    """Calls the user's phone."""
    usage = " <phonenumber>"
    
    @route(r"(\S+)", access = "hc")
    @require_user
    def execute(self, message, user, params):
        if not Config.get("Twilio", "sid"):
            message.reply("Twilio support not configured. Tell the admin. If you are the admin, configure Twilio or disable !call to prevent this message.")
            return

        rec = params.group(1)



        phone = self.prepare_phone_number(rec)
        if not phone or len(phone) <= 7:
            message.reply("No phone number or phone number is too short to be valid (under 6 digits). No call made." % (rec,))
            return

        client = TwilioRestClient(Config.get("Twilio", "sid"), Config.get("Twilio", "auth_token"))
        if Config.getboolean("Twilio", "warn"):
            url="http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%20voice%3D%22alice%22%20language%3D%22en-GB%22%20%3EHello.%20This%20is%20" +\
                Config.get("Connection", "nick") + ".%20Stop%20wasting%20our%20credit!%3C%2FSay%3E%3CHangup%2F%3E%3C%2FResponse%3E&",
        else:
            url="http://twimlets.com/echo?Twiml=%3CResponse%3E%3CHangup%2F%3E%3C%2FResponse%3E&",
        tw = client.calls.create(to=phone, from_=Config.get("Twilio", "number"), url=url, Timeout=Config.getint("Twilio", "timeout"))

        if tw.sid:
            message.reply("Successfully called %s." % (rec))
        else:
            message.reply("Error: Failed to get call ID from Twilio server.")
        
    def prepare_phone_number(self,text):
        if not text:
            return text
        s = "".join([c for c in text if c.isdigit()])
        return "+"+s.lstrip("00")
