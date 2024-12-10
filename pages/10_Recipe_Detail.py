### in pages/10_Recipe_Detail.py ###
import streamlit as st

# 디버깅: selected_recipe 확인
if "selected_recipe" not in st.session_state:
    st.warning("레시피가 선택되지 않았습니다. 레시피 목록에서 레시피를 선택해주세요.")
    st.stop()

# 선택된 레시피 데이터 가져오기
recipe = st.session_state.selected_recipe

# 레시피 정보 표시
st.title(recipe.get("recipe_name", "레시피 이름 없음"))
st.write("---")

difficulty_level = recipe.get('recipe_level', 0)
st.code(f"👥  {recipe.get('recipe_amount', 'N/A')}인분\t⏱️  {recipe.get('recipe_time', 'N/A')}분\t{'⭐' * (difficulty_level + 1)}")

# 재료와 재료량 표시
st.write("---")
st.subheader("필요한 재료")
ingredients = recipe.get("ingredients_title_lst", [])
amounts = recipe.get("ingredients_amount_lst", [])

if ingredients and amounts:
    for ing, amt in zip(ingredients, amounts):
        st.write(f"- **{ing}**: {amt}")
else:
    st.write("재료 정보가 없습니다.")

# 동영상 링크가 있을 경우
video_src = recipe.get("video_src")
if video_src and video_src != "nan":
    st.write("---")
    st.subheader("레시피 동영상")
    st.video(video_src)

# 조리 과정과 이미지 표시
st.write("---")
st.subheader("조리 과정")
steps = recipe.get("recipe_progress_lst", [])
images = recipe.get("recipe_progress_img_lst", [])

for i, (step, img_url) in enumerate(zip(steps, images)):
    st.write(f"{i+1}. {step}")
    if img_url:
        st.image(img_url, width=300)
    st.write("---")

# 뒤로 가기 버튼
if st.button("Back to Recipes"):
    st.switch_page(st.session_state.get("previous_page", "pages/8_Entire_Recipe.py"))
