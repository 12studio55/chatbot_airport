
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

coversation_cnt = 0
max_cnt = 9
end_flg = 0

system_prompt = """
あなたは優秀な英語教師です。
これから私とアメリカの空港での入国審査の時の英会話のレッスンを行います。

## 要件
- これ以降すべて10単語以内で入国審査官として私に英語でひとつずつ質問してください。
- それに対して私も英語で答えますので、答えたらまたあなたが質問してください。
- 私の言った言葉に End! が入っていたら会話のレッスンは終わりで、それ以降はあなたは日本語で話をして、あなたは私の話した英語について、間違いやもっといい言い回しがあれば日本語で教えてください。
【出力 フォーマット】Officer: + あなたの質問
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt},
#        {"role": "user", "content": "Hello"},
#        {"role": "assistant", "content": "Hi, welcome to the United States. What is the purpose of your visit?"}
        ]

# チャットボットとやりとりする関数
def communicate(messe=""):
    global coversation_cnt
    global max_cnt
    global end_flg

#    messages = st.session_state["messages"]

    if st.session_state["user_input"] == "":
        st.session_state["user_input"] = "私の話した英語について、間違いやもっといい言い回しがあれば日本語で教えてください。"

    messages = st.session_state["messages"]


    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)


    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("英会話レッスン -- 入国審査編")
st.text("アメリカの空港での入国審査の時の英会話のレッスンを行います。\n入国審査官の質問に英語で答えてください。\n5回やり取りしたら、最後にあなたの英語の評価が表示されます。\n\n")

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in messages[1:]:  # 直近のメッセージを下に
        speaker = "🙂: "
        if message["role"]=="assistant":
            speaker="👮‍♂️ "

        coversation_cnt = coversation_cnt + 1
        if coversation_cnt <= max_cnt:
            #st.write(speaker + str(coversation_cnt) + " " + message["content"])
            st.write(speaker + " " + message["content"])

inp_mess = ""
if coversation_cnt == 0 :
    inp_mess = "最初に Hi! または Hello と入国審査官に話しかけてください"
else : 
    inp_mess = "英語で答えてください"

if coversation_cnt < max_cnt:
    user_input = st.text_input(inp_mess, key="user_input", on_change=communicate)
elif coversation_cnt >= max_cnt and end_flg == 0:
    end_flg = 1
    communicate()
    
    speaker="👌 "

    if st.session_state["messages"]:
        messages = st.session_state["messages"]

        for message in messages[coversation_cnt+2:]:  # 最後のメッセージ
            st.write(speaker + "これでレッスン修了です")
            st.write(speaker +  message["content"])

    st.write(speaker + "お疲れ様でした！")

