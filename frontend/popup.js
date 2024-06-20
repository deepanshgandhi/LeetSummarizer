document.addEventListener('DOMContentLoaded', () => {
    const mainPage = document.getElementById('main-page');
    const summaryPage = document.getElementById('summary-page');
    const generateSummaryButton = document.getElementById('generate-summary');
    const backButton = document.getElementById('back-button');

    // Fetch data from local storage and display in the popup
    chrome.storage.local.get(['scrapedData'], (result) => {
        const data = result.scrapedData || {};
        document.getElementById('title').textContent = data.title || 'N/A';
        document.getElementById('description').innerHTML = data.description || 'N/A';
        document.getElementById('problemUrl').textContent = data.problemUrl || 'N/A';
        document.getElementById('user').textContent = data.user || 'N/A';

        // Enable the "Generate Summary" button only if the URL is a problem page
        if (data.problemUrl && data.problemUrl.includes('/description/')) {
            generateSummaryButton.disabled = false;
        } else {
            generateSummaryButton.disabled = true;
        }
    });

    // Add click event listener to "Generate Summary" button
    generateSummaryButton.addEventListener('click', () => {
        chrome.storage.local.get(['scrapedData'], (result) => {
            const data = result.scrapedData || {};
            const submissionsUrl = data.problemUrl.replace('/description/', '/submissions/');
            
            // Redirect to submissions page and scrape the data
            chrome.tabs.create({ url: submissionsUrl }, (tab) => {
                chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo) {
                    if (tabId === tab.id && changeInfo.status === 'complete') {
                        chrome.tabs.sendMessage(tab.id, { type: 'scrapeSubmission' });
                        chrome.tabs.onUpdated.removeListener(listener);
                    }
                });
            });
        });
    });

    // Add click event listener to "Back" button
    backButton.addEventListener('click', () => {
        summaryPage.style.display = 'none';
        mainPage.style.display = 'block';
    });

    // Listen for messages from content script to update the UI with submission data
    chrome.runtime.onMessage.addListener((message) => {
        if (message.type === 'showSubmission') {
            document.getElementById('submittedCode').textContent = message.data.submittedCode || 'No code submitted.';
            mainPage.style.display = 'none';
            summaryPage.style.display = 'block';
        }
    });
});
