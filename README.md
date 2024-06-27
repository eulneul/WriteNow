# WriteNow - 필기 및 문서 요약 서비스 
----------
## 프로젝트 배경 및 소개
>노트 대신 디지털 기기... 대학 강의실 필기 문화 바뀌었다 <br/>
>http://www.civicnews.com/news/articleView.html?idxno=34583 <br/>
>'대학 복사실 앞 긴 줄' 옛말…"요즘엔 다 패드로 보죠" <br/>
>https://www.yna.co.kr/view/AKR20231013166100004 <br/>

<br/>
문서에서 필기 정보(하이라이트, 밑줄, 네모 등)를 인식하고 추출하여, 문단 내에서 더 중요한 내용을 요약문에 포함시키는 서비스다.  <br/><br/>
코로나 19 사태 이후 온라인 미팅과 수업이 사회 전반에 사용이 되며 사람들은 책과 종이 대신 전자문서에 필기를 하곤 한다. 
그러나 강의 자료나 문서 등은 때론 수십, 수백 페이지에 달하며 읽거나 학습하는 사용자로 하여금 부담감과 압박감을 느끼게 만든다. 
따라서 최근 문서를 요약해주는 서비스의 수요가 늘고 있으며, 문서의 내용 뿐만 아니라 문서에 필기된 내용까지 요약해주는 웹 서비스를 개발하고자 한다.  <br/>

<br/>

-----------
## 과제 내용
필기 인식 모듈, 요약 모델, 웹 서비스 구현으로 나누어 과제를 수행했다. 필기 인식 모듈은 PyMuPDF 라이브러리를 이용해 필기 정보를 추출하고, 이 정보를 요약 모델에게 전달한다. 요약 모델은 KoBART 모델을 사용하였고, 필기 모듈로부터 전달받은 중요한 내용을 포함하여 요약을 진행한다. 최종결과물인 웹 서비스는 Flask를 이용해 구현하였다. <br/>
사용자가 기록한 필기(하이라이트, 밑줄, 네모)로부터 중요한 단어와 문장, 문단을 알아내고, 이들에게 가중치를 부여하여 내용 요약에 반영한다. 단순 본문 요약에서는 삭제될 수 있는 내용도 사용자가 필기한 내용은 필수적으로 요약에 포함한다. 최종 요약본에는 중요한 문장이나 단어가 하이라이트로 표시된다.사용자가 요약된 본문을 공부할 때 자신이 기록했던 필기 내용을 참고하게 한다. 이로써 사용자가 중점적으로 표기 및 필기한 부분이 단순히 요약된 글보다 눈에 더 잘 들어올 것이다. 이를 통해 사용자는 이전 기억을 빠르게 상기할 수 있고, 본문의 핵심을 한 눈에 인지할 수 있다.


-----------
## 개발 언어

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white"/>
<img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white"/>
<br/>

## 개발 도구 / 프레임워크
<img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white"/> <img src="https://img.shields.io/badge/Google Colab-F9AB00?style=flat-square&logo=Google Colab&logoColor=white"/>
<img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/>

## 외부 라이브러리
[PyMuPDF](https://github.com/pymupdf/PyMuPDF) - pdf 정보 추출 위해 사용 <br/>
[KoBART-news](https://huggingface.co/ainize/kobart-news) - 문서 요약 모델로 활용

------
## 아키텍쳐

![architecture](https://github.com/eulneul/WriteNow/assets/70475010/37a58260-b1ec-445b-a752-a27fc169a3df)

<br/>

------
## 데모 영상



https://github.com/eulneul/WriteNow/assets/70475010/a53157b0-1f39-4d2a-a57e-f7091f23b727

------
## 결과 및 향후 개발 개획
### 결과
 필기 추출 및 요약 서비스의 자동화를 구현하는 것은 성공하였다. 이 롸잇나우 서비스를 통해 사용자는 필기 내용과 요약된 본문을 같이 파악하게 할 수 있다. 이로써 사용자가 이전 기억을 빠르게 상기할 수 있도록 도와주며, 중요한 포인트를 한 눈에 볼 수 있도록 한다. <br/>

### 사용자 필기 글씨 인식 OCR 모델 구현
- 필기 어플리케이션을 사용하는 사용자 중에서는 직접 손으로 필기를 하는 경우도 많으니 그렇게 필기한 내용도 추출하는 기능을 추가할 예정이다. 또한, 이미지 위에 사용자가 그림을 그린 내용도 요약문에 포함시킬 예정이다.
### UI 개선
- 사용자 친화적인 UI로의 개선, 로딩 페이지, 로그인 및 이전 요약문 확인 페이지 등

### 기타 요약 모델 성능 개선 및 오류 수정

