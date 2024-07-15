from openai import OpenAI
import streamlit as st
import time

assistant_id = st.secrets["assistant_id"]
thread_id = st.secrets["thread_id"]

with st.sidebar:
    st.link_button("더 많은 정보 보러가기", "https://quick-log.com/")

    iframe_html = """<iframe src="https://ads-partners.coupang.com/widgets.html?id=791259&template=banner&trackingCode=AF1061869&subId=&width=300&height=250" width="300" height="250" frameborder="0" scrolling="no" referrerpolicy="unsafe-url" browsingtopics></iframe>"""
    st.markdown(iframe_html, unsafe_allow_html=True)
    st.info("이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")
    
    openai_api_key = st.text_input("OpenAI API KEY", type="password")
    client = OpenAI(api_key=openai_api_key)
    thread_id = st.text_input("Thread ID", value=thread_id)

    thread_make_btn = st.button("Create a new thread")
    if thread_make_btn:
        #스레드 생성
        thread = client.beta.threads.create()
        thread_id = thread.id
        st.subheader(thread_id)

st.title("My ChatBot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "성을 입력 해 주세요. 이름을 지어드립니다!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


prompt = st.chat_input()
if prompt:
    # client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    response = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=prompt)

    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    
    # assistant_content = response.choices[0].message.content
    thread_messages = client.beta.threads.messages.list(thread_id)
    assistant_content = thread_messages.data[0].content[0].text.value

    st.session_state.messages.append({"role": "assistant", "content":assistant_content})
    st.chat_message("assistant").write(assistant_content)

    # print(st.session_state.messages)
