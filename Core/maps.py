# This file is part of Merlin.
 
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
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from .variables import access

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	name = Column(String) # pnick <- we could have two separate field for user and pnick, don't think it's needed
	passwd = Column(String)
	active = Column(Boolean, default=True)
	access = Column(Integer)
	#planet_id - reference to planet_canon - on delete cascade
	email = Column(String) # regex constraint here would be cool, can sqla do that? <-- yes it can, see passwd validation below
	phone = Column(String)
	pubphone = Column(Boolean, default=False) # Asc
	sponsor = Column(String) # Asc
	#invites = Column - check >=0 # Asc
	quits = Column(Integer) # Asc
	stay = Column(Boolean) # Asc
	
	@staticmethod
	def load(id=None, name=None, passwd=None, exact=True, active=True):
		assert id or name
		session = Session()
		Q = session.query(User)
		if id is not None:
			Q = Q.filter(User.id == id)
		if name is not None:
			if (exact is not True) and Q.filter(User.name.like(name)).count() < 1:
				Q = Q.filter(User.name.like(like("%"+name+"%")))
			else:
				Q = Q.filter(User.name.like(name))
		if passwd is not None:
			Q = Q.filter(User.passwd == func.MD5(passwd))
		if active is True:
			Q = Q.filter(User.active == True)
		user = Q.first()
		session.close()
		return user
	
	@validates('passwd')
	def hash_paswd(self, key, passwd):
		return func.MD5(passwd)

def user_access_function(num):
	# Function generator for access check
	def func(self):
		if self.access & num == num:
			return True
	return func

# Bind user access functions
for lvl, num in access.items():
	setattr(User, "is_"+lvl, user_access_function(num))

class Ship(Base):
	__tablename__ = 'ships'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	class_ = Column(String)
	t1 = Column(String)
	t2 = Column(String)
	t3 = Column(String)
	type = Column(String)
	init = Column(Integer)
	guns = Column(Integer)
	armor = Column(Integer)
	damage = Column(Integer)
	empres = Column(Integer)
	metal = Column(Integer)
	crystal = Column(Integer)
	eonium = Column(Integer)
	total_cost = Column(Integer)
	race = Column(String)
	
	@staticmethod
	def load(id=None, name=None):
		assert id or name
		session = Session()
		Q = session.query(Ship)
		if id is not None:
			Q = Q.filter(Ship.id == id)
		if name is not None:
			if Q.filter(Ship.name.like(name)).count() < 1:
				if Q.filter(Ship.name.like("%"+name+"%")) < 1 and name[-1].lower()=="s":
					Q = Q.filter(Ship.name.like("%"+name[:-1]+"%"))
				else:
					Q = Q.filter(Ship.name.like("%"+name+"%"))
			else:
				Q = Q.filter(Ship.name.like(name))
		ship = Q.first()
		session.close()
		return ship
