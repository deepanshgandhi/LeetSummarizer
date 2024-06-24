import express from 'express';
import fetch from 'node-fetch';
import cors from 'cors';

const app = express();
const port = 3000;

app.use(express.json());
app.use(cors());

app.post('/proxy', async (req, res) => {
    try {
        const response = await fetch('http://34.125.6.114:8000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(req.body)
        });

        if (!response.ok) {
            throw new Error('Failed to fetch data from upstream server');
        }

        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error('Error fetching data:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.listen(port, () => {
    console.log(`Proxy server running on port ${port}`);
});
