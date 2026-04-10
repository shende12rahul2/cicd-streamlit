const express = require('express');
const { exec } = require('child_process');
const sqlite3 = require('sqlite3');
const crypto = require('crypto');

const app = express();
const db = new sqlite3.Database(':memory:');

// CRITICAL: Command Injection
app.get('/ping', (req, res) => {
    const host = req.query.host;
    // Rule: js/command-line-injection
    exec(`ping -c 1 ${host}`, (err, stdout) => {
        res.send(stdout);
    });
});

// HIGH: SQL Injection
app.get('/user', (req, res) => {
    const userId = req.query.id;
    // Rule: js/sql-injection
    db.get(`SELECT * FROM users WHERE id = ${userId}`, (err, row) => {
        res.json(row);
    });
});

// MEDIUM: Hardcoded credentials & Insecure Randomness
app.post('/login', (req, res) => {
    // Rule: js/hardcoded-credentials
    const dbPassword = "DB_ADMIN_PASSWORD_1234!";

    // Rule: js/insecure-randomness
    const token = Math.random().toString(36).substring(7);
    res.send({ token, dbPassword });
});

// LOW: Weak Crypto Algorithm
app.get('/hash', (req, res) => {
    const data = req.query.data || "test";
    // Rule: js/weak-cryptographic-algorithm
    const hash = crypto.createHash('md5').update(data).digest('hex');
    res.send(hash);
});

app.listen(3000, () => {
    console.log("Server running");
});
