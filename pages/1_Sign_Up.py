### in pages/1_Sign_Up.py ###
import streamlit as st
import requests

# API URL 설정
API_SIGNUP_URL = "https://bogo-recipe.com/api/users/signup/"

# 회원가입 함수
def sign_up(email, password, confirm_password, name, gender, convenience):
    # 입력된 비밀번호와 확인 비밀번호가 일치하는지 검사
    if password != confirm_password:
        st.error("비밀번호가 일치하지 않습니다.")
        return

    # 서버로 보낼 데이터 생성
    payload = {
        "email": email,
        "password": password,
        "name": name,
        "gender": gender,
        "convenience": convenience
    }

    try:
        # 회원가입 API 호출
        response = requests.post(API_SIGNUP_URL, json=payload)
        
        # 성공적으로 가입된 경우
        if response.status_code == 201:
            st.success("회원가입이 완료되었습니다! 로그인 페이지로 이동합니다.")
            st.switch_page("pages/2_Sign_In.py")
        else:
            # 서버로부터 반환된 에러 메시지 출력
            st.error(f"회원가입 실패: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"요청 중 오류 발생: {e}")

# UI 설정
st.title("Sign Up")

email = st.text_input("Email")
name = st.text_input("Name")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

gender = st.selectbox("Gender", ["M", "F", "Other"])
convenience = st.checkbox("I agree to use convenience features")

if st.button("Sign Up"):
    sign_up(email, password, confirm_password, name, gender, convenience)
