from Node_t import Node_t
class Graph_t:
	"""docstring for Graph_t"""
	FIELD_1 = 0
	FIELD_2 = 1
	FIELD_3 = 2
	#CRITICAL = ["store", "storeAI", "storeAO", "outputAI"]
	CRITICAL = ["outputAI"]
	def __init__(self, raw_instructions):
		self.raw_instructions = raw_instructions
		self.head = None
		self.tail = None
		self.worklist = []
		self.result = []
		
	def serialize(self):
		id_num = 1
		for line in self.raw_instructions:
			new_node = Node_t(line, id_num)
			id_num+=1
			if(self.head is None):
				self.head = new_node
				self.tail = new_node
				continue

			node = self.tail
			new_node.prev = self.tail
			self.tail.next = new_node
			self.tail = self.tail.next
	
	def get_worklist(self):
		node = self.head
		while(node is not None):
			if(node.opcode in self.CRITICAL):
				node.mark = True
				self.worklist.append(node)
			node = node.next

	def Mark(self):
		while(self.worklist):
			node = self.worklist[0]
			self.worklist.pop(0)
			#print(f"popped {node.inst_id}: {node.inst_string}")
			parameters = self.defined(node)
			for param in parameters:
				if(not param.mark):
					param.mark = True
					self.worklist.append(param)
					#print(f"\tadded {param.inst_id}: {param.inst_string} to worklist")

	def sweep(self):
		while(self.head is not None):
			if(self.head.mark):
				self.result.append(self.head.inst_string)

			if(self.tail == self.head):
				self.tail = self.tail.next
			self.head = self.head.next

		if(self.result is None):
			print("you fucked it")

		return self.result


### helper functions

	def defined(self, node):
		closed = []
		read = node.get_readable()

		if(read is None):
			#print('none')
			return closed
		#print( read )
		for readable in read:
			ptr = node.prev
			#print('yes')
			while(ptr is not None):
				writable = ptr.get_writable()
				#print(f"writable: {writable}")
				if(writable is not None and writable == readable):
					closed.append(ptr)
					break
				ptr = ptr.prev
		#print(f"closed: {closed}")
		return closed

	def print_instructions(self):
		for line in self.result:
			print(line)

### debugging

	def print_marked(self):
		ptr = self.head
		closed = []
		while(ptr is not None):
			if(ptr.mark):
				closed.append(str(ptr.inst_id))
			ptr = ptr.next
		print("\t".join(closed))

	def print_graph(self):
		closed = []
		node = self.head
		while(node is not None):
			closed.append(node.opcode)
			node = node.next

		closed.append("???")
		print(" <---> ".join(closed))

	def print_worklist(self):
		closed = []
		for node in self.worklist:
			closed.append(str(node.inst_id))
		closed.append("end")
		print("\t".join(closed))

