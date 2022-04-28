from Node_t import Node_t
class Graph_t:
	"""docstring for Graph_t"""
	FIELD_1 = 0
	FIELD_2 = 1
	FIELD_3 = 2
	def __init__(self, raw_instructions):
		self.raw_instructions = raw_instructions
		self.node_list = []
		self.tracker = {}
		self.last_output = -1
		
	def serialize(self):
		id_num = 1
		for line in self.raw_instructions:	
			newNode = Node_t(line, id_num)
			id_num+=1
			# self.node_list.append(newNode)
			if(newNode.opcode == "loadI"):
				self.node_list.append(newNode)
				self.tracker.update({newNode.getWritable() : len(self.node_list)-1})
				continue

			read_registers = newNode.getReadable()
			if(newNode.opcode == "outputAI"):
				self.output_append(newNode, read_registers)
			else:
				self.normal_append(newNode, read_registers)



	def output_append(self, new_node, read_registers):
		read_registers.append(self.last_output)
		keys = []
		keys.append(self.tracker[read_registers[0]])
		if(self.last_output > 0 and self.last_output not in keys):
			keys.append(self.last_output)
		for key in keys:
			self.appendNode(new_node, key)
		self.last_output = keys[0]
	def normal_append(self, new_node, read_registers):
		for key in read_registers:
			if(key not in self.tracker):
				print("something went wrong while adding")
				return None
			pos = self.tracker[key]
			self.appendNode(new_node, pos)
			writable = new_node.getWritable()	
			self.tracker.update({writable : pos})	



### helper functions

	def print_graph(self):
		done = []
		for head in self.node_list:
			ptr = head
			builder = []
			while(ptr is not None):
				builder.append(f"{ptr.inst_id}")
				if(ptr.inst_id in done):
					break
				done.append(ptr.inst_id)
				ptr = ptr.next
			builder.append("//")
			print(" ==> ".join(builder))

	def appendNode(self, node, pos):
		ptr = self.node_list[pos]
		while(ptr.next is not None):
			ptr = ptr.next
		ptr.next = node