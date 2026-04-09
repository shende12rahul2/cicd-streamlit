/**
 * vulnerable-app.js
 * ---------------------------------------------------------
 * DEMO FILE — intentional critical security vulnerabilities
 * for CodeQL detection testing.
 * DO NOT deploy or use in any real environment.
 * ---------------------------------------------------------
 *
 * CodeQL rules that WILL fire on this file:
 *   js/sql-injection               (critical)
 *   js/reflected-xss               (critical)
 *   js/code-injection              (critical)
 *   js/path-traversal              (critical)
 *   js/hardcoded-credentials       (critical)
 *   js/command-injection           (critical)
 */

const express    = require('express');
const mysql      = require('mysql2');
const fs         = require('fs');
const { exec }   = require('child_process');
const app        = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ─── VULNERABILITY 1: Hardcoded credentials ──────────────────────────────────
// CodeQL: js/hardcoded-credentials
// The password and secret are embedded directly in source code.
const DB_CONFIG = {
  host:     'localhost',
  user:     'root',
  password: 'SuperSecret123!',      // ← hardcoded credential
  database: 'production_db',
};
const JWT_SECRET = 'my_jwt_secret_key_never_change'; // ← hardcoded secret

const db = mysql.createConnection(DB_CONFIG);

// ─── VULNERABILITY 2: SQL Injection ──────────────────────────────────────────
// CodeQL: js/sql-injection
// User-supplied input is concatenated directly into a SQL query string.
// An attacker can send: username = ' OR '1'='1' --
app.get('/user', (req, res) => {
  const username = req.query.username;

  // VULNERABLE — unsanitised user input flows directly into SQL
  const query = "SELECT * FROM users WHERE username = '" + username + "'";

  db.query(query, (err, results) => {
    if (err) return res.status(500).send(err.message);
    res.json(results);
  });
});

// ─── VULNERABILITY 3: Reflected Cross-Site Scripting (XSS) ───────────────────
// CodeQL: js/reflected-xss
// User input is written back to the HTTP response without encoding.
// An attacker can inject: <script>document.cookie</script>
app.get('/search', (req, res) => {
  const searchTerm = req.query.q;

  // VULNERABLE — raw user input reflected into HTML response
  res.send(`
    <html>
      <body>
        <h1>Search results for: ${searchTerm}</h1>
      </body>
    </html>
  `);
});

// ─── VULNERABILITY 4: Code Injection via eval() ──────────────────────────────
// CodeQL: js/code-injection
// Arbitrary JavaScript sent by the client is executed on the server.
app.post('/calculate', (req, res) => {
  const expression = req.body.expression;

  // VULNERABLE — eval() on untrusted input gives full code execution
  const result = eval(expression);
  res.json({ result });
});

// ─── VULNERABILITY 5: Path Traversal ─────────────────────────────────────────
// CodeQL: js/path-traversal
// A user-controlled filename is used in a filesystem read without validation.
// An attacker can request: filename = ../../../../etc/passwd
app.get('/file', (req, res) => {
  const filename = req.query.filename;

  // VULNERABLE — no normalisation or containment check
  const filePath = '/var/app/uploads/' + filename;

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) return res.status(404).send('File not found');
    res.send(data);
  });
});

// ─── VULNERABILITY 6: Command Injection ──────────────────────────────────────
// CodeQL: js/command-injection
// User input is passed directly to a shell command.
// An attacker can send: host = 127.0.0.1; cat /etc/shadow
app.get('/ping', (req, res) => {
  const host = req.query.host;

  // VULNERABLE — shell=true + unsanitised input = arbitrary command execution
  exec(`ping -c 1 ${host}`, (err, stdout, stderr) => {
    if (err) return res.status(500).send(stderr);
    res.send(stdout);
  });
});

app.listen(3000, () => console.log('Running on port 3000'));
