"""

"""
is_print_content = False
latencies = {'nop': 1, 'add': 1, 'sub': 1, 'mult': 3, 'div': 3, 'load': 5, 'loadI': 1, 'store': 5, 'output': 1, "lshift": 1, "rshift": 1}

class Instruction(object):
	"""represent an instruction"""
	def __init__(self, opcode, src = [], dest = None):
		self.opcode = opcode
		self.src = src
		self.dest = dest
		self.oprands = list(src)
		if dest:
			self.oprands.append(dest)
		self.dep_set  = None
		self.serial_set  = None
		self.successors = set()
		self.latency = latencies[opcode]
		self.priority = 0
		self.schedule = 0

	def __repr__(self):
		if self.opcode == "nop":
			return self.opcode
		if self.opcode == "output":
			return "%s %s" % (self.opcode, repr(self.dest))
		# print self.oprands
		return "%s %s => %s" %(self.opcode, ",".join(map(repr, self.src)),repr(self.dest))

	def set_dep_set(self, dep_set):
		self.dep_set = dep_set

	def is_load(self):
		if self.opcode == "load":
			return True
		return False

	def is_output(self):
		if self.opcode == "output":
			return True
		return False

	def is_store(self):
		if self.opcode == "store":
			return True
		return False

	def is_true_dep(self, instrct):
		for oprand in self.oprands:
			for another_oprand in instrct.oprands:
					if oprand.is_known() and another_oprand.is_known():
							if oprand.content == another_oprand.content:
								return True

	@staticmethod
	def get_latency(instruction):
		return instruction.latency

	@staticmethod
	def get_schedule(instruction):
		return instruction.schedule

class Register(object):
	"""docstring for Register"""
	def __init__(self, arg):
		
		self.arg = arg
		
class Oprend(object):
	"""docstring for Oprend"""
	def __init__(self, val):
		self.val = val
	def __repr__(self):
		raise NotImplementedError
	def set_val(self, val):
		self.val = val
	def is_register(self):
		return False
	def is_immediate(self):
		return False
	def is_address(self):
		return False
	def is_known(self):
		return False

class Register(Oprend):
	"""docstring for register"""
	def __init__(self, val):
		super(Register, self).__init__(val)
		self.content = None
	if is_print_content:
			def __repr__(self):
					return "r%s(%s)" % (self.val, self.content)
	else:
			def __repr__(self):
					return "r%s" % self.val
	def is_register(self):
			return True
	def is_known(self):
			return True if self.content else False
	def set_content(self, content):
			self.content = content
		
class Immediate(Oprend):
	"""docstring for Immediate"""
	def __init__(self, val):
		super(Immediate, self).__init__(val)
	def __repr__(self):
		return repr(self.val)
	def is_immediate(self):
		return True

class Address(Oprend):
	"""docstring for ClassName"""
	def __init__(self, val):
		super(Address, self).__init__(val)
		self.content = val
	def __repr__(self):
		return repr(self.val)
	def is_known(self):
		return True
	def is_address(self):
		return True

		
		