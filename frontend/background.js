let scrapedData = {};

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'scrapedData') {
        scrapedData = message.data;
        console.log('Scraped data received:', scrapedData);
    }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'getScrapedData') {
        sendResponse(scrapedData);
    }
});
