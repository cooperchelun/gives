from flask import Flask
from google import genai
from google.genai import types

app = Flask(__name__)

# 在全域（函式外面）建立 Client 物件，只初始化一次即可，不用每次初始化
client = genai.Client()

chat = client.chats.create(model='gemini-3.5-flash')

@app.route("/AI")
def AI():
    # 每次使用者拜訪該路徑時，直接使用全域的 client 呼叫模型
    response = client.models.generate_content(
            model='gemini-3.5-flash', 
            contents=req["queryResult"]["queryText"],
            config=ai_config,
        )

    if response.text:
        info = response.text
    else:
        info = "抱歉，我現在無法生成回應，請稍後再試。"

    return make_response(jsonify({"fulfillmentText": info}))

@app.route("/webhook7", methods=["POST"])
def webhook7():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "rateChoice"):
        print("hi")
    elif (action == "input.unknown"):
        instruction_text = (
            "你是一個熱心且知識豐富的專業智慧助理。"
            "對於使用者的提問，請回覆重點的關鍵字，不要重述問題。"         
        )


        ai_config = types.GenerateContentConfig(
            max_output_tokens=500, 
            system_instruction=instruction_text
        )

    return make_response(jsonify({"fulfillmentText": info}))


@app.route('/ask', methods=['GET', 'POST']) 
def ask():
    if request.method == "POST":
        user_prompt = request.form.get('prompt', '')
        if not user_prompt:
            return "請輸入內容", 400
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=user_prompt,
            )
            return response.text
        except Exception as e:
            return f"發生錯誤: {str(e)}", 500

    else:    
        # 當使用者直接打開網頁 (GET) 時，顯示輸入框畫面
        return render_template("ask.html")
