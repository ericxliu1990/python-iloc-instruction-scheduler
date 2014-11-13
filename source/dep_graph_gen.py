NO_NEXT_USE = -1
from instruction import Instruction
import operator
class DepGraphGen(object):
	"""docstring for DepGraphGen"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list

	def rename(self):
		instrct_rename_gen = InstrctRenameGen(self.instrct_list)
		instrct_rename_gen.rename()

	def find_reg_dep(self, instrct_chk):
		""""""
		def depend(instrct_chk, instrct):
			""""""
			def build_reg_chk_list(instrct):
				reg_chk_list = filter(operator.methodcaller("is_register"), instrct.src)
				if instrct.dest.is_register():
					reg_chk_list.append(instrct.dest)
				return reg_chk_list

			if instrct_chk == instrct:
				return False
			for oprand_1 in build_reg_chk_list(instrct_chk):
				for oprand_2 in build_reg_chk_list(instrct):
					if oprand_1.val == oprand_2.val:
						return True
			return False

		return filter(lambda x: depend(instrct_chk, x), self.instrct_list)

	def build_dep_graph(self):
		for instrct in self.instrct_list:
			instrct.set_dep_set(self.find_reg_dep(instrct))

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
			origin_dest_val = instrct.dest.val
			self.update(instrct.dest, idx)
			if instrct.dest and instrct.dest.is_register():
				if not instrct.opcode == "store":
					del self.rename_map[origin_dest_val]
					del self.last_used[origin_dest_val]
			map(lambda x: self.update(x, idx), instrct.src)


		