import streamlit as st
import json
import requests

# IngreList.json 데이터 로드
with open("IngreList.json", "r", encoding="utf-8") as file:
    ingre_list = json.load(file)

# 재료명과 id 매핑 테이블 생성
ingre_mapping = {item["fields"]["ingre_name"]: item["pk"] for item in ingre_list}

# 위치 매핑 (0: 냉장실, 1: 냉동실, 2: 선반)
loc_mapping = {
    "냉장실": 0,
    "냉동실": 1,
    "선반": 2
}

# 세션에 토큰이 있는지 확인
if "access_token" not in st.session_state:
    st.warning("로그인이 필요합니다. 로그인 페이지로 이동합니다.")
    st.switch_page("pages/2_Sign_In.py")

# 페이지 제목
st.title("Input Ingredients")

# 입력 필드
ingredient_names = st.text_input("재료 입력 (예: 계란, 대파)")
ingredient_amounts = st.text_input("재료양 입력 (예: 500g, 1병)")
ingredient_expiry = st.text_input("유통기한 입력 (예: 2024-12-15, 2024-12-28)")
ingredient_locations = st.text_input("재료 위치 입력 (예: 0, 2) (냉장실: 0, 냉동실: 1, 선반: 2)")

# Save 버튼
if st.button("Save"):
    # 입력값을 리스트로 변환
    ingre_names_list = [name.strip() for name in ingredient_names.split(",") if name.strip()]
    ingre_amounts_list = [amount.strip() for amount in ingredient_amounts.split(",") if amount.strip()]
    expiry_list = [expiry.strip() for expiry in ingredient_expiry.split(",") if expiry.strip()]
    loc_list = [loc.strip() for loc in ingredient_locations.split(",") if loc.strip()]

    # 모든 입력 리스트의 길이가 일치하는지 확인
    if len(ingre_names_list) != len(ingre_amounts_list) or len(ingre_names_list) != len(expiry_list) or len(ingre_names_list) != len(loc_list):
        st.error("재료명, 재료양, 유통기한, 재료 위치의 수가 일치하지 않습니다. 다시 확인해주세요.")
    else:
        # 재료명을 ingre_id로 매핑
        ingre_id_lst = []
        for name in ingre_names_list:
            ingre_id = ingre_mapping.get(name)
            if ingre_id is not None:
                ingre_id_lst.append(ingre_id)
            else:
                st.warning(f"'{name}' 재료는 매핑 테이블에 없습니다.")

        # 위치를 loc_id로 매핑
        ingre_loc_lst = []
        for loc in loc_list:
            try:
                ingre_loc_lst.append(int(loc))
            except ValueError:
                st.warning(f"'{loc}'는 유효한 위치 id가 아닙니다.")

        # 모든 데이터가 매핑되었는지 확인
        if len(ingre_id_lst) == len(ingre_names_list) and len(ingre_loc_lst) == len(loc_list):
            # API에 전송할 데이터
            payload = {
                "ingre_id_lst": ingre_id_lst,
                "user_ingre_amount_lst": ingre_amounts_list,
                "expiry_lst": expiry_list,
                "ingre_loc_lst": ingre_loc_lst
            }

            # API URL
            API_URL = "https://bogo-recipe.com/api/users/ingredients/"
            headers = {
                "Authorization": f"Bearer {st.session_state.access_token}",
                "Content-Type": "application/json"
            }

            # API 요청 보내기
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 200 or response.status_code == 201:
                    st.success("재료가 성공적으로 저장되었습니다!")
                else:
                    st.error(f"저장 실패: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"요청 중 오류 발생: {e}")
        else:
            st.error("재료 또는 위치 매핑 중 오류가 발생했습니다.")
