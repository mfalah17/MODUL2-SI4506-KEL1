from flask import Flask, jsonify, send_file
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Konfigurasi koneksi ke database MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'SI4506_STUDIO'
app.config['MYSQL_PORT'] = 3307

# Inisialisasi koneksi MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def root():
    return 'Hello, World!'

@app.route('/movies', methods=['GET'])
def movies():
    # Membuat kursor untuk koneksi database
    cur = mysql.connection.cursor()

    # Melakukan kueri untuk mengambil semua data dari tabel movies
    cur.execute("SELECT * FROM movies")

    # Mengambil semua hasil kueri
    rv = cur.fetchall()

    # Menutup kursor
    cur.close()

    # Membuat daftar kosong untuk menyimpan semua data film
    movies_list = []

    # Meloopi setiap baris hasil kueri dan menambahkannya ke daftar
    for movie in rv:
        # Mengekstrak setiap atribut film, termasuk is_premium
        movie_id, title, description, release_year, duration, genre, rating, video_file, thumbnail, is_premium = movie

        # Membuat kamus untuk menyimpan atribut film
        movie_data = {
            'movie_id': movie_id,
            'title': title,
            'release_year': release_year,
            'genre': genre,
            'video_file': video_file,
            'thumbnail': thumbnail,
            'is_premium': is_premium
        }

        # Menambahkan data film ke daftar
        movies_list.append(movie_data)

    # Mengonversi daftar film menjadi respons JSON
    json_response = jsonify(movies_list)

    return json_response

@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie(movie_id):
    # Membuat kursor untuk koneksi database
    cur = mysql.connection.cursor()

    # Melakukan kueri untuk mengambil data film berdasarkan ID
    cur.execute("SELECT * FROM movies WHERE movie_id = %s", (movie_id,))

    # Mengambil hasil kueri
    movie = cur.fetchone()  # Menggunakan fetchone() karena mengambil satu baris

    # Menutup kursor setelah selesai digunakan
    cur.close()
    
    # Memeriksa apakah film ditemukan
    if movie:
        movie_id, title, description, release_year, duration, genre, rating, video_file, thumbnail, is_premium = movie
        
        # Membuat dictionary dengan data film
        movie_data = {
            'movie_id': movie_id,
            'title': title,
            'description': description,
            'release_year': release_year,
            'duration': duration,  # Mengubah timedelta ke total detik jika diperlukan
            'genre': genre,
            'rating': rating,
            'video_file': video_file,
            'thumbnail': thumbnail,
            'is_premium': is_premium
        }

        # Mengembalikan hasil dalam format yang sesuai
        return jsonify(movie_data)
    else:
        # Jika film tidak ditemukan, mengembalikan respons 404 Not Found
        return jsonify({'error': 'Movie not found'}), 404

@app.route('/thumbnail/<path:filename>')
def get_thumbnail(filename):
    cur = mysql.connection.cursor()

    # Melakukan kueri untuk mengambil nama file gambar berdasarkan nama file yang diberikan
    cur.execute("SELECT thumbnail FROM movies WHERE thumbnail = %s", (filename,))
    
    result = cur.fetchone()
    
    cur.close()
    
    if not result:
        return "Thumbnail not found", 404
    
    thumbnail_filename = result[0]

    # Tentukan path ke gambar
    image_path = f"/Users/nandanugraha/Documents/MICROSERVICES/python-flask/thumbnail/{thumbnail_filename}"

    # Mengirimkan file gambar sebagai respons HTTP
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
