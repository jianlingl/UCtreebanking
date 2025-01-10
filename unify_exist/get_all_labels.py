from typing import Union, List
import collections.abc


class Tree(object):
	"""Tree data structure.
	Attributes:
		label:
		word:
		is_leaf:
		left and right: span idx in sentence, left included, right excluded. -> [left, right)
	"""
	
	def __init__(self, label: str, children_or_word: Union[List['Tree'], str], span_start_idx: int, span_end_idx: int):
		super(Tree, self).__init__()
		
		self.label: str = label
		self.word = None
		self.children = None
		self.is_leaf = isinstance(children_or_word, str)
		
		if self.is_leaf:
			self.word: str = children_or_word
		else:
			assert isinstance(children_or_word, collections.abc.Sequence)
			assert all(isinstance(child, Tree) for child in children_or_word)
			self.children: List[Tree] = children_or_word
		
		self.left = span_start_idx
		self.right = span_end_idx
		assert self.left < self.right
		if not self.is_leaf:
			assert all(left.right == right.left for left, right in zip(self.children, self.children[1:]))
			assert self.left == self.children[0].left and self.right == self.children[-1].right
	
	def get_sent_words(self, sent):
		if self.is_leaf:
			sent.append(self.word)
		elif not self.is_leaf:
			for child in self.children:
				child.get_sent_words(sent)
	
	def recognize_compound_and_reconstruction(self, line_count, fr_tag_map_str, fr_label_map_str):
		if not self.is_leaf:
			if self.label.endswith('+'):
				compound = []
				for child in self.children:
					if child.is_leaf:
						if child.word is not '-':
							compound.append(child.word)
					else:
						print("deep compound here: ", line_count)
				word = '-'.join(compound)
				if ',' in word and compound[0].isdigit():
					word = word.replace('-', '')
				self.word = word
				self.children = None
				self.is_leaf = True
				self.label = self.label[:-1]
			elif self.label in fr_tag_map_str and self.label not in fr_label_map_str:
				compound = []
				for child in self.children:
					compound.append(child.word)
				self.word = ''.join(compound)
				self.children = None
				self.is_leaf = True
				self.label = self.label
			else:
				for child in self.children:
					child.recognize_compound_and_reconstruction(line_count, fr_tag_map_str, fr_label_map_str)
	
	def remove_compound_label(self, line_count, fr_tag_map_str, fr_label_map_str):
		if not self.is_leaf:
			for child in self.children:
				if child.is_leaf:
					continue
				
				elif child.label.endswith('+') or (
						child.label in fr_tag_map_str and child.label not in fr_label_map_str):
					compound_child_tree_list = []
					for grandchild in child.children:
						compound_child_tree_list.append(grandchild)
					compound_index = self.children.index(child)
					self.children = self.children[0:compound_index] + compound_child_tree_list + self.children[
																								 compound_index + 1:]
				
				else:
					child.Fr_remove_compound_label(line_count, fr_tag_map_str, fr_label_map_str)
	
	def change_label(self, span_label: str):
		if not self.is_leaf:
			assert '-' not in self.label \
				   or ('POSTAG' in self.label and self.label.count('-') == 1) \
				   or (self.label in (
				'POSTAG--LRB-', 'POSTAG--RRB-', 'POSTAG--LCB-', 'POSTAG--RCB-', 'POSTAG--LSB-', 'POSTAG--RSB-'))
			self.label = self.label + '-' + span_label
			for child in self.children:
				child.change_label(span_label)
	
	def unify_label_tag(self, zh_label_map, zh_tag_map):
		if not self.is_leaf:
			try:
				self.label = zh_label_map[self.label]
			except:
				print(self.label, 'cant find in the mapping table to universal label')
			for child in self.children:
				child.unify_label_tag(zh_label_map, zh_tag_map)
		elif self.is_leaf:
			self.label = zh_tag_map[self.label]
	
	def linearize(self):
		if self.is_leaf:
			text = self.word
		else:
			text = ' '.join([child.linearize() for child in self.children])
		return '(%s %s)' % (self.label, text)
	
	def leaves(self, wordList=[]):
		if self.is_leaf:
			wordList.append(self.word)
		else:
			for child in self.children:
				child.leaves(wordList)
		return wordList
	
	def leaves_labels(self, labelList=[]):
		if not self.is_leaf:
			if self.label in ['CONJ', 'INTJ', 'P']:
				print(self)
			labelList.append(self.label.split(';')[0])
		
			for child in self.children:
				child.leaves_labels(labelList)


def load_trees(path: str) -> List[Tree]:
	trees = []
	with open(path, 'r', encoding='utf-8') as reader:
		for line in reader:
			line = line.strip()
			
			tree = generate_tree_from_str(line)
			trees.append(tree)
	return trees


def generate_tree_from_str(text: str) -> Tree:
	assert text.count('(') == text.count(')')
	tokens = text.replace("(", " ( ").replace(")", " ) ").split()
	idx = 0
	return build_tree(tokens, idx, 0)[0]


def build_tree(tokens: List[str], idx: int, span_startpoint_idx: int):
	"""generate a tree from tokens list.
	and the tree to be generated is bracketed.
	Args:
		tokens[idx] must be '('
		span_startpoint_idx: the start point idx in the sentence of the span
	Returns:
		tree and idx to be processed.
	"""
	idx += 1
	label = tokens[idx]
	idx += 1
	assert idx < len(tokens)
	
	if tokens[idx] == '(':
		children = []
		span_endpoint_idx = span_startpoint_idx
		while idx < len(tokens) and tokens[idx] == '(':
			child, idx, span_endpoint_idx = build_tree(tokens, idx, span_endpoint_idx)
			children.append(child)
		# generate internal node
		tree = Tree(label, children, span_startpoint_idx, span_endpoint_idx)
		assert not tree.is_leaf
	elif tokens[idx] == ')':
		print('No word!!!')
		exit(-1)
	else:
		word = tokens[idx]
		idx += 1
		# generate leaf node
		span_endpoint_idx = span_startpoint_idx + 1
		tree = Tree(label, word, span_startpoint_idx, span_endpoint_idx)
		assert tree.is_leaf
	
	assert tokens[idx] == ')'
	return tree, idx + 1, span_endpoint_idx

def statis_labels(path_tain, path_dev, path_test):
	trees = load_trees(path_tain)
	labelList = []
	for idx, t in enumerate(trees):
		t.leaves_labels(labelList)
	labelset_tain = set(labelList)
	print(len(labelset_tain))
	print(sorted(labelset_tain))
	
	trees = load_trees(path_dev)
	labelList = []
	for idx, t in enumerate(trees):
		t.leaves_labels(labelList)
		
	labelset_dev = set(labelList)
	print(len(labelset_dev))
	print(sorted(labelset_dev))
	for label in labelset_dev:
		if label not in labelset_tain:
			print(label, ' not in train corpus!!!')
	
	trees = load_trees(path_test)
	labelList = []
	for idx, t in enumerate(trees):
		t.leaves_labels(labelList)
		
	labelset_test = set(labelList)
	print(len(labelset_test))
	print(sorted(labelset_test))
	for label in labelset_test:
		if label not in labelset_tain:
			print(label, ' not in train corpus!!!')
if __name__ == '__main__':
	path_tain, path_dev, path_test = 'unify_exist/origin/french/French.train', 'unify_exist/origin/french/French.dev', 'unify_exist/origin/french/French.test'
	statis_labels(path_tain, path_dev, path_test)
	print('==============' * 10)


