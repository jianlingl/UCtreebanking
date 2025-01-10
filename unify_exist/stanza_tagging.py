

def stanza_tagging(nlp, words):
    
    sent_line = ' '.join(words)
    doc = nlp(sent_line)  # 对stanza来说分词或者不分词都可
    
    word_tag_ = [[word.text, word.upos] for sent in doc.sentences for word in sent.words]
    
    def split_word_with_blank(word_with_blank):
        words = word_with_blank.split(' ')
        new_splited_word_tag = []
        for w in words:
            doc = nlp(w)  # 对stanza来说分词或者不分词都可
            for sent in doc.sentences:
                for word in sent.words:
                    new_splited_word_tag.append([word.text, word.upos])
        
        return new_splited_word_tag
        
    def deal_with_space(word_tag):
        str_4check_space = ''
        for w, _ in word_tag:
            str_4check_space += ('#####' + w)
        while ' ' in str_4check_space:
            for id, (word, tag) in enumerate(word_tag):
                if ' ' in word:
                    new_splited_word_tag = split_word_with_blank(word)
                    id_4_replace = word_tag.index([word, tag])
                    if id_4_replace >= id:
                        if id_4_replace == 0:
                            word_tag = new_splited_word_tag + word_tag[1:]
                        elif id_4_replace > 0 and id_4_replace < len(word_tag) - 1:
                            word_tag = word_tag[: id_4_replace] + new_splited_word_tag + word_tag[id_4_replace + 1:]
                        elif id_4_replace == len(word_tag) - 1:
                            word_tag = word_tag[:-1] + new_splited_word_tag
                        break
                    else:
                        print(new_splited_word_tag)
                        assert False
            
            str_4check_space = ''
            for w, _ in word_tag:
                str_4check_space += ('#####' + w)
        return word_tag
        
    word_tag = deal_with_space(word_tag_)
    
    words_4stanza = sent_line.split(' ')
    if len(words_4stanza) == 0:
        print('no word for stanza')
    if len(words_4stanza) != len(word_tag):
        
        for idx, word in enumerate(words_4stanza):
            
            if word == word_tag[idx][0]:
                continue

            else:
                word_list, tag_list = [], []
                for i in range(0, len(word_tag) - idx):
                    word_list.append(word_tag[idx + i][0])
                    tag_list.append(word_tag[idx + i][1])
                    
                    # token能对上
                    if word.startswith(''.join(word_list)):
                        if word == ''.join(word_list):
                            # 合并删除操作
                            new_tag = tag_list[0]
                            for t in tag_list:
                                if t is not 'PUNCT':
                                    new_tag = t
                            
                            word_tag = word_tag[0:idx] + [[word, new_tag]] + word_tag[idx + i + 1:]
                            break
                    
                    # token对不上
                    # repalce目标token或直接替换原token
                    else:
                        word_list = unify_punt(word_list)
                        if word.startswith(''.join(word_list)):
                            if word == ''.join(word_list):
                                new_tag = tag_list[0]
                                for t in tag_list:
                                    if t is not 'PUNCT':
                                        new_tag = t
                                        break
                                
                                word_tag = word_tag[0:idx] + [[word, new_tag]] + word_tag[idx + i + 1:]
                                break
                        else:
                            word = unify_punt([word])[0]
                            if word.startswith(''.join(word_list)):
                                if word == ''.join(word_list):
                                    new_tag = tag_list[0]
                                    for t in tag_list:
                                        if t is not 'PUNCT':
                                            new_tag = t
                                            break
                                    
                                    word_tag = word_tag[0:idx] + [[word, new_tag]] + word_tag[idx + i + 1:]
                                    break
                            else:
                                if idx + 1 < len(words_4stanza):
                                    next_word = words_4stanza[idx + 1]
                                    for x, (w_, t_) in enumerate(word_tag[idx + 2:]):
                                        if next_word.startswith(w_):
                                            new_tag = word_tag[idx][1]
                                            word_tag = word_tag[0:idx] + [[word, new_tag]] + word_tag[idx + x + 2:]
                                            break
                                        elif next_word.startswith(w_.replace('_', '')):
                                            new_tag = word_tag[idx][1]
                                            word_tag = word_tag[0:idx] + [[word, new_tag]] + word_tag[idx + x + 2:]
                                            break
                                else:
                                    new_tag = word_tag[idx][1]
                                    word_tag = word_tag[0:idx] + [[word, new_tag]]
                                
                                break
    
    assert len(words_4stanza) == len(word_tag)

    word_tag = [tuple(lst) for lst in word_tag]
    tags = [tag for _, tag in word_tag]
    assert len(tags) == len(words_4stanza)
    return tags


def unify_punt(token_list):
    punt_dict = {
        '“': '"',
        '”': '"',
        '``': '"',
        "''": '"',
        
        '—': '--',
        
        '‘': "'",
        '’': "'",
        "`": "'",
    }
    # 对于 '\'\'s,' 这一类还需要replace操作
    replaced_token_list = []
    for tok in token_list:
        try:
            replaced_token_list.append(punt_dict[tok])
        except:
            replaced_token_list.append(tok
                                       .replace('“', '"')
                                       .replace('”', '"')
                                       .replace('``', '"')
                                       .replace("''", '"')
                                       .replace('—', '--')
                                       .replace('‘', "'")
                                       .replace('’', "'")
                                       .replace("`", "'"))
    return replaced_token_list



