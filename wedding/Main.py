
from main import create_app
from main.extention import socketio
app=create_app()
if __name__ == "__main__":
# ngrok http 2000
  # app.run(host='0.0.0.0', port=2000)
  socketio.run(app, host='0.0.0.0', port=2000, debug=True)