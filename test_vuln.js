/**
 * test-vuln.js
 * -------------------------------------------------------
 * DROP THIS FILE into your repo and open a PR to dev.
 * CodeQL will fire on every function below.
 *
 * Expected alerts (all CRITICAL):
 *   js/sql-injection          → getUser()
 *   js/command-injection      → ping()
 *   js/path-traversal         → readFile()
 *   js/code-injection         → calculate()
 *   js/reflected-xss          → search()
 * -------------------------------------------------------
 */

const express  = require('express');
const mysql    = require('mysql2');
const fs       = require('fs');
const { exec } = require('child_process');
const app      = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const db = mysql.createConnection({
  host: 'localhost', user: 'root', password: 'pass', database: 'app'
});

// CRITICAL — js/sql-injection
// Attacker sends: username = ' OR '1'='1' --
app.get('/user', (req, res) => {
  const username = req.query.username;
  const query = "SELECT * FROM users WHERE username = '" + username + "'";
  db.query(query, (err, rows) => res.json(rows));
});

// CRITICAL — js/command-injection
// Attacker sends: host = 127.0.0.1; cat /etc/passwd
app.get('/ping', (req, res) => {
  const host = req.query.host;
  exec(`ping -c 1 ${host}`, (err, stdout) => res.send(stdout));
});

// CRITICAL — js/path-traversal
// Attacker sends: file = ../../../../etc/shadow
app.get('/file', (req, res) => {
  const file = req.query.file;
  fs.readFile('/var/uploads/' + file, 'utf8', (err, data) => res.send(data));
});

// CRITICAL — js/code-injection
// Attacker sends: expr = process.env
app.post('/calc', (req, res) => {
  const result = eval(req.body.expr);
  res.json({ result });
});

// CRITICAL — js/reflected-xss
// Attacker sends: q = <script>alert(document.cookie)</script>
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${req.query.q}</h1>`);
});

app.listen(3000);
