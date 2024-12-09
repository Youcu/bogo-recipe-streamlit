import streamlit as st

# 세션에서 선택된 레시피 확인
if "selected_recipe" not in st.session_state:
    st.warning("레시피를 선택해주세요.")
    st.switch_page("pages/8_Entire_Recipe.py")

recipe = st.session_state.selected_recipe

# 레시피 상세 정보 UI 구현
st.title(recipe.get("recipe_name"))
st.write(f"**인분:** {recipe.get('recipe_amount')}인분")
st.write(f"**조리시간:** {recipe.get('recipe_time')}분")
st.write(f"**난이도:** {recipe.get('recipe_level')}")
st.write("### 필요한 재료")

# 재료와 재료량 표시
ingredients = recipe.get("ingredients_title_lst", [])
amounts = recipe.get("ingredients_amount_lst", [])

if ingredients and amounts:
    for ing, amt in zip(ingredients, amounts):
        st.write(f"- **{ing}**: {amt}")
else:
    st.write("재료 정보가 없습니다.")

st.write("\n### 조리 과정")

# 비디오 링크 표시 (video_src가 존재하고 유효할 경우)
video_src = recipe.get("video_src")
if video_src and video_src != "nan":
    st.write("\n### 레시피 영상")
    st.video(video_src)

# 조리 과정과 이미지 표시
steps = recipe.get("recipe_progress_lst", [])
images = recipe.get("recipe_progress_img_lst", [])

for i, (step, img_url) in enumerate(zip(steps, images)):
    st.write(f"{step}")
    if img_url:
        st.image(img_url, width=300)
    st.write("---")


# 뒤로 가기 버튼
if st.button("Back to Recipes"):
    st.switch_page("pages/8_Entire_Recipe.py")
