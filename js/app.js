const express = require('express');
const { exec } = require('child_process');
const app = express();

app.use(express.json());

// 🚨 Command Injection
app.get('/ping', (req, res) => {
    const host = req.query.host;

    exec(`ping -c 1 ${host}`, (err, stdout, stderr) => {
        res.send(stdout);
    });
});

// 🚨 SQL Injection (simulated)
app.get('/user', (req, res) => {
    const id = req.query.id;

    const query = "SELECT * FROM users WHERE id = " + id;
    console.log("Executing query:", query);

    res.send("User data");
});



// 🚨 eval usage (RCE risk)
app.post('/run', (req, res) => {
    const code = req.body.code;

    const result = eval(code);  // ⚠️ Very dangerous
    res.send(result.toString());
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});
