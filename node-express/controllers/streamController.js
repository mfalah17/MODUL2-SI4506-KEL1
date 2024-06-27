const pool = require('../config/database');
const path = require('path');


exports.stream = (req, res) => {

    const video_file = req.params.video_file;

    pool.query('SELECT * FROM movies WHERE video_file = ?', [video_file], (error, results) => {
        if (error) {
            console.error(error);
            return res.status(500).json({ error: 'Internal Server Error' });
        }

        if (results.length === 0) {
            return res.status(404).json({ error: 'Video not found' });
        }

        const video_name = results[0]['video_file'];

        // Mengecek jika hasil query tidak kosong
        if (!video_name) {
            return res.status(404).json({ error: 'Video not found' });
        }

        // Membuat path lengkap ke file video
        const videoPath = path.join(__dirname, `../public/stream/${video_name}`);

        // Mengirimkan file video sebagai respons
        res.sendFile(videoPath);
    });

    
}