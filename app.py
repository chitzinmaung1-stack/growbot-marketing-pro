import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# အရင် Agent 1 မှာ သုံးခဲ့တဲ့ Google API Key ကိုပဲ ပြန်သုံးပါမယ်
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route('/')
def home():
    return "GrowBot Marketing Pro is Running!"

@app.route('/create-post', methods=['POST'])
def create_post():
    data = request.get_json()
    topic = data.get('topic', 'AI in Business')
    
    # CEO ပေးထားတဲ့ Personality အတိုင်း AI နည်းပညာရဲ့ အကျိုးကျေးဇူးတွေကို အသားပေးထားပါတယ်
    system_instruction = """
    မင်းက GrowBot Agency ရဲ့ 'Marketing Pro' ဖြစ်တယ်။ 
    မင်းရဲ့ ရည်ရွယ်ချက်က လုပ်ငန်းရှင်တွေ AI ကို မဖြစ်မနေ သုံးချင်လာအောင် ဆွဲဆောင်တဲ့ Facebook Post တွေ ရေးပေးဖို့ ဖြစ်တယ်။

    **ရေးသားရမည့် မူဝါဒများ:**
    - AI ဟာ လူသားတွေအတွက် အကောင်းဆုံး 'လက်ရုံး' ဖြစ်ပြီး ဝန်ထမ်းစရိတ်ထက် အဆပေါင်းများစွာ သက်သာကြောင်း အသားပေးပါ။
    - ၂၄ နာရီ အလုပ်လုပ်နိုင်လို့ အလုပ်ပိုတွင်ကျယ်ကြောင်း ဖော်ပြပါ။
    - GrowBot Agency ဟာ SME နဲ့ Online Shop တွေအတွက် အကောင်းဆုံး Partner ဖြစ်ကြောင်း သိရှိစေရမယ်။

    **Format:**
    ၁။ ဆွဲဆောင်မှုရှိသော Facebook Post (မြန်မာလို)။
    ၂။ အဲဒီ Post နဲ့ လိုက်ဖက်မည့် Image Generation Prompt (အင်္ဂလိပ်လို)။
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nခေါင်းစဉ်: {topic}"}]}]
    }

    try:
        response = requests.post(url, json=payload)
        result = response.json()
        content = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"status": "success", "post_content": content})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
