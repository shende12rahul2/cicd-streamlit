const express = require('express');
const { exec } = require('child_process');
const sqlite3 = require('sqlite3');
const crypto = require('crypto');

const app = express();
const db = new sqlite3.Database(':memory:');

// CRITICAL: OS Command Injection
app.get('/status', (req, res) => {
    const serverId = req.query.id;
    // Rule: js/command-line-injection
    exec(`cat /var/log/server_${serverId}.log`, (error, stdout) => {
        res.send(stdout);
    });
});

// HIGH: Reflected Cross-Site Scripting (XSS)
app.get('/welcome', (req, res) => {
    const username = req.query.user;
    // Rule: js/reflected-xss
    res.send(`<h1>Welcome back, ${username}!</h1>`);
});

// HIGH: SQL Injection
app.post('/update_profile', (req, res) => {
    const age = req.body.age;
    const userId = req.body.id;
    // Rule: js/sql-injection
    db.run(`UPDATE profiles SET age = ${age} WHERE id = ${userId}`);
    res.send("Profile updated");
});

// MEDIUM: Hardcoded Credentials
function connectToThirdPartyAPI() {
    // Rule: js/hardcoded-credentials
    const STRIPE_API_KEY = "";
    console.log("Connecting with key:", STRIPE_API_KEY);
}

// LOW: Use of a Broken or Risky Cryptographic Algorithm
app.post('/encrypt_data', (req, res) => {
    const dataToEncrypt = req.body.data;
    // Rule: js/weak-cryptographic-algorithm
    const cipher = crypto.createCipheriv('des-ede3-cbc', 'secret_key', 'iv');
    let encrypted = cipher.update(dataToEncrypt, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    res.send(encrypted);
});

app.listen(8080, () => {
    console.log("App listening on port 8080");
});
