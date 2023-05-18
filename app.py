
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

coversation_cnt = 0
max_cnt = 5

system_prompt = """
あなたは優秀な英語教師です。
これから私とアメリカの空港での入国審査の時の英会話のレッスンを行います。

## 要件
- これ以降すべて10単語以内で入国審査官として私に英語でひとつずつ質問してください。
- それに対して私も英語で答えますので、答えたらまたあなたが質問してください。
- TOEICスコアー400点でもわかる英語で行ってください。
- 私の言った言葉に End! が入っていたら会話のレッスンは終わりで、それ以降は日本語で話してください。そして、私のそれまでに話した英語について、間違いやもっといい言い回しがあれば日本語で教えてください。

【出力 フォーマット】Officer: + あなたの質問
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate(messe):
    messages = st.session_state["messages"]

    if messe == "":
        user_message = {"role": "user", "content": st.session_state["user_input"]}
        messages.append(user_message)
    else:
        user_message = {"role": "user", "content": messe}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

    coversation_cnt = coversation_cnt + 1

    if coversation_cnt == 5:
        communicate("End!")



# ユーザーインターフェイスの構築
st.title("英会話レッスン - 入国審査")
st.write("アメリカの空港での入国審査の時の英会話のレッスンを行います。")
st.write("入国審査官の質問に英語で答えてください。")
st.write("５回やり取りしたら、最後にあなたの英語の評価が表示されます。")

user_input = st.text_input("答えてください", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
