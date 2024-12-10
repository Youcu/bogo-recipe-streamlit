### in pages/9_Filtered_Recipe.py ###
import streamlit as st
import requests

# API URL
API_URL = "https://bogo-recipe.com/api/recipes/filtered-recipes/"

# 세션 상태에 토큰이 없으면 로그인 페이지로 이동
if "access_token" not in st.session_state:
    st.warning("로그인이 필요합니다.")
    st.switch_page("pages/2_Sign_In.py")

# 카테고리 매핑 JSON
CATEGORY_MAPPING = [
    {"pk": -1, "recipe_category_name": "전체"},
    {"pk": 0, "recipe_category_name": "국_탕"},
    {"pk": 1, "recipe_category_name": "찌개"},
    {"pk": 2, "recipe_category_name": "면_만두"},
    {"pk": 3, "recipe_category_name": "밥_죽_떡"},
    {"pk": 4, "recipe_category_name": "메인반찬"},
    {"pk": 5, "recipe_category_name": "밑반찬"},
    {"pk": 6, "recipe_category_name": "가공식품류"},
    {"pk": 7, "recipe_category_name": "양식"},
    {"pk": 8, "recipe_category_name": "육류"},
    {"pk": 9, "recipe_category_name": "채소류"},
    {"pk": 10, "recipe_category_name": "해물류"}
]

# 카테고리 이름을 선택하면 ID를 반환하는 함수
def get_category_id(name):
    for category in CATEGORY_MAPPING:
        if category["recipe_category_name"] == name:
            return category["pk"]
    return -1  # 기본값

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

# 현재 페이지 기록
st.session_state.previous_page = "pages/9_Filtered_Recipe.py"

# 페이지 UI 구현
st.title("Filtered Recipe Page")

# 카테고리 선택 (이름으로 선택)
category_names = [item["recipe_category_name"] for item in CATEGORY_MAPPING]
selected_category_name = st.selectbox("Recipe Category", category_names)

# 선택한 카테고리의 ID 가져오기
category_id = get_category_id(selected_category_name)

# 레시피 데이터 불러오기
data = read_filtered_recipes(API_URL, st.session_state.access_token, recipe_category=category_id, page=st.session_state.page)

if data:
    recipes = data.get("results", {}).get("results", {})

    # 레시피 단일 리스트로 출력
    for recipe_id, recipe in recipes.items():
        st.image(recipe.get("thumb"), width=300)
        st.subheader(recipe.get("recipe_name"))
        st.write(f"**조리시간:** {recipe.get('recipe_time')}분")
        st.write(f"**난이도:** {recipe.get('recipe_level')}")
        st.write(f"**매칭률:** {recipe.get('match_rate'):.2f}%")
        st.write(f"**주재료 매칭률:** {recipe.get('main_match_rate'):.2f}%")
        st.write(f"**주재료:** {', '.join(recipe.get('main_ingre', []))}")

        # 상세 페이지로 이동 버튼
        if st.button(f"View Details {recipe_id}", key=recipe_id):
            st.session_state.selected_recipe = recipe
            st.switch_page("pages/10_Recipe_Detail.py")

        st.markdown("---")  # 각 레시피 구분선 추가

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
