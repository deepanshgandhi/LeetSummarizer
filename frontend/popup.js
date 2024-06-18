document.addEventListener('DOMContentLoaded', () => {
    chrome.runtime.sendMessage({ type: 'getScrapedData' }, (response) => {
        if (response) {
            document.getElementById('title').textContent = response.title || 'N/A';
            document.getElementById('description').innerHTML = response.description || 'N/A';
            document.getElementById('problemUrl').textContent = response.problemUrl || 'N/A';
            document.getElementById('user').textContent = response.user || 'N/A';
        } else {
            console.error('No scraped data found.');
        }
    });
});
