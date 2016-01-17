### tiny-orm

A wee little layer on top of TinyDB that provides a few ORM conveniences like those found in django.


### Example:

```python
import unittest

from tiny_orm import *


class Address(Model):
	def __init__(self, *args, **kwargs):
		self.address = None
		self.city = None

		super(Address, self).__init__(*args, **kwargs)


class Person(Model):
	def __init__(self, *args, **kwargs):
		self.first_name = None
		self.last_name = None
		self.age = None
		self.address_id = None

		super(Person, self).__init__(*args, **kwargs)

	@property
	def address(self):
		return Address.objects().first(self.address_id)


class TestTinyOrm(unittest.TestCase):

	def test(self):
		address = Address()
		address.address = '10 Downing Street'
		address.city = 'London'
		address.save()

		person = Person()
		person.address_id = address.id
		person.first_name = 'Sherlock'
		person.last_name = 'Holmes'
		person.age = 3
		person.save()

		assert Address.objects().find(address.id).id == person.id
		assert Person.objects().find(person.id).id == person.id
		assert Person.objects().find(person.id).address.id == Address.objects().find(address.id).id

		query = Query()

		assert Person.objects().find(query.first_name == 'Sherlock')[0].id == person.id

		person.delete()
		address.delete()

		assert Address.objects().find(address.id) is None
		assert Person.objects().find(person.id) is None

```