# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, g
import os
import fitz
from notemodel import *

from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from readlines import *

app = Flask(__name__)


tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
model = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")




# 업로드된 파일을 저장할 폴더
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdfFile' not in request.files:
        return 'No file part'

    file = request.files['pdfFile']

    if file.filename == '':
        return 'No selected file'

    if file:
        # 업로드된 파일을 저장할 경로 설정
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return 'File uploaded successfully!'

@app.route('/pymodel')
def pymodel():
    import shutil
    current_directory1 = os.getcwd()

    shutil.move(os.path.join(current_directory1, 'uploads', 'example_note2.pdf'), current_directory1)


    pdf_name = "example_note2.pdf"
    make_md(pdf_name)
    doc = fitz.open(pdf_name)
    pdf_to_img(doc)

    current_directory2 = os.getcwd()

    # 상대 경로로 이동할 파일과 대상 디렉토리 설정
    source_file = os.path.join(current_directory2, 'pdf_image0.png')
    destination_directory = os.path.join(current_directory2, 'static', 'images')

    # 파일 이동
    shutil.move(source_file, destination_directory)



    f = open("notetext.txt", 'w', encoding='utf-8')
    f.close()
    for i in range(len(doc)):
        page = doc[i]
        paths = draw_path(page)
        fills, colors = find_color(paths)
        if fills == [] and colors == []:
            break
        else:
            real_lines, etc_lines = find_line(colors)
            boolNext = combine_line(fills)
            underlined_text = underlined_texts(page, real_lines)
            etc_text = etc_texts(page, etc_lines)
            highlight_text = highlight_texts(page, fills, boolNext)
            sorted_list = sorting_text(underlined_text, etc_text, highlight_text)
            if i == 0:
                f = open("notetext.txt", 'w', encoding='utf-8')
            else:
                f = open("notetext.txt", 'a', encoding='utf-8')
            f.write("Page {}\n".format(i))
            f.write("Important texts \n-------------------\n")
            for j in range(len(sorted_list)):
                data = sorted_list[j][0] + '\n'
                f.write(data)
            f.close()

    # 요약 모델 시작
    weight_list = save_weight("notetext.txt", doc)
    weight_list = delete_n(weight_list)
    summarized_list = []
    lst = []
    for p in range(len(doc)):
        page = doc[p]  # 첫 번째 페이지
        result_text = []
        result_page = []
        paragraph = splittext(page)
        weight = weight_list[p].copy()
        add_sentence(weight, paragraph, lst)
        indexing = [item[0] for item in lst[0]]
        result_list = paragraph_to_list(paragraph)
        temp_paragraph = insert_sentence(doc, p, lst)
        summarized_text = ''

        for i in range(len(temp_paragraph)):
            onep = temp_paragraph[i]
            result_text.append([dotandcombine(onep)])
        for i in range(len(result_text)):
            if len(result_text[i][0]) > 30:
                input_ids = tokenizer.encode(result_text[i][0], return_tensors="pt")

                if i in indexing:
                    summary_text_ids = model.generate(
                        input_ids=input_ids,
                        bos_token_id=model.config.bos_token_id,
                        eos_token_id=model.config.eos_token_id,
                        length_penalty=2.0,
                        max_length=round(len(result_text[i][0]) / 5),
                        min_length=round(len(result_text[i][0]) / 15 + len(result_text[i]) / 20),
                        num_beams=4,
                    )
                else:
                    summary_text_ids = model.generate(
                        input_ids=input_ids,
                        bos_token_id=model.config.bos_token_id,
                        eos_token_id=model.config.eos_token_id,
                        length_penalty=2.0,
                        max_length=round(len(result_text[i][0]) / 5),
                        min_length=round(len(result_text[i][0]) / 15),
                        num_beams=4,
                    )
                summarized_text = summarized_text + tokenizer.decode(summary_text_ids[0],
                                                                     skip_special_tokens=True) + '\n'
            else:
                summarized_text = summarized_text + result_text[i][0] + '\n'
        summarized_list.append(summarized_text)
        """
        추가된 부분
        확인되면 이 주석은 지울 것 
        """
        styled_hl = add_style(summarized_list, weight_list, p)
        result_with_highlight = combine_hl(styled_hl)
        g.python_output = (result_with_highlight)

    html_content = f"""
    
    
    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR&display=swap" rel="stylesheet">
        <link href="static/css/font.css" rel="stylesheet" />

        
        <title>Summarization Completed!</title>

    </head>
    <body class = "my_gradient_1">
        <table border="1" cellpadding="10" align = "center" valign="middle" style="width:70%; height:auto;background-color:white; table-layout:fixed;">
        <th>원문</th>
        <th>요약문</th>
        <tr> <!--첫째 행-->	
           <td>
            <p>
            <img src="/static/images/pdf_image0.png" style="display: block; margin: 0 auto; width: 100%; height: auto;  padding: 10px 0px 30px 0px;"/>
            </p>
            </td>
            <td>
            <p> {g.python_output} </p></td>
        </tr>
            <img src="static/images/writenowlogo.png" style="display: block; margin: 0 auto; width: 20%; height: auto; padding: 10px 0px 30px 0px;" />

    </body>
    </html>
    """

    with open('output.html', 'w') as file:
        file.write(html_content)
    print("HTML file created successfully.")

    current_directory3 = os.getcwd()

    # 상대 경로로 이동할 파일과 대상 디렉토리 설정
    source_file1 = os.path.join(current_directory3, 'output.html')
    destination_directory1 = os.path.join(current_directory3, 'templates')

    # 파일 이동
    shutil.move(source_file1, destination_directory1)

    return render_template("output.html")




if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 9900)