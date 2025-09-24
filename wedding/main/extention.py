from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask_socketio import SocketIO
cred = credentials.Certificate(r'C:\Users\yizhen\PersonalAnalys\wedding-photo-c5d0b-firebase-adminsdk-fbsvc-ae6f6fd811.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': "wedding-photo-c5d0b.firebasestorage.app"  # 這行要用你 Firebase Storage 上的 bucket 名稱
})

db = firestore.client()
bucket = storage.bucket()
# 不要在正式上線時用 *，建議改成明確的域名。
socketio = SocketIO(cors_allowed_origins=["http://127.0.0.1:2000", "http://localhost:2000"])