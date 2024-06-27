const pool = require('../config/database');

exports.index = (req, res) => {
    res.send('Hello World');
};

exports.aboutUs = (req, res) => {
    res.send('About Us');
}