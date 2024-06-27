# -*- coding: utf-8 -*-
import fitz
import copy
import re
from pykospacing import Spacing

def splittext(page, pdf_name):
    doc = fitz.open(pdf_name)
    text = page.get_text()
    spacing = Spacing()
    text = spacing(text)
    text = text.replace('\n ', ' <enter> ')
    text = text.replace('\n', '')
    # text = re.sub(r'[^가-힣a-zA-Z\s]', '', text)
    text2 = text.split(' <enter> ')
    text2 = [item for item in text2 if len(item)>1]

    return text2

def save_weight(txtname, doc):
    f = open("{}".format(txtname), encoding = 'utf-8')
    lines = f.readlines()
    weight = []
    for i in range(len(doc)):
        weight.append([])
    for i in range(len(doc)):
        for j in range(len(lines)):
            if lines[j] == 'Page {}\n'.format(i):
                check = True
                num = j+3
                while num < len(lines) and check:
                    if lines[num] != 'Page {}\n'.format(i+1):
                        weight[i].append(lines[num])
                        num += 1
                    else:
                        check = False
                break
    f.close()
    return weight

def delete_n(weight_list):
    for i in range(len(weight_list)):
        weight_list[i] = [item for item in weight_list[i] if len(item) > 3]
    for i in range(len(weight_list)):
        for j in range(len(weight_list[i])):
            if weight_list[i][j][-2:] == '.\n':
                weight_list[i][j] = weight_list[i][j][:-2]
            else:
                weight_list[i][j] = weight_list[i][j][:-1]
    return weight_list


def onewordsplit(weight_list):
    split_weight = []
    for i in range(len(weight_list)):
        weight_sentences = list(weight_list[i]).copy()
        weight_sentences = [items for items in weight_sentences if items != ' ']
        split_weight.append(weight_sentences)
    return split_weight

def add_sentence(weight, paragraph, lst):
    index_result = []
    pnum = -1
    add = -1
    for i in range(len(weight)): #page 0: 4번 반복
        index = -1
        weight_list2 = weight.copy()
        weight_list = onewordsplit(weight_list2)[i]
        for j in range(len(paragraph)):
            temp_p = paragraph.copy()
            oneSinP = list(temp_p[j].split('.')).copy()
            for k in range(len(oneSinP)):
                SPK2 = oneSinP[k]
                SPK = [item for item in SPK2 if item != ' ']
                for l in range(len(SPK)):
                    if (SPK[l] == weight_list[0]) and (len(SPK) >= l+len(weight_list)):
                        if(SPK[l+len(weight_list)-1] == weight_list[-1]):
                            index = k
                            add += 1
                            pnum = j

                            break
                    else:
                        continue

        if index != -1:
            index_result.append((pnum, index, index+add))
    lst.append(index_result)


def dotandcombine(oneSinP_result):
    """
    add_sentnece에서 나온 oneSinP_result(가중치있는 문장 추가해준 리스트)를
    다시 문장 끝에 점 붙이고 한 str로 합쳐주는 함수
    """
    oneSinP_result2 = oneSinP_result.copy()
    for i in range(len(oneSinP_result2)):
        oneSinP_result2[i] += '.'
    modified_text = ''
    for i in oneSinP_result2:
        modified_text += i

    return modified_text

def paragraph_to_list(paragraph):
    result_list = []
    for i in range(len(paragraph)):
        a = list(paragraph[i].split('.'))
        a = [item for item in a if len(item) > 1]
        result_list.append(a)

    return result_list

def insert_sentence(doc, pagenum, lst, pdf_name):
    page = doc[pagenum]
    paragraph = splittext(page, pdf_name)
    ptl = paragraph_to_list(paragraph)
    count_p = []
    temp_paragraph = copy.deepcopy(ptl)
    for num in range(len(lst[pagenum])):
        tl = lst[pagenum][num]
        temp_paragraph[tl[0]].insert(tl[1]+count_p.count(tl[0])+1, ptl[tl[0]][tl[1]])
        count_p.append(tl[0])
    return temp_paragraph

"""
추가된 부분
확인되면 이 주석은 지울것
"""
def add_style(summarized_list, weight_list, pagenum):
    split_sl = summarized_list[pagenum].split(' ')
    result_hl = copy.deepcopy(split_sl)
    for k in range(len(weight_list[pagenum])):
        score = 0
        split_wl = weight_list[pagenum][k].split(' ')
        index = -1
        for s in range(len(split_sl)):
            if split_wl[0] == split_sl[s]:
                for w in range(len(split_wl)):
                    if s+w < len(split_sl):
                        if split_wl[w] == split_sl[s+w]:
                            score += 1
                            index = s
                score = score / len(split_wl)
                break
        if score > 0.7 and index != -1:
            result_hl.insert(index, '<mark>')
            result_hl.insert(index + len(split_wl) + 1, '</mark>')
        split_sl = result_hl.copy()

    return result_hl

def combine_hl(styled_list):
    textwithhl = ''
    for l in styled_list:
        textwithhl += l + ' '
    return textwithhl
