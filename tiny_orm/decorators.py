def singleton(klass):
	class Decorated(klass):
		def __init__(self, *args, **kwargs):
			if hasattr(klass, '__init__'):
				klass.__init__(self, *args, **kwargs)
		def __repr__(self): return klass.__name__ + " obj"
		__str__ = __repr__
	Decorated.__name__ = klass.__name__
	class ClassObject:
		def __init__(cls):
			cls.instance = None
		def __repr__(cls):
			return klass.__name__
		__str__ = __repr__
		def __call__(cls, *args, **kwargs):
			if not cls.instance:
				cls.instance = Decorated(*args, **kwargs)
			return cls.instance

	return ClassObject()