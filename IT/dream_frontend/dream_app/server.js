const express = require('express');
const serveStatic = require("serve-static")
const path = require('path');
app = express();

// Let the server start the frontend
app.use(serveStatic(path.join(__dirname, 'dist')));
app.get(/.*/, function (req, res) {
    res.sendFile(path.join(__dirname, '/dist/index.html'))
})
const port = process.env.PORT || 3000;
app.listen(port);
