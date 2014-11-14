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

	def find_mem_dep(self, instrct_chk):
		pass

	def build_dep_graph(self):
		reg_dep_gen = RegDepGen(self.instrct_list)
		reg_dep_gen.find_reg_dep()

	def get_instrct_list(self):
		return "\n".join(map(str,self.instrct_list))

class RegDepGen(object):
	"""docstring for InstrctDepGen"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list
		self.reg_dep = {}

	def update(self, oprand, instrct):
		if oprand and oprand.is_register():
			if not oprand.val in self.reg_dep:
				self.reg_dep[oprand.val] = []
			self.reg_dep[oprand.val].append(instrct)

	def build_dep_set(self, instrct):
		def dep_list_extend(oprand):
			if oprand and oprand.is_register():
				if self.reg_dep.get(oprand.val):
					dep_list.extend(self.reg_dep[oprand.val])
		dep_list = []
		map(dep_list_extend, instrct.oprands)
		return dep_list

	def find_reg_dep(self):
		for instrct in self.instrct_list:
			instrct.set_dep_set(self.build_dep_set(instrct))
			map(lambda x: self.update(x, instrct), instrct.oprands)
			print instrct, instrct.dep_set

class InstrctRenameGen(object):
	"""docstring for InstrctRename"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list
		self.rename_map = {}
		self.next_reg = 0

	def update(self, oprand):
		if oprand and oprand.is_register():
			if not oprand.val in self.rename_map:
				self.rename_map[oprand.val] = self.next_reg
				self.next_reg += 1
			oprand.set_val(self.rename_map[oprand.val])

	def rename(self):
		for instrct in reversed(self.instrct_list):
			origin_dest_val = instrct.dest.val
			self.update(instrct.dest)
			if instrct.dest and instrct.dest.is_register():
				if not instrct.opcode == "store":
					del self.rename_map[origin_dest_val]
			map(self.update, instrct.src)


		