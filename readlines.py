# -*- coding: utf-8 -*-
import os
import copy
from pykospacing import Spacing



import fitz

def pdf_to_img(doc):
    for i, page in enumerate(doc):
        img = page.get_pixmap()
        img.save(f"pdf_image{i}.png")


def make_md(pdf_name):
    """
    pdf path를 입력받아 markdown 파일을 생성함
    """
    terminal_command = "pdfannots {} > highlights.md".format(pdf_name)
    os.system(terminal_command)


def draw_path(page):
    """
    page를 입력받아, 그 page의 drawing을 반환
    """
    paths = page.get_drawings()  # 페이지 내의 draw된 객체들을 불러 올 수 있음
    return paths


def find_color(paths):
    """
    하이라이트와 펜 필기 객체를 구분하여 리스트에 저장
    """
    fills = []
    colors = []
    for i in range(len(paths)):
        if paths[i]['fill'] != None:
            fills.append(copy.copy(paths[i]))
        elif paths[i]['color'] != None:
            colors.append(copy.copy(paths[i]))
    # 검은 색 하이라이트 제거

    for i in range(len(fills)):
        if (0.9 <= fills[i]['fill'][0] <= 1.0) and (0.9 <= fills[i]['fill'][1] <= 1.0) and (
                0.9 <= fills[i]['fill'][2] <= 1.0):
            fills[i]['fill'] = 1000

    for item in fills:
        if item['fill'] == 1000:
            fills.remove(item)
    valid_fills = []
    for fill in fills:
        if fill['fill'] is not None:
            if fill['fill'] != (0.0, 0.0, 0.0):
                valid_fills.append(fill)
    fills = valid_fills
    return fills, colors


def find_line(colors):
    """
    펜으로 그린 필기 중 line인 것과 그렇지 않은 것을
    리스트에 넣어 반환
    real_line: line인 객체들의 리스트
    etc_line: line이 아닌 객체들의 리스트
    """

    bool_line = []
    for i in range(len(colors)):
        total = 0
        num = 0
        item_len = len(colors[i]['items'])
        if colors[i]['items'][0][0] != 'qu' and colors[i]['items'][0][0] != 're':
            print(colors[i]['items'][0][0], i)
            for j in range(item_len):
                point_len = len(colors[i]['items'][j])

                for k in range(1, point_len):
                    total += colors[i]['items'][j][k][1]
                    num+=1
        elif colors[i]['items'][0][0] == 're':
            for j in range(2):
                total += (colors[i]['items'][0][1][j*2 + 1])
                num += 1
            avg = total / num
        else:
            for j in range(len(colors[i]['items'][0][1])):

                total += colors[i]['items'][0][1][j][1]
                num+=1
        avg = total /num
        bool_line.append(abs(colors[i]['items'][0][1][1] - avg))

    real_lines = []
    etc_lines = []

    for i in range(len(colors)):
        if bool_line[i]<=3:
            real_lines.append(colors[i])
        else:
            etc_lines.append(colors[i])

    return real_lines, etc_lines


def combine_line(fills):
    """
    fills를 받아서 다음 줄이랑 연결되면..어쩌고 암튼
    다른 줄이라고 분리되는거 막기 위한 함수
    다른 줄이랑 연결되는 highlight면 1, 아니면 0
    """
    fillavgY = [0] * len(fills)
    for i in range(len(fills)):
        num = 0
        if fills[i]['items'][0][0] != 're':
            for j in range(len(fills[i]['items'])):
                for k in range(1, len(fills[i]['items'][j])):
                    num += 1
                    fillavgY[i] = fillavgY[i] + fills[i]['items'][j][k][1]
            fillavgY[i] = fillavgY[i] / num
        else:
            fillavgY[i] = fillavgY[i] + fills[i]['items'][0][1][1] + fills[i]['items'][0][1][3]
            fillavgY[i] = fillavgY[i] / 2
    boolNext = [0] * len(fills)
    for i in range(len(fillavgY) - 1):
        minus = abs(fillavgY[i + 1] - fillavgY[i])
        if minus <= 5:
            boolNext[i] = 1
    return boolNext


def underlined_texts(page, real_lines):
    """
    real_lines를 받아 밑줄이 쳐져있는 텍스트를 반환
    underlined_text에는 text, text의 처음 위치, text의 마지막 위치가 있음
    """
    lines = []
    for i in range(len(real_lines)):
        p1 = real_lines[i]['items'][0][1]
        p2 = real_lines[i]['items'][-1][-1]
        lines.append((p1, p2))

    underlined_text = []
    draw_lines = lines
    blocks = page.get_text("dict",flags=fitz.TEXTFLAGS_TEXT)["blocks"]
    max_lineheight = 0
    for b in blocks:
        for l in b["lines"]:
            bbox=fitz.Rect(l["bbox"])
            if bbox.height > max_lineheight:
                max_lineheight = bbox.height
    for p1, p2 in draw_lines:
        rect = fitz.Rect(p1.x, p1.y - max_lineheight, p2.x, p2.y) 
        text = page.get_textbox(rect)
        underlined_text.append((text, (p1.x,p1.y), (p2.x, p2.y)))

    return underlined_text


def etc_texts(page, etc_lines):
    """
    etc_lines를 받아 밑줄이 쳐져있는 텍스트를 반환
    etc_text에는 text, text의 처음 위치, text의 마지막 위치가 있음
    """
    etcs = []
    for i in range(len(etc_lines)):
        maxXPoint = 0
        minXPoint = 1000
        maxYPoint = 0
        if etc_lines[i]['items'][0][0] != 'qu' and etc_lines[i]['items'][0][0] != 're':
            for j in range(len(etc_lines[i]['items'])):
                for k in range(1, len(etc_lines[i]['items'][j])):
                    if etc_lines[i]['items'][j][k][0] >= maxXPoint:
                        maxXPoint = etc_lines[i]['items'][j][k][0]
                    if etc_lines[i]['items'][j][k][0] <= minXPoint:
                        minXPoint = etc_lines[i]['items'][j][k][0]
                    if etc_lines[i]['items'][j][k][1] >= maxYPoint:
                        maxYPoint = etc_lines[i]['items'][j][k][1]
        elif etc_lines[i]['items'][0][0] == 're':
            minXPoint = etc_lines[i]['items'][0][1][0]
            maxXPoint = etc_lines[i]['items'][0][1][2]
            maxYPoint = etc_lines[i]['items'][0][1][3]
        else:
            for j in range(len(etc_lines[i]['items'][0][1])):
                if etc_lines[i]['items'][0][1][j][0] >= maxXPoint:
                    maxXPoint = etc_lines[i]['items'][0][1][j][0]
                if etc_lines[i]['items'][0][1][j][0] <= minXPoint:
                    minXPoint = etc_lines[i]['items'][0][1][j][0]
                if etc_lines[i]['items'][0][1][j][1] >= maxYPoint:
                    maxYPoint = etc_lines[i]['items'][0][1][j][1]

        leftPoint = fitz.fitz.Point(minXPoint, maxYPoint)
        rightPoint = fitz.fitz.Point(maxXPoint, maxYPoint)
        etcs.append((leftPoint, rightPoint))

    etc_text = []
    draw_lines = etcs
    blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]
    max_lineheight = 0
    for b in blocks:
        for l in b["lines"]:
            bbox = fitz.Rect(l["bbox"])
            if bbox.height > max_lineheight:
                max_lineheight = bbox.height
    for p1, p2 in draw_lines:
        rect = fitz.Rect(p1.x, p1.y - max_lineheight, p2.x, p2.y)  
        text = page.get_textbox(rect)
        etc_text.append((text, (p1.x, p1.y), (p2.x, p2.y)))

    return etc_text


def highlight_texts(page, fills, boolnext):
    highlight_text = []

    lines = []
    for i in range(len(fills)):
        p1 = fills[i]['items'][0][-1]
        p2 = fills[i]['items'][-1][-1]
        lines.append((p1, p2))

    draw_lines = lines
    blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]
    max_lineheight = 0
    for b in blocks:
        for l in b["lines"]:
            bbox = fitz.Rect(l["bbox"])
            if bbox.height > max_lineheight:
                max_lineheight = bbox.height
    for p1, p2 in draw_lines:
        if type(p1) != int and type(p2) != int:
            rect = fitz.Rect(p1.x, p1.y - max_lineheight / 3, p2.x, p2.y)  
            text = page.get_textbox(rect)
            highlight_text.append((text, (p1.x, p1.y), (p2.x, p2.y)))

    result_text = []
    turn = 0
    while turn < len(highlight_text):
        if boolnext[turn]:
            boundtext = highlight_text[turn][0] + highlight_text[turn + 1][0]
            a = (boundtext, highlight_text[turn][1], highlight_text[turn + 1][2])
            turn += 2
        else:
            a = highlight_text[turn]
            turn += 1
        result_text.append(a)

    return result_text


def sorting_text(underlined_text, etc_text, highlight_text):
    """
    최종적으로 추출해놓은 텍스트 list들을
    y좌표가 큰 순 (= 문단에서 가장 위에부분)으로 정렬
    """
    sorted_list = underlined_text + etc_text + highlight_text

    for i in range(len(sorted_list) - 1):
        min_index = i

        for j in range(i + 1, len(sorted_list)):
            if sorted_list[min_index][1][1] > sorted_list[j][1][1]:
                min_index = j

        sorted_list[i], sorted_list[min_index] = sorted_list[min_index], sorted_list[i]

    return sorted_list