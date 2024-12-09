### in 9_Filtered_Recipe.py ###
import streamlit as st
import requests

# 인증 토큰 및 API URL
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNjM4NTQwLCJpYXQiOjE3MzM2MzY3NDAsImp0aSI6ImQ1ZmFhMTk4YzIxODQ5ZTY5NjM2MzQ1MTYyNjQzNjg4IiwidXNlcl9pZCI6Mn0.8Uc_1msK5r1xopq4lkfi3jCIj68vv8KW4wiNMFYdJAI"
API_URL = "https://bogo-recipe.com/api/recipes/filtered-recipes/"

# API 함수
def read_filtered_recipes(api, access_token, recipe_category, page=1):
    url = f"{api}?recipe_category={recipe_category}&page={page}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"요청 중 오류 발생: {e}")
        return None

# 페이지 번호 상태 유지
if 'page' not in st.session_state:
    st.session_state.page = 1

# 페이지 UI 구현
st.title("Filtered Recipe Page")

category = st.selectbox("Recipe Category", [-1, 1, 2, 3])  # 예제 카테고리 값

# 레시피 데이터 불러오기
data = read_filtered_recipes(API_URL, ACCESS_TOKEN, recipe_category=category, page=st.session_state.page)

if data:
    recipes = data.get("results", {}).get("results", {})

    # 레시피 출력
    for recipe_id, recipe in recipes.items():
        with st.container():
            st.image(recipe.get("thumb"), width=150)
            st.subheader(recipe.get("recipe_name"))
            st.write(f"**조리시간:** {recipe.get('recipe_time')}분")
            st.write(f"**난이도:** {recipe.get('recipe_level')}")
            st.write(f"**주재료:** {', '.join(recipe.get('main_ingre', []))}")
            st.write("---")

    # 디버그 출력
    st.write(f"Next Page URL: {data.get('next')}")
    st.write(f"Previous Page URL: {data.get('previous')}")
    st.write(f"Current Page: {st.session_state.page}")

    # 페이지네이션 버튼
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if data.get("previous") is not None:
            if st.button("Previous Page"):
                st.session_state.page -= 1
                st.rerun()

    with col3:
        if data.get("next") is not None:
            if st.button("Next Page"):
                st.session_state.page += 1
                st.rerun()
