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

    // Add click event listener to "Back" button
    backButton.addEventListener('click', () => {
        summaryPage.style.display = 'none';
        mainPage.style.display = 'block';
    });

    // Listen for messages from content script to update the UI with submission data
    chrome.runtime.onMessage.addListener((message) => {
        if (message.type === 'showSubmission') {
            document.getElementById('submittedCode').innerHTML = message.data.submittedCode || 'No code submitted.';
            document.getElementById('summary').innerHTML = message.data.summary || 'No summary generated.';
            mainPage.style.display = 'none';
            summaryPage.style.display = 'block';
        }
    });
});
