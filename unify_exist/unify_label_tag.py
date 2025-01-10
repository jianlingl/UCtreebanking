from typing import Union, List
import stanza, os
from LabelMapTable import get_label_mappings
from stanza_tagging import stanza_tagging


is_singleton, sibling, only_nephew, multi_nephew, far_than_nephew = 0, 0, 0, 0, 0

class Tree(object):
    def __init__(self, label: str, children: Union[list, str], left: int, right: int):
        super(Tree, self).__init__()
        self.label: str = label
        self.is_leaf = isinstance(children, str)
        self.word = None
        self.children = None
        if self.is_leaf: self.word = children
        else: self.children = children

        self.left = left
        self.right = right
        assert self.left < self.right
    
    def cnt_phrase(self):
        if not self.is_leaf:
            if self.label not in ['TOP', 'ROOT', 'root']:
                yield self.label
            
            for child in self.children:
                yield from child.cnt_phrase()

    def unify_label_tag(self, label_map: dict, tags=None):
        if not self.is_leaf:
            assert self.label in label_map.keys(), 'cant find in the mapping table to universal label'
            self.label = label_map[self.label]

            for child in self.children:
                child.unify_label_tag(label_map, tags)
        
        elif self.is_leaf and tags is not None:
            assert len(tags) > 0, "no tags left, the num of tags and words do not align"
            self.label = tags[0] # 根据下标取树节点相应的tag
            del(tags[0]) # remove只删除第一个

    # He将二级tag直接舍弃
    def He_rm_secnd_tag(self):
        if not self.is_leaf:

            tmp_kids = []
            for child in self.children:
                if not child.is_leaf and child.label.startswith('SYN_'): tmp_kids.extend(child.children)
                else: tmp_kids.append(child)
            self.children = tmp_kids

            for child in self.children:
                child.He_rm_secnd_tag()
    
    # Hu舍弃将tag作为短语标签同he
    def Hu_rm_tag_label(self, hu_tags=['A', 'C', 'I', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z']):
        if not self.is_leaf:

            tmp_kids = []
            for child in self.children:
                if not child.is_leaf and child.label in hu_tags: tmp_kids.extend(child.children)
                else: tmp_kids.append(child)
            self.children = tmp_kids

            for child in self.children:
                child.Hu_rm_tag_label()
    
    # Ja舍弃分号后细分标签，舍弃将tag作为短语标签
    def Ja_rm_semicolon_and_tag_label(self, ja_tags=['ADJI', 'ADJN', 'ADV', 'AX', 'AXD', 'CL', 'CONJ', 'D', 'FN', 'FW', 'INTJ', 'MD', 'N', 'NEG', 'NPR', 'NUM', 'P', 'PASS', 'PASS2', 'PNL', 'PRO', 'PU', 'PUL', 'PUR', 'Q', 'SYM', 'VB', 'VB0', 'VB2', 'WADV', 'WD', 'WNUM', 'WPRO']):
        if not self.is_leaf:
            # 舍弃分号后细分标签
            self.label = self.label.split(';')[0]
            # 舍弃tag作为短语标签
            tmp_kids = []
            for child in self.children:
                if not child.is_leaf and child.label in ja_tags: tmp_kids.extend(child.children)
                else: tmp_kids.append(child)
            self.children = tmp_kids

            for child in self.children:
                child.Ja_rm_semicolon_and_tag_label()
        else:
            self.label = self.label.split(';')[0]
 
    def cut_vertic_dups(self):
        if not self.is_leaf:
            if len(self.children) == 1 and not self.children[0].is_leaf:
                if self.label == self.children[0].label:
                    self.children = self.children[0].children
                    
                    if len(self.children) == 1 and self.label == self.children[0].label:
                        self.children = self.children[0].children

            for child in self.children:
                child.cut_vertic_dups()

    def simplify_multi_labels(self):
        if not self.is_leaf:
            multi_labels = [self.label]
            t: Tree = self
            while len(t.children) == 1:
                if t.children[0].is_leaf: break

                if t.children[0].label in multi_labels: 
                    t.children = t.children[0].children
                    t = t
                else:
                    multi_labels.append(t.children[0].label)
                    t: Tree = t.children[0]
                if t.is_leaf: break
            
            for child in self.children:
                child.simplify_multi_labels()
  
    def linearize(self):
        if self.is_leaf:
            text = self.word
        else:
            text = ' '.join([child.linearize() for child in self.children])
        return '(%s %s)' % (self.label, text)

    def leaves(self):
        if self.is_leaf:
            yield self.word
        else:
            for child in self.children:
                yield from child.leaves()

    def binarize(self):
        if not self.is_leaf:
            while len(self.children) == 1 and not self.children[0].is_leaf:
                self.label += '::' + self.children[0].label
                self.children = self.children[0].children

            if len(self.children) > 2:
                left_child = self.children[0]
                right_child = Tree('*', self.children[1:], self.children[1].left, self.children[-1].right)
                self.children = [left_child, right_child]

            for child in self.children:
                child.binarize()

    def debinarize(self):
        if not self.is_leaf:
            while '::' in self.label:
                label_list = self.label.split('::')
                label_this, label_tail = '::'.join(label_list[:-1]), label_list[-1]
                self.label = label_this
                self.children = [Tree(label_tail, self.children, self.left, self.right)]

            for child in self.children:
                child.debinarize()

            child_list = []
            for child in self.children:
                if '*' in child.label:
                    child_list.extend(child.children)
                else:
                    child_list.append(child)
            self.children = child_list

    def span_labels(self):
        if self.is_leaf:
            res = []
        else:
            res = [self.label]
            for child in self.children:
                res += child.span_labels()
        return res


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
    return tree, idx+1, span_endpoint_idx


def unify_label_tag(lan, nlp, src_path, tgt_path='unify_exist/univer/'):
    label_map, _ = get_label_mappings(lan)
    
    cnt_, cnt = 0, 0
    for f in os.listdir(src_path):
        pattern = f.split('.')[-1]
        # if pattern in ['test']:
        if pattern in ['train', 'dev', 'test']:

            trees = load_trees(src_path + f)
            tmps = []
            for i, t in enumerate(trees):
                if lan == 'he': t.He_rm_secnd_tag() # 将二层tag删除掉
                if lan == 'hu': t.Hu_rm_tag_label() # 将hu中tag作为短语标签的删除
                if lan == 'ja': t.Ja_rm_semicolon_and_tag_label() # 将分号及其后续补充标签删除&将ja中tag作为短语标签的情况删除
                
                cnt_ += len(list(t.cnt_phrase()))

                if nlp: tags = stanza_tagging(nlp, list(t.leaves()))
                else: tags = None

                try:
                    t.unify_label_tag(label_map, tags)
                    t.simplify_multi_labels()
                    tree_str = t.linearize()
                    if len(tree_str.split(' ')) > 2: # 去除(TOP None)的情况
                        tmps.append(tree_str)

                    cnt += len(list(t.cnt_phrase()))

                except:
                    pass               

            with open(tgt_path + lan + '.' + pattern, 'w', encoding='utf-8') as F:
                for t in tmps: F.write(t + '\n')
            print(tgt_path + lan + '.' + pattern, ' write done!!!!!!!!!!!')

    print(cnt, cnt_, "%.5f" %(cnt/cnt_))
    print('\n')


if __name__ == "__main__":
    # unify all existing treebanks
    src_path = {'en': 'unify_exist/origin/wsj/', 'de': 'unify_exist/origin/german/', 'fr': 'unify_exist/origin/french/', 'he': 'unify_exist/origin/hebrew/', 'hu': 'unify_exist/origin/hungarian/', 'ko': 'unify_exist/origin/korean/', 'ja': 'unify_exist/origin/japanese/', 'sv': 'unify_exist/origin/swedish/', 'zh': 'unify_exist/origin/ctb/'}
    for lan in ['en', 'de', 'fr', 'he', 'hu', 'ko', 'ja', 'sv', 'zh']: # , 'en', 'de', 'fr', 'he', 'hu', 'ko', 'ja', 'sv', 'zh'
        # nlp = stanza.Pipeline(lang=lan, processors='tokenize, pos', download_method=2, tokenize_pretokenized=True)
        nlp = False
        unify_label_tag(lan, nlp, src_path[lan])
    
    # unify EWT specifically
    unify_label_tag('en', False, 'unify_exist/origin/EWT/', 'unify_exist/univer/EWT/')

