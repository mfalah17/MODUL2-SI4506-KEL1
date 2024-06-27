const express = require('express');
const app = express();
const apiRoutes = require('./routes/apiRoutes');

// Menggunakan rute apiRoutes
app.use('/', apiRoutes);

// Menjalankan server
app.listen(3000, () => {
  console.log('Server is running on port 3000');
});