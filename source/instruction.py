"""

"""
import copy
class Instruction(object):
	"""represent an instruction"""
	def __init__(self, opcode, src = [], dest = None):
		self.opcode = opcode
		self.src = src
		self.dest = dest
		self.latency = 0
	def __repr__(self):
		if self.opcode == "nop":
			return self.opcode
		if self.opcode == "output":
			return "%s %s" % (self.opcode, repr(self.dest))
		return "%s %s => %s" %(self.opcode, ",".join(map(repr, self.src)),repr(self.dest))

class Oprend(object):
	"""docstring for Oprend"""
	def __init__(self):
		pass
	def __repr__(self):
		raise NotImplementedError
	def is_register(self):
		return False
	def is_immediate(self):
		return False
	def is_address(self):
		return False

class Register(Oprend):
	"""docstring for register"""
	def __init__(self, val):
		self.val = val
	def __repr__(self):
		return "r%s" % self.val
	def is_register(self):
		return True
		
class Immediate(Oprend):
	"""docstring for Immediate"""
	def __init__(self, val):
		self.val = val
	def __repr__(self):
		return repr(self.val)
	def is_immediate(self):
		return True
class Address(Oprend):
	"""docstring for ClassName"""
	def __init__(self, val):
		self.val = val
	def __repr__(self):
		return repr(self.val)
	def is_address(self):
		return True

		
		