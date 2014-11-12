NO_NEXT_USE = -1
from instruction import Instruction

class DepGraphGen(object):
	"""docstring for DepGraphGen"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list

	def rename(self):
		instrct_rename_gen = InstrctRenameGen(self.instrct_list)
		instrct_rename_gen.rename()

	def get_instrct_list(self):
		return "\n".join(map(str,self.instrct_list))

class InstrctRenameGen(object):
	"""docstring for InstrctRename"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list
		self.rename_map = {}
		self.next_reg = 0
		self.last_used = {}
	def update(self, oprand, idx):
		if oprand and oprand.is_register():
			if not oprand.val in self.rename_map:
				self.rename_map[oprand.val] = self.next_reg
				self.next_reg += 1
				self.last_used[oprand.val] = NO_NEXT_USE
			self.last_used[oprand.val] = idx
			oprand.val = self.rename_map[oprand.val]

	def rename(self):
		for idx, instrct in reversed(list(enumerate(self.instrct_list))):
			origin_instrct = Instruction.deepcopy(instrct)
			self.update(instrct.dest, idx)
			if instrct.dest and instrct.dest.is_register():
				if not instrct.opcode == "store":
					del self.rename_map[origin_instrct.dest.val]
					del self.last_used[origin_instrct.dest.val]
			map(lambda x: self.update(x, idx), instrct.src)
			# print self.rename_map
			# print self.last_used

		