from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__, template_folder='.')

RAPIDAPI_KEY = "a35cfdd1bamshdfb2a0c44650aa1p1bae90jsn701d6190a734"
RAPIDAPI_HOST = "instagram-scraper-stable-api.p.rapidapi.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/profile/<username>')
def get_profile(username):
    username = username.strip().replace('@', '')
    url = "https://instagram-scraper-stable-api.p.rapidapi.com/get_ig_user_id.php"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "content-type": "application/x-www-form-urlencoded"
    }
    
    payload = f"username_or_url={username}"
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            res_data = response.json()
            user = res_data.get('user', res_data)
            
            return jsonify({
                "status": "success",
                "username": user.get('username', username),
                "full_name": user.get('full_name', username),
                "biography": user.get('biography', ''),
                "profile_pic": user.get('profile_pic_url_hd') or user.get('profile_pic_url'),
                "followers": user.get('follower_count', 0),
                "following": user.get('following_count', 0),
                "posts_count": user.get('media_count', 0),
                "is_verified": user.get('is_verified', False)
            })
    except Exception as e:
        pass

    return jsonify({
        "status": "error",
        "message": "Data fetch failed"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
