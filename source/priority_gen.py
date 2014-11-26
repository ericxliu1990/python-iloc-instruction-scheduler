from instruction import Instruction
import sys

sys.setrecursionlimit(7000)
is_gen_graphviz = False

class PriorityGen(object):
	"""docstring for PriorityGen"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list

	def compute(self):
		for instrct in reversed(self.instrct_list):
			if instrct.priority == 0:
				self.latency_weighted_distance(instrct)
			# print instrct.priority, instrct

	def highest_latency(self, instrct, seq = 0, choices_set = None):
		priority = seq + 1
		instrct.priority = priority
		deps = instrct.dep_set
		if choices_set:
			deps = deps.union(choices_set)
		if not deps:
			return
		if is_gen_graphviz:
			next_instrct = max(deps, key = lambda x: Instruction.get_latency(x[0]))
		else:
			next_instrct = max(deps, key = Instruction.get_latency)
		deps.remove(next_instrct)
		self.highest_latency(next_instrct[0], priority, deps)

	def latency_weighted_distance(self, instrct, weight = 0):
		priority = instrct.latency + weight
		instrct.priority = priority
		for dep_instrct in instrct.dep_set:
			if is_gen_graphviz:
				if dep_instrct[0].priority == 0:
					self.latency_weighted_distance(dep_instrct[0], priority)
			else:
				if dep_instrct.priority == 0:
					self.latency_weighted_distance(dep_instrct, priority)