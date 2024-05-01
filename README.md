# Quanters
## ML을 활용한 주식 투자 예측 시스템
<br />

## 팀원별 역할
#### 🍔 김대현
- UI
	- Springboot + Java 환경을 통해 검색을 통해 해당 주가 예측 결과를 표시해주는 UI 구축
- CI/CD
	- AWS EC2 서버를 구축하여 젠킨스를 통해 Github commit시 Webhook을 유발하여 자동 배포 및 톰캣 서버 실행 자동화 설정
	- AWS S3 스토리지 서버를 통해 주가 예측 결과 csv 파일이 적재되고 UI에서 parsing 하는 구조 구축

#### ⛰️ 김산
- Data crawling
	- 뉴스 데이터
	- 주가 데이터
- Data EDA
	- 뉴스 본문 전처리
	- 뉴스와 주가 데이터를 병합하기 위한 전처리
	- Feature selection
- Modeling
	- 뉴스 본문 감성분석
	- 뉴스 데이터와 주가 데이터 병합
	- 주가 데이터를 기반으로 labeling
	- 주가 예측 모델링
<br />

## Development_Skills

<div align=left>
  
##### BACK-END
  <img src="https://img.shields.io/badge/Spring Boot-6DB33F?style=flat&logo=Spring Boot&logoColor=white"/>
  <img src="https://img.shields.io/badge/Java-007396?style=flat&logo=Java&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/>

##### FRONT-END
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=HTML5&logoColor=white"/></a> 
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=CSS3&logoColor=white"/></a> 
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=JavaScript&logoColor=white"/></a>
  <img src="https://img.shields.io/badge/jQuery-0769AD?style=flat&logo=jQuery&logoColor=white"/></a>
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=flat&logo=Bootstrap&logoColor=white"/></a> 

##### CI/CD
  <img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=Git&logoColor=white"/></a> 
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=GitHub&logoColor=white"/></a> 
  <img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=flat&logo=Amazon EC2&logoColor=white"/></a> 
  <img src="https://img.shields.io/badge/Amazon S3-569A31?style=flat&logo=Amazon S3&logoColor=white"/>
  <img src="https://img.shields.io/badge/GCP-4285F4?style=flat&logo=googlecloud&logoColor=white"/></a> 
  <img src="https://img.shields.io/badge/Jenkins-D24939?style=flat&logo=Jenkins&logoColor=white"/></a>
  <img src="https://img.shields.io/badge/Filezilla-BF0000?style=flat&logo=filezilla&logoColor=white"/></a> 

##### ML
> BERT : KLUE-BERT(뉴스데이터를 pre-trained) <br />
> 형태소 분석기 : Mecab <br />
> Model : Autogluon <br />

##### 협업툴
  <img src="https://img.shields.io/badge/Notion-000000?style=flat&logo=Notion&logoColor=white"/></a>

<br />

## 프로젝트 개요
> Machine Learning 기술을 활용하여 주식 관련 뉴스 기사 데이터를 분석하여 특정 주식 종목의 주가 변동을 예측하는 시스템.<br />
> Quant Investment(퀀트투자)란 일반적으로 투자자들이 산업과 기업을 분석해 가치를 매기는 정성적인 투자법과는 달리, 수학과 통계를 기반으로 전략을 만들고 이를 바탕으로 투자하는 정량적인 투자법을 의미합니다. <br />
> 이에 ML 기술을 활용해 퀀트투자(Quant)를 하는 사람들(ers) 이라는 의미로 Quanters라는 프로젝트를 시작하게 되었습니다.<br />

<br />

## 참고
> [A study on Deep Learning-based Stock Price Prediction using News Sentiment Analysis](https://koreascience.kr/article/JAKO202225752973104.page) <br />
> [뉴스와 주가 빅데이터 감성분석을 통한 지능형 투자 의사결정 모형](https://www.dbpia.co.kr/pdf/pdfView.do?nodeId=NODE01901732&googleIPSandBox=false&mark=0&ipRange=false&b2cLoginYN=false&aiChatView=B&readTime=15-20&isPDFSizeAllowed=true&nodeHistoryTotalCnt=2&accessgl=Y&language=ko_KR&hasTopBanner=true)

<br />

## 프로젝트 소개
> 프로젝트 주제 : 머신러닝을 활용한 뉴스테이터 분석 및 주가 예측 시스템<br />
> 프로젝트 기간 : 2023.12.24~ <br />
> 가설 : 전날 폐장 이후부터 당일 개장 전까지의 뉴스가 당일 개장 후 주가에 영향을 미친다.

<br />

## Version 1.0
> 삼성전자, SK 하이닉스, 네이버, 카카오 4개의 주식 종목만 특정하여 해당 주가의 주가 상승/하락 여부만 판단하여 사용자에게 정보 제공하는 형태

![quanters](https://github.com/kimdaehyuun/Quanters/assets/111870436/8d4972ef-922b-4b4a-9bdd-3a8e16e13e7c)

<br />


## 프로젝트 작업순서
1. 뉴스 데이터 수집
2. 주가 데이터 수집
3. 데이터 전처리
4. 뉴스 본문 감성분석
5. 일별 감성점수 계산
6. 데이터 통합
7. modeling

<br />

#### 1. 뉴스 데이터 수집
2023년 1월부터 11월까지의 기사 수집

![news](https://github.com/kimdaehyuun/Quanters/assets/111870436/5f6ba644-3945-430d-940e-27cc4975a654)


#### 2. 주가 데이터 수집
일별 주가 데이터, 로그 데이터, 로그 후 차분한 데이터 확인

![stock](https://github.com/kimdaehyuun/Quanters/assets/111870436/bdeb18d9-3482-41c1-a8c6-185be52f2e18)


#### 3. 데이터 전처리
- 뉴스 본문 불용어 제거

- 기업별 기사 단어 빈도 확인 (삼성전자, SK하이닉스, 네이버, 카카오)

<img width="119" alt="삼성전자 기사 빈도" src="https://github.com/kimdaehyuun/Quanters/assets/111870436/0eaa2c5c-6c08-4182-b5dc-1de04a77c079">
<img width="119" alt="sk하이닉스 기사 빈도" src="https://github.com/kimdaehyuun/Quanters/assets/111870436/457dc6a0-9c61-44b8-901c-c3f618a8e8b8">
<img width="109" alt="네이버 기사 빈도" src="https://github.com/kimdaehyuun/Quanters/assets/111870436/b30fec74-7047-43d8-a70c-10cd8f1048fd">
<img width="112" alt="카카오 기사 빈도" src="https://github.com/kimdaehyuun/Quanters/assets/111870436/ff28fdbe-67a1-4ec6-b00a-6a2f8912befa">


- SBERT를 이용한 기사 본문 키워드 추출

```
sbert = SentenceTransformer('jhgan/ko-sroberta-multitask')

doc_emb = sbert.encode(df['article'])
doc_idx = 0

word_emb = sbert.encode(words)
dists = cosine_distances(doc_emb[[doc_idx]], word_emb).flatten()
for i in np.argsort(dists)[:10]:
    print(words[i])

```
<img width="46" alt="스크린샷 2024-05-01 오후 5 12 31" src="https://github.com/kimdaehyuun/Quanters/assets/111870436/450a4510-917a-49f6-9fb1-50c6beaf8e40">



## 프로젝트 파이프라인
  ![pipeline_3](https://github.com/kimdaehyuun/Quanters/assets/42797206/99d14914-afa9-4b58-b04f-510ef641d939)
  - 로컬 환경의 IntelliJ에서 코드 개발
  - Github로 commit & push
  - AWS EC2 서버에 띄워져있는 Jenkins가 깃허브의 push로부터 webhook을 일으켜 빌드 유발
  - EC2 서버에서 bootWar로 빌드 후 톰캣 서버 실행. 추후 사이트 접속 가능.
  - 머신러닝은 GPU가 탑재되어있는 GCP 서버에서 수행되어야하므로 젠킨스에서 빌드 후 조치사항으로 GCP 서버에 깃허브 repository의 파이썬 소스 디렉토리만 전송
  - GCP 서버에서는 파이썬 소스가 cron으로 수행되며 데이터 크롤링, 학습, 예측 작업을 거쳐서 그 날의 해당 주식 주가 예측 최종 결과파일을 AWS S3에 csv 파일 형태로 적재
  - 사이트 UI에서는 해당 날짜의 예측 결과를 AWS S3로부터 parsing하여 화면에 예측 결과 표시
  
</div>


## 모델 구조

![quanters_model_architect](https://github.com/kimdaehyuun/Quanters/assets/111870436/fa12da60-2019-4efc-852d-e6dae2dbb4f2)


</div>