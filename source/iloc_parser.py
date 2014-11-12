"""
"""
import re
from instruction import Instruction, Register, Immediate, Address


class IlocParser():
	"""docstring for Scanner"""
	def __init__(self, file):
		self.iloc_input = file.read()
		file.close()

	def parse(self):
		""""""
		def rm_comment(text):
			return re.sub(re.compile("//.*?\n" ) ,"" ,text) 
		def read_lines(text):
			return [line for line in text.split("\n") if not line.strip() == ""]
		def torkz_instrct(text):
			def instrct_factory(line):
				def oprand_factory(opcode, oprand):
					if "r" in oprand:
						return Register(int(oprand[1 : ]))
					if opcode == "loadI":
						return Immediate(int(oprand))
					if opcode == "output":
						return Address(int(oprand))
					raise Exception

				line_list = line.replace("=>", " => ").replace(",", " ", 1).split()
				if line_list[0] == "nop":
					return Instruction(line_list[0])
				if line_list[0] == "output":
					return Instruction(line_list[0], dest = oprand_factory(line_list[0], line_list[1]))
				return Instruction(line_list[0],
								[oprand_factory(line_list[0], item) for item in line_list[1 : line_list.index("=>")]],
								oprand_factory(line_list[0], line_list[-1]))
			return [instrct_factory(line) for line in text]
		
		return torkz_instrct(read_lines(rm_comment(self.iloc_input)))

		