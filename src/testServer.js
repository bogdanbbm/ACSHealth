const express = require('express');

const app = express();

app.use(express.static('public'));

app.get('/api/message', (req, res) => {
  res.send('Hello, ACSHealth! fortza dada');
});

app.listen(3000, () => console.log('Server listening on port 3000'));
