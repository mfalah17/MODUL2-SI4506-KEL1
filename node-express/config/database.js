const mysql = require('mysql');

// Buat koneksi pool ke basis data MySQL
const pool = mysql.createPool({
    connectionLimit: 10,
    host: '127.0.0.1', // atau 'localhost'
    port: 3307,
    user: 'root',
    password: '',
    database: 'SI4506_STUDIO'
  });
  

// Ekspor pool koneksi
module.exports = pool;
