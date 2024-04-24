import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import requests

# 假設這是存儲在某個地方的聊天歷史數據
chat_history = {
    "History1": {
        "messages": [
            {"role": "assistant", "content": "Hello, how can I help?"},
            {"role": "user", "content": "What is the weather today?"},
            {"role": "assistant", "content": "Today is a sunny day.", "source": ["今天的天氣如下：現在天氣：輕雨，攝氏 30 度。最高溫度：31 度。最低溫度：22 度。日出時間：上午 5:24。日落時間：下午 6:20。"]},
        ],
        "model": "gpt-3.5-turbo",
        "databases": ["Database 1"]
	},
    "History2": {
		"messages": [
			{"role": "assistant", "content": "Hello, how can I help?"},
			{"role": "user", "content": "Can you book a flight for me?"},
			{"role": "assistant", "content": "Sure, where would you like to go?"}
		],
        "model": "gpt-3.5-turbo",
        "databases": ["Database 2"]
	},
    "History3": {
		"messages": [
			{"role": "assistant", "content": "Hello, how can I help?"},
			{"role": "user", "content": "What's the currency rate for EUR to USD?"},
			{"role": "assistant", "content": "As of today, it is 1.13.", "source": ["今天的 歐元 (EUR) 兌 美元 (USD) 匯率為 1 歐元 = 1.07 美元", "https://www.bing.com/search?q=EUR+to+USD+currency+rate&FORM=wndcht&toWww=1&redig=25FDF18430034C909422C59892119F36"]}
		],
        "model": "gpt-3.5-turbo",
        "databases": ["Database 3"]
	},
    "History4": {
		"messages": [
			{"role": "assistant", "content": "Hello, how can I help?"},
			{"role": "user", "content": "I need directions to the nearest hospital."},
			{"role": "assistant", "content": "Here is the map for the nearest hospital.","source": ["臺北市立聯合醫院中興院區：地址：臺北市大同區鄭州路145號電話：02 2552 3234", "西園醫院：地址：臺北市萬華區西園路二段270號電話：02 2307 6968"]}
		],
        "model": "gpt-4",
        "databases": ["Database 1", "Database 2"]
	},
    "History5": {
		"messages": [
			{"role": "assistant", "content": "Hello, how can I help?"},
			{"role": "user", "content": "Can you play some music?"},
			{"role": "assistant", "content": "Playing your favorite playlist now."}
		],
		"model": "Taiwan-LLM-13B-2.0-chat",
		"databases": ["Database 1", "Database 2", "Database 3"]
	}
}

# 假設這是可選擇的助理模型和數據庫來源
assistant_models = ["gpt-3.5-turbo", "gpt-4", "yabi/breeze-7b-instruct-v1_0_q6_k", "jcai/taide-lx-7b-chat:latest", "llama3:latest"]
database_sources = ["Database 1", "Database 2", "Database 3"]

# 登入檢查和處理函數
def check_login(username, password):
    # 這裡應該是你的登入邏輯
    # 如果登入成功，返回 True
    # 這裡我假設任何非空的用戶名和密碼都代表登入成功
    return username != "" and password != ""

def generate_ollama_text(model, prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get('response', '無返回響應。')
    else:
        return f'發生錯誤: {response.status_code}'

# 建立側邊欄並輸入 API Key
with st.sidebar:
	st.header("經濟統計智慧客服")

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
    # 下拉選單來選擇數據庫來源
    default_databases = st.session_state.get('database_choices', database_sources)
    database_choices = st.multiselect(
        "Choose database sources:", 
        database_sources, 
        default=default_databases, 
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
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if "gpt" not in model_choice:
        response = generate_ollama_text(model_choice, prompt)
    else:
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(model=model_choice, messages=st.session_state.messages)
        response = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

    st.session_state.selection_locked = True
