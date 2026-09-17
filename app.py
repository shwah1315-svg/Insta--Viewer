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
    url = f"https://{RAPIDAPI_HOST}/get_ig_user_info.php"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    params = {"username": username}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=12)
        print("API Status Code:", response.status_code)
        
        if response.status_code == 200:
            data = response.json()
            print("API Response:", data)  # Debugging log

            # Extract user data dictionary safely
            user = data.get('user', data)
            if isinstance(user, dict):
                full_name = user.get('full_name') or user.get('username') or username
                profile_pic = user.get('profile_pic_url_hd') or user.get('profile_pic_url') or user.get('hd_profile_pic_url_info', {}).get('url')
                bio = user.get('biography') or user.get('bio') or ''
                followers = user.get('follower_count') or user.get('edge_followed_by', {}).get('count') or 0
                following = user.get('following_count') or user.get('edge_follow', {}).get('count') or 0
                posts = user.get('media_count') or user.get('edge_owner_to_timeline_media', {}).get('count') or 0
                is_verified = user.get('is_verified', False)

                return jsonify({
                    "status": "success",
                    "username": username,
                    "full_name": full_name,
                    "biography": bio,
                    "profile_pic": profile_pic,
                    "followers": followers,
                    "following": following,
                    "posts_count": posts,
                    "is_verified": is_verified
                })
    except Exception as e:
        print("Error:", str(e))

    return jsonify({"status": "error", "message": "Failed to fetch data"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
