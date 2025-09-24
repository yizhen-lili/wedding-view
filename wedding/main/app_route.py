from flask import Blueprint,render_template,redirect,url_for,request
import uuid,random
import os
from main.extention import db,bucket,socketio
from flask import flash,jsonify,session
from datetime import datetime
wedding = Blueprint('wedding', __name__ ,url_prefix='/wedding')
photos = []
@wedding.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        image = request.files['image']

        if image:
            if not image.content_type or not image.content_type.startswith('image/'):
                flash('❌ 僅限上傳圖片檔案')
                return redirect('/')
            # 產生唯一檔名
            ext = os.path.splitext(image.filename)[1]  # e.g. ".jpg", ".png"
            filename = f"{uuid.uuid4()}{ext}"
            blob = bucket.blob(f"images/{filename}")
            blob.upload_from_file(image.stream, content_type=image.content_type)
            blob.make_public()  # 讓圖片能用網址存取
            uploaded_at = datetime.utcnow().isoformat()
            photo={                
                'username': username,
                'message': message,
                'image_url': blob.public_url,
                'uploaded_at':uploaded_at

            }
            # 將資料寫入 Firestore
            db.collection('posts').add(photo)

            # 廣播給投影端
            socketio.emit('new_photo', photo, namespace='/slideshow')
            return jsonify({"ok": True, "data": photo})

    else:
            return render_template('upload.html')


@wedding.route('/display')
def display():

    return render_template('display.html')



@wedding.route('/lottery', methods=['GET', 'POST'])
def lottery():
    usernames = set()
    for post in db.collection('posts').select(['username']).stream():
        data = post.to_dict()
        usernames.add(data.get('username'))
    # 產出亂數前端視覺化
    unique_usernames = list(usernames)
    # 結果產出(前端收到submit 才顯示 並檔戲結果)
    winning = random.choice(unique_usernames)
    if request.method=='POST':
        return render_template('winning.html',winning=winning)
    return render_template('lottery.html',unique_usernames=unique_usernames)

@socketio.on("connect", namespace="/slideshow")
# 像是不同路由器
def connect(*args, **kwargs):
    print("投影端連上")
    posts = db.collection('posts').order_by('uploaded_at').stream()
    for doc in posts:
        data = doc.to_dict()
        # 確保 uploaded_at 是字串
        if 'uploaded_at' in data and not isinstance(data['uploaded_at'], str):
            data['uploaded_at'] = data['uploaded_at'].isoformat()
        socketio.emit("new_photo", data, namespace="/slideshow")