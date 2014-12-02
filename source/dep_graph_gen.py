from instruction import Instruction

is_gen_graphviz = False
NO_NEXT_USE = -1

class DepGraphGen(object):
	"""docstring for DepGraphGen"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list

	def rename(self):
		instrct_rename_gen = InstrctRenameGen(self.instrct_list)
		instrct_rename_gen.rename()

	def build_dep_graph(self):
		compute_loadi_gen = ComputeLoadIGen(self.instrct_list)
		compute_loadi_gen.compute()
		instrct_dep_gen = InstrctDepGen(self.instrct_list)
		instrct_dep_gen.find_reg_dep()

	def get_instrct_list(self):
		return "\n".join(map(str,self.instrct_list))

class InstrctDepGen(object):
	"""docstring for InstrctDepGen"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list
		self.reg_dep = {}
		self.load_list = []
		self.output_list = []
		self.store_list = []

	def reg_update(self, instrct):
		if not instrct.opcode == "store":
			oprand = instrct.dest
			if oprand and oprand.is_register():
				if oprand.val in self.reg_dep:
					raise ValueError
				if is_gen_graphviz:
					self.reg_dep[oprand.val] = (instrct, oprand, instrct.latency)
				else:
					self.reg_dep[oprand.val] = instrct

	def mem_update(self, instrct):
		if is_gen_graphviz:
			if instrct.is_load():
				self.load_list.append((instrct, "IO Edge", instrct.latency))
			if instrct.is_output():
				self.output_list.append((instrct, "IO Edge", instrct.latency))
			if instrct.is_store():
				self.store_list.append((instrct, "IO Edge", instrct.latency))
		else:
			if instrct.is_load():
				self.load_list.append(instrct)
			if instrct.is_output():
				self.output_list.append(instrct)
			if instrct.is_store():
				self.store_list.append(instrct)

	def add_to_successors(self, instrct, dep_instrct):
		if is_gen_graphviz:
			dep_instrct[0].successors.add(instrct)
		else:
			dep_instrct.successors.add(instrct)

	def find_reg_dep(self):
		for instrct in self.instrct_list:
			dep_list_gen = DepListGen(instrct, self.reg_dep, self.load_list, self.output_list, self.store_list)
			dep_list = dep_list_gen.build_dep_list()
			# print self.instrct_list.index(instrct), instrct
			# # print self.reg_dep
			# print dep_list
			# print "---------------"
			if is_gen_graphviz:
				if not len(set(dep_list)) == len(dep_list):
					print dep_list
					raise Exception
			instrct.set_dep_set(dep_list)

			#update to the working sets
			self.reg_update(instrct)
			self.mem_update(instrct)

			#add this instrction to the successor set of all dependencies
			map(lambda x: self.add_to_successors(instrct, x), dep_list)

class DepListGen(object):
	"""docstring for ClassName"""
	def __init__(self, instrct, reg_dep, load_list, output_list, store_list):
		self.instrct = instrct
		self.reg_dep = reg_dep
		self.load_list = load_list
		self.output_list = output_list
		self.store_list = store_list
		self.dep_list = []

	def append_last(self, a_list):
		if len(a_list) > 0:
			self.dep_list.append(a_list[-1])

	def append(self, instrct):
		def is_instrct_in_dep_list(instrct):
			for (another_instrct, label, latency) in self.dep_list: 
				if instrct[0] == another_instrct:
					return True
			return False
		if is_gen_graphviz:
			if not is_instrct_in_dep_list(instrct):
				self.dep_list.append(instrct)
		else:
			if not instrct in self.dep_list:
				self.dep_list.append(instrct)

	def extend(self, a_list):
		map(self.append, a_list)

	def append_reg_dep(self, oprand):
		if oprand and oprand.is_register():
			if self.reg_dep.get(oprand.val):
				self.append(self.reg_dep[oprand.val])

	def build_dep_list(self):
		map(self.append_reg_dep, self.instrct.oprands)
		if self.instrct.is_load():
			self.extend(self.store_list)
		if self.instrct.is_output():
			self.extend(self.store_list)
			self.append_last(self.output_list)
		if self.instrct.is_store():
			self.extend(self.store_list)
			self.extend(self.load_list)
			self.extend(self.output_list)

		return self.dep_list

class ComputeLoadIGen(object):
        """docstring for ComputeLoadI"""
        def __init__(self, instrct_list):
                self.instrct_list = instrct_list
                self.working_set = {}

        def operation(self, func, src_0, src_1, dest):
                if src_0.val in self.working_set and src_1.val in self.working_set:
                        self.working_set[dest.val] = func(self.working_set[src_0.val], self.working_set[src_1.val])

        def update_working_set(self, instrct):
                if instrct.opcode == "loadI":
                        self.working_set[instrct.dest.val] = instrct.src[0].val
                if instrct.opcode == "load":
                        if instrct.dest.val in self.working_set:
                                del self.working_set[instrct.dest.val]
                if instrct.opcode == "add":
                        self.operation(lambda x,y: x + y, instrct.src[0], instrct.src[1], instrct.dest)
                if instrct.opcode == "sub":
                        self.operation(lambda x,y: x - y, instrct.src[0], instrct.src[1], instrct.dest)
                if instrct.opcode == "mult":
                        self.operation(lambda x,y: x * y, instrct.src[0], instrct.src[1], instrct.dest)
                if instrct.opcode == "div":
                        self.operation(lambda x,y: x / y, instrct.src[0], instrct.src[1], instrct.dest)

        def update_register(self, instrct):
                for oprand in instrct.oprands:
                        if oprand.is_register() and oprand.val in self.working_set:
                                oprand.set_content(self.working_set[oprand.val])

        def compute(self):
                for instrct in self.instrct_list:
                        self.update_working_set(instrct)
                        self.update_register(instrct)

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
