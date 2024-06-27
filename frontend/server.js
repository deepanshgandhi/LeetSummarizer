import express from 'express';
import fetch from 'node-fetch';
import cors from 'cors';
import bodyParser from 'body-parser';
import fs from 'fs';

const app = express();
const port = 3000;

app.use(express.json());
app.use(cors());

app.use(bodyParser.json());

function normalizeNewlines(text) {
    return text.replace(/\r\n/g, '\n').replace(/\r/g, '\n').replace(/\u00A0/g, ' ');
}

app.post('/proxy', async (req, res) => {
    try {
        console.log("Before API request:");

        const body = req.body;
        const normalizedBody = normalizeNewlines(JSON.stringify(body, null, 2));
        fs.writeFileSync('normalizedBody.json', normalizedBody);
        console.log("Request body:", normalizedBody);

        const response = await fetch('https://leet-summarizer-server-zznx.vercel.app/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: normalizedBody
        });

        console.log("-----------------------------------------------------");

        if (!response.ok) {
            throw new Error('Failed to fetch data from upstream server');
        }

        const data = await response.json();
        console.log("Response data:", data);
        res.json(data);
    } catch (error) {
        console.error('Error fetching data:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

app.listen(port, () => {
    console.log(`Proxy server running on port ${port}`);
});