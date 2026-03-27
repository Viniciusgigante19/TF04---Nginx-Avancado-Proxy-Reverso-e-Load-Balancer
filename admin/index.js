const express = require('express');
const app = express();
const path = require('path');
const os = require('os');
const port = 5000;

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'dashboard.html'));
});

app.get('/info', (req, res) => {
  res.json({
    client_ip: req.headers['x-real-ip'] || 'desconhecido',
    server_ip: req.headers['x-instance-ip'] || 'desconhecido',
    server_name: req.headers['x-server-name'] || 'desconhecido',
    server_hostname: os.hostname(),
  });
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.listen(port, () => {
  console.log(`Admin rodando em http://localhost:${port}`);
});