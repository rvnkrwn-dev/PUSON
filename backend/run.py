from app import create_app
from flask_cors import CORS

app = create_app()  # Membuat instance aplikasi Flask dengan konfigurasi yang telah ditentukan

# Konfigurasi CORS untuk membatasi akses hanya ke localhost:3000 dan https://puson.zedis.live
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "https://puson.zedis.live"])

if __name__ == '__main__':  # Memeriksa apakah file ini dijalankan sebagai program utama
    app.run(debug=True)  # Menjalankan aplikasi Flask dalam mode debug untuk pengembangan
