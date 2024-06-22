const express = require('express')
const bodyParser = require('body-parser');
const app = express()
const port = 3000

app.use(bodyParser.json());


app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.post('/upload', (req, res) => {
    const data = req.body;
    
    res.send(data.question)
  })

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})