
const express = require('express');
const app = express();
const port = 5000;

app.get('/', (req, res) => {
  res.send('Painel Admin');
});
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});
app.listen(port, () => {
  console.log(`Admin rodando em http://localhost:${port}`);
});