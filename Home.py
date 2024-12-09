### Home.py ###
import streamlit as st

st.set_page_config(page_title="BOGO Home Page", layout="wide")

# 메인 페이지 화면
st.title("Welcome to BOGO Home Page")

# 세션 상태에 저장된 토큰과 사용자 정보 확인
if "access_token" in st.session_state:
    st.success(f"\n환영합니다, {st.session_state.email}님!")
    st.write("로그인이 성공적으로 완료되었습니다.")
else:
    st.warning("로그인이 필요합니다.")
    st.switch_page("pages/2_Sign_In.py")

