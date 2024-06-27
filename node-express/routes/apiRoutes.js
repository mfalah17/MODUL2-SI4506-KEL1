const express = require('express');
const router = express.Router();
const testController = require('../controllers/testController');
const streamController = require('../controllers/streamController'); 
;

// Rute untuk mengakses endpoint root
router.get('/', testController.index);
router.get('/about', testController.aboutUs);
router.get('/stream/:video_file', streamController.stream);


// Rute untuk menampilkan video


module.exports = router;