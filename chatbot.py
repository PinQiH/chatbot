import streamlit as st
import matplotlib.pyplot as plt
from history import chat_history
from user import check_login
from model import get_response_from_ollama, get_response_from_openai
from pre_data import setup_vector_store
from database import search_documents

# 假設這是可選擇的助理模型和數據庫來源
assistant_models = ["gpt-3.5-turbo", "gpt-4", "yabi/breeze-7b-instruct-v1_0_q6_k", "jcai/taide-lx-7b-chat:latest", "llama3:latest"]
database_sources = ["None", "NCKUH_Brian", "NCKUH_Gary"]

# Setup the document and vector store
collection_name="summaries"
model_name="thenlper/gte-large"
id_key="doc_id"
retriever = setup_vector_store(collection_name, model_name, id_key)

# 建立側邊欄並輸入 API Key
with st.sidebar:
	st.header("Chatbot")

	if st.button("💬 Start New Chat", key="new_chat"):
			# 清空聊天記錄或執行開啟新聊天的邏輯
			st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
			st.session_state.current_history = "💬 Chatbot"
			if 'model_choice' in st.session_state:
				del st.session_state.model_choice
			if 'database_choices' in st.session_state:
				del st.session_state.database_choices
			st.session_state.selection_locked = False
			st.rerun()

	# 增加登入選項
	# 如果已經登入，顯示用戶名，否則顯示登入表單
	if 'logged_in' in st.session_state and st.session_state.logged_in:
		# 歷史紀錄選單
		with st.expander("📜 History"):
			for history_key in chat_history:
					if st.button(history_key, key=history_key):
						# 恢復訊息和當時的設定
						st.session_state.messages = chat_history[history_key]["messages"]
						st.session_state.current_history = history_key
						st.session_state.model_choice = chat_history[history_key]["model"]
						st.session_state.database_choices = chat_history[history_key]["databases"]

		# 增加使用量設定選項
		with st.expander("📊 Usage Settings"):
			current_usage = 750
			st.write(f"目前使用量: {current_usage} token")
			usage_limit = st.number_input("設定使用量上限", min_value=0, value=1000, step=50, format="%d", key="usage_limit")
			# 創建數據以及標籤
			data = [current_usage, usage_limit - current_usage]
			labels = ['Used Tokens', 'Remaining Tokens']

			# 繪製圓餅圖
			fig, ax = plt.subplots()
			ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
			ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

			# 顯示圓餅圖
			st.pyplot(fig)
			alert_usage = st.checkbox("使用量示警")
			if st.button("Save Usage Settings", key="save_usage"):
					st.write("Save logic goes here")

		with st.expander(f"👤 {st.session_state.username}"):
			st.write("You are logged in.")
			if st.button('Logout'):
				st.session_state.logged_in = False
				st.session_state.username = ''
				st.experimental_rerun()
	else:
		with st.expander("🔐 Login"):
			username = st.text_input("Username")
			password = st.text_input("Password", type="password")
			if st.button("Login", key="login"):
				if check_login(username, password):
					st.session_state.logged_in = True
					st.session_state.username = username
					st.write(f"Welcome {username}!")
					st.experimental_rerun()
				else:
					st.error("Login failed.")
	
	# 增加API key設定選項
	with st.expander("🔑 API Key Settings"):
		openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
		"[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
		if st.button("Save API key Settings", key="save_api"):
				st.write("Save success")
			
# 創建三個並排的列
col1, col2, col3 = st.columns(3)

# 在第一列中放置標題
with col1:
	# 主要內容區
	current_title = st.session_state.get('current_history', '💬Chatbot')
	st.title(current_title)

# 如果已經開始聊天（messages 至少有一條訊息），則禁用選項
disable_selection = "selection_locked" in st.session_state and st.session_state.selection_locked

# 在第二列中放置選擇助理模型的下拉選單
with col2:
    # 下拉選單來選擇助理模型
    default_model = st.session_state.get('model_choice', assistant_models[0])
    model_choice = st.selectbox(
        "Choose an assistant model:", 
        assistant_models, 
        index=assistant_models.index(default_model), 
        disabled=disable_selection
    )

# 在第三列中放置選擇數據庫來源的多選下拉選單
with col3:
    default_database = st.session_state.get('database_sources', database_sources[0])
    # 下拉選單來選擇數據庫來源
    database_choices = st.selectbox(
        "Choose database sources:", 
        database_sources,
        index=database_sources.index(default_database), 
        disabled=disable_selection
    )

# 初始訊息管理
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# 顯示聊天訊息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    if 'source' in msg:
        sources = msg['source']
        for source in sources:
            if "http" in source:
                st.markdown(f"[Source]({source})", unsafe_allow_html=True)
            else:
                st.write(f"Source: {source}")

# 處理新的聊天輸入
if prompt := st.chat_input():
    st.session_state.model_choice = model_choice
    st.session_state.database_choices = database_choices
    st.chat_message("user").write(prompt)

    if database_choices != "None":
        res = search_documents(retriever, prompt, database_choices)
        if res.startswith("No relevant documents found."):
            st.warning(res)
            complete_prompt = prompt  # 如果沒有找到相關文件，則將提示作為完整的提示
        else:
            st.text(res)
            complete_prompt = prompt + "\n\n" + res  # 將找到的文件資訊追加到提示中
    else:
        complete_prompt = prompt 

    st.session_state.messages.append({"role": "user", "content": complete_prompt})
    
    if "gpt" not in model_choice:
	    response = get_response_from_ollama(model_choice, complete_prompt)
    else:
	    if not openai_api_key:
	        st.info("Please add your OpenAI API key to continue.")
	        st.stop()
	    response = get_response_from_openai(openai_api_key, model_choice, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

    st.session_state.selection_locked = True
