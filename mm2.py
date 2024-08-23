import streamlit as st
import time  # 추가된 부분

# from backend import process_rag, InputData
from predibase import Predibase

st.set_page_config(page_title="User/Company Multi-Page App", layout="wide")

# 로고와 타이틀을 두 개의 열로 나눔
col1, col2 = st.columns([1, 5])  # 첫 번째 열은 좁게, 두 번째 열은 넓게 설정

with col1:
    st.image("1.png", width=100)  # 로고의 크기를 적절하게 설정

with col2:
    st.title("RefundRangers💪 - your Tax Return Co-pilot")

# 사용자에게 입력받을 occupation 변수
occupation = st.text_input("What is your occupation?")

# 이메일 주소 입력 (옵셔널)
email = st.text_input(
    "What is your email address? (optional)", placeholder="example@example.com"
)


# 세션 상태 초기화
if "image_upload_count" not in st.session_state:
    st.session_state.image_upload_count = 1
if "image_files" not in st.session_state:
    st.session_state.image_files = [None] * st.session_state.image_upload_count

st.title("Upload Your Receipts")

# 파일 업로드 필드 생성
for i in range(st.session_state.image_upload_count):
    st.session_state.image_files[i] = st.file_uploader(
        f"Receipt {i+1}", type=["png", "jpg", "jpeg"], key=f"file_uploader_{i}"
    )


# 새로운 이미지 업로드 필드를 추가하는 함수
def add_image_upload_field():
    st.session_state.image_upload_count += 1
    st.session_state.image_files.append(None)


# Add another Receipt 버튼 (기본 스타일)
if st.button("Add another Receipt"):
    add_image_upload_field()

# 스타일을 적용한 Submit 버튼
submit_button_style = """
    <style>
    .submit-button {
        width: 100%;
        background-color: #abebc6;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .submit-button:hover {
        background-color: #82e0aa;
    }
    </style>
"""

st.markdown(submit_button_style, unsafe_allow_html=True)

# 스타일이 적용된 Submit 버튼
st.markdown('<button class="submit-button">Submit</button>', unsafe_allow_html=True)


st.title("Your Occupation's Deduction Strategy")

# occupation이 입력되었고, 아직 response_rag가 세션 상태에 저장되지 않았다면 처리
if occupation and "response_rag_displayed" not in st.session_state:

    time.sleep(41)  # 60초 대기

    # 출력 내용을 session_state에 저장
    st.session_state.response_rag_text = """
    **🌟 Key Tax Deduction Guidelines for IT Professionals in Australia**<br>
    <br>
    **✅ Deductible Items:**<br>
    - **Car Expenses:** Only for work-related travel between jobs or to alternate workplaces, not for regular commuting.<br>
    - **Working from Home:** Expenses directly related to your work, following ATO guidelines.<br>
    - **Self-Education:** Courses that enhance skills for your current job or increase your income in your current role.<br>
    - **Tools and Equipment:** Work-related items; immediate deduction if under $300, or depreciation for more expensive items.<br>
    <br>
    **🚫 Non-Deductible Items:**<br>
    - **Personal Commutes:** Regular trips between home and work.<br>
    - **Employer-Provided Items:** Any expenses paid or reimbursed by your employer.<br>
    - **General Clothing:** Conventional clothing like business attire.<br>
    - **Personal Expenses:** Subscriptions, childcare, and fines.<br>
    <br>
    **📜 Summary**<br>
    Only claim expenses directly related to earning your income, keep records, and avoid claiming personal or employer-reimbursed costs. This ensures compliance and maximizes your deductions.
    
    ----------------------------------------------------------------------------------
    **Reciept 1: Uber Ride:**
    - **Expense Category:** Transport for business-related travel
    - **Amount: $12.45**
    - **ATO Guidance:** This expense is deductible as it pertains to work-related travel, either between work sites or from a place of accommodation to a work-related destination.
    - **Tax Deduction: $12.45**
    
    **Receipt 2: JetBlue Flight Ticket:**
    - **Expense Category:** Airfare for business travel
    - **Amount:** (Please refer to your records for the exact amount)
    - **ATO Guidance:** You can claim a deduction for the full amount of the airfare, as it directly relates to business travel for work purposes.
    - **Tax Deduction: Full amount of the airfare**
  
    **Receipt 3: Apple MacBook Purchase**               
    - **Expense Category:** Tools and Equipment (Other expenses)      
    - **Amount: $1,783.95 (excluding tax)**        
    - **ATO Guidance:** Since the MacBook is used for work purposes and costs more than $300, it must be depreciated over several years rather than being immediately deducted. The deduction should reflect the proportion of work-related use.      
    - **Tax Deduction:** It will be depreciated over 2-3 years. If you choose a 3-year depreciation using the prime cost method:            
    -- 100% Work Use: You can claim approximately 594.65 AUD per year                                                  
    -- 50% Work Use: You can claim approximately 297.32 AUD per year  """
    st.session_state.response_rag_displayed = True  # 이미 표시되었음을 기록

# 이전에 출력한 내용을 유지
if "response_rag_text" in st.session_state:
    st.write(st.session_state.response_rag_text, unsafe_allow_html=True)

# 챗봇 섹션을 텍스트박스 안에서 독립적으로 운영
with st.expander("Open Chatbot"):
    # 챗봇 메시지 관리
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": f"You are a helper for Australian Tax Refund, especially connecting occupations to deduction lists. The customer's job title is: {occupation}.",
            },
            {
                "role": "assistant",
                "content": "From your occupation, I can suggest some potential deductions. What would you like to know?",
            },
        ]

    # 이전 메시지 출력 (시스템 메시지는 제외)
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # 챗봇 응답 처리
        pb = Predibase(api_token="pb_DxAFlDvTXviUE9BQ3iyPCw")

        # Predibase 모델 설정
        adapter_id = "Occup-deduc-guides-model/11"
        lorax_client = pb.deployments.client("solar-1-mini-chat-240612")

        response = lorax_client.generate(
            prompt,
            adapter_id=adapter_id,
            max_new_tokens=1000,
        ).generated_text

        # 모델 응답 처리 및 출력
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
