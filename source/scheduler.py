from instruction import Instruction
from collections import namedtuple
FunctionalUnit = namedtuple("FunctionalUnit", ["constrain", "schedule"])

class Scheduler(object):
	"""docstring for Scheduler"""
	def __init__(self, instrct_list):
		self.instrct_list = instrct_list
		self.cycle = 1
		self.ready_set = set([instrct for instrct in instrct_list if len(instrct.dep_set) == 0])
		self.active_set = set([])
		self.func_unit_list = [
		FunctionalUnit(constrain = ["load", "store", "loadI", "add", "sub", "lshift", "rshift", "output"], schedule = []), 
		FunctionalUnit(constrain = ["mult","div", "loadI", "add", "sub", "lshift", "rshift", "output"], schedule = [])]


	def schedule(self):
		while len(self.ready_set.union(self.active_set)) != 0:
			for func_unit in self.func_unit_list:
				if len(self.ready_set) > 0:
					instrct = self.choose_ready(func_unit.constrain)
					func_unit.schedule.append(instrct)
					if instrct:
						instrct.schedule = self.cycle
						self.ready_set.remove(instrct)
						self.active_set.add(instrct)
				else:
					func_unit.schedule.append(None)

			self.cycle += 1

			for instrct in self.active_set.copy():
				if instrct.schedule + instrct.latency <= self.cycle:
					self.active_set.remove(instrct)
					self.add_to_successors(instrct)
	
	def choose_ready(self, constrain):
		max_priority = 0
		instrct = None
		for ready_instrct in self.ready_set:
			if ready_instrct.schedule == 0:
				if ready_instrct.priority > max_priority:
					max_priority = ready_instrct.priority
					instrct = ready_instrct
		if instrct.opcode in constrain:
			return instrct
		else:
			return None
	
	def add_to_successors(self, instrct):
		for dep_instrct in instrct.successors:
			if self.is_ready(dep_instrct):
				self.ready_set.add(dep_instrct)

	def is_ready(self, instrct):
		if instrct.schedule != 0:
			return False
		for dep_instrct in instrct.dep_set:
			if dep_instrct.schedule <= 0:
				return False
		return True

	def get_schedule(self):
		return zip(self.func_unit_list[0].schedule, self.func_unit_list[1].schedule)
	
	def get_schedule_str(self):
		def get_instrct_str(instrct):
			return "nop" if instrct == None else str(instrct)
		
		def get_instrct_pair_str(instrct_pair):
			return "[%s] " % "; ".join(map(get_instrct_str, instrct_pair))

		return "\n".join(map(get_instrct_pair_str, self.get_schedule()))


		