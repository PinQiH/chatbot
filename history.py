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