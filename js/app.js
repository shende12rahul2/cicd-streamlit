const express = require('express');
const { execFile } = require('child_process');
const app = express();

app.use(express.json());

// ✅ Use env variable
const API_KEY = process.env.API_KEY || "safe-default";

// ✅ Command Injection FIX
app.get('/ping', (req, res) => {
    const host = req.query.host;

    if (!host || !/^[a-zA-Z0-9.]+$/.test(host)) {
        return res.status(400).send("Invalid host");
    }

    execFile('ping', ['-c', '1', host], (err, stdout) => {
        res.send(stdout);
    });
});

// ✅ SQL Injection FIX (example with placeholder)
app.get('/user', (req, res) => {
    const id = req.query.id;

    if (!id || isNaN(id)) {
        return res.status(400).send("Invalid ID");
    }

    const query = "SELECT * FROM users WHERE id = ?";
    console.log("Safe query:", query, id);

    res.send("User data");
});

// ✅ Remove eval
app.post('/run', (req, res) => {
    return res.status(403).send("Code execution disabled");
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});
