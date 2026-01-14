# 1. 라이브러리 가져오고 api key를 환경 변수에서 가져오기
import os
from PIL import Image
import google.genai as genai
# from dotenv import load_dotenv
# -0) 라이브러리 추가하기 : streamlit
import streamlit as st

# load_dotenv()

# 1. 클라이언트 생성 (API 키 설정)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 2.모델이 이미지 분류 요청 함수 정의하기
# client 객체의 models.generate_content 사용
def classify_image(prompt, image,model):
    response = client.models.generate_content(
        model, 
        contents=[prompt, image]
    )
    return response.text

# 3.프롬프트 선언하고 이미지 분류 실행하기
# GPT에게 보낼 프롬프트 정의
prompt = """
영상을 보고 다음 보기 내용이 포함되면 1, 포함되지 않으면 0으로 분류해줘.
보기 = [건축물, 바다, 산]
JSON format으로 키는 'building', 'sea', 'mountain'으로 하고 각각 건축물, 바다, 산에 대응되도록 출력해줘.
자연 이외의 건축물이 조금이라도 존재하면 'building'을 1로, 물이 조금이라도 존재하면 'sea'을 1로, 산이 조금이라도 보이면 'mountain'을 1로 설정해줘.
markdown format은 포함하지 말아줘.
"""

# img = Image.open('imgs_classification/01.jpg')  # 이미지 열기
# #img = Image.open(os.path.join('imgs_classification', '01.jpg'))  # 이미지 열기
# response = classify_image(prompt, img)     # GPT로부터 분류 결과 받기
# print(response)  # 결과 출력

st.set_page_config(
    page_title = 'Image Classification - Gemini',
    layout = "centered",
    initial_sidebar_state="auto"
)
st.title = 'Image Classification - Gemini'

with st.sidebar:
    model = st.selectbox(
        'Model Selection',
        options = ['gemini-2.0-flash','gemini-2.0-flash-lite'],
        index = 0
    )

prompt = st.text_area('Prompt Input',value=prompt, height = 300)
uploaded_file = st.file_uploader('Image upload',type = ['jpg','jpeg','png'])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption = 'Uploaded Image',width='content')
    if st.button('Classification Excution'):
        with st.spinner('ing...'):
            response = classify_image(prompt, img, model=model)
        st.subheader('Result')

        st.code(response)
