### in pages/2_Sign_In.py ###
import streamlit as st
import requests

API_LOGIN_URL = "https://bogo-recipe.com/api/users/signin/"

def login(email, password):
    payload = {"email": email, "password": password}
    try:
        response = requests.post(API_LOGIN_URL, json=payload)
        if response.status_code == 200:
            tokens = response.json()
            st.session_state.access_token = tokens["access"]
            st.session_state.refresh_token = tokens["refresh"]
            st.session_state.email = email
            st.success("로그인 성공!")
            st.switch_page("Home.py")
        else:
            st.error(f"로그인 실패: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"요청 중 오류 발생: {e}")

st.title("Sign In")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    login(email, password)
