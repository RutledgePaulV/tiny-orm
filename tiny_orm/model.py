from tinydb import *

from .decorators import *


@singleton
class Store(TinyDB):
	pass


class EntityManagerMeta(type):
	def __init__(cls, what, bases=None, dict=None):
		if cls.__name__ is not 'Model':
			cls.em = cls.store.table(cls.__name__)
		super().__init__(what, bases, dict)


# base model object
class Model(object, metaclass=EntityManagerMeta):
	store = Store('db.json')

	def __init__(self, *args, **kwargs):
		for key, value in kwargs.items():
			if not callable(value) and not key.startswith('_'):
				self.__dict__[key] = value

	@classmethod
	def objects(cls):
		return Manager(cls)

	@property
	def dictify(self):
		fields = dict((key, value) for key, value in self.__dict__.items()
		              if not callable(value) and not key.startswith('_'))
		return fields

	def save(self):
		if hasattr(self, 'id') and self.id:
			self.em.update(self.dictify, eids=[self.id])
		else:
			self.id = self.em.insert(self.dictify)
		return self

	def delete(self):
		if hasattr(self, 'id') and self.id:
			self.em.remove(eids=[self.id])

	def __str__(self):
		return str(self.__dict__)

	def __unicode__(self):
		return str(self.__dict__)


# accompanying object for querying against models
class Manager(object):
	def __init__(self, model_class: type):
		self.model_class = model_class
		self.em = model_class.em

	def _model(self, result):
		if result is None: return None
		instance = self.model_class(**result)
		instance.id = result.eid
		return instance

	def exists(self, query=None):
		query = Query() if query is None else query
		return self.em.exists(query)

	def first(self, query=None):
		if isinstance(query, int):
			return self._model(self.em.get(eid=query))
		query = Query() if query is None else query
		return self._model(self.em.get(query))

	def find(self, query=None):
		if isinstance(query, int):
			return self._model(self.em.get(eid=query))
		query = Query() if query is None else query
		return list(map(self._model, self.em.search(query)))

	def all(self):
		return list(map(self._model, self.em.all()))
