function scrapeLeetCodeData() {
    try {
        const titleElement = document.querySelector('.text-title-large');
        const descriptionElement = document.querySelector('div[data-track-load="description_content"]');
        const userElement = document.querySelector('#web-user-menu > div > div.flex.shrink-0.items-center > a');
        // const submittedCode = document.querySelector('#editor > div.flex.flex-1.flex-col.overflow-hidden.pb-2 > div.flex-1.overflow-hidden > div > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs-dark > div.lines-content.monaco-editor-background > div.view-lines.monaco-mouse-cursor-text');

        if (!titleElement) console.log('Title element not found.');
        if (!descriptionElement) console.log('Description element not found.');
        if (!userElement) console.log('User element not found.');

        if (titleElement && descriptionElement && userElement) {
            const title = titleElement.textContent.trim();
            const description = descriptionElement.innerHTML.trim();
            const problemUrl = window.location.href;
            const user = userElement.href;

            const scrapedData = {
                user,
                title,
                description,
                problemUrl
            };

            // Send scraped data to background script
            chrome.runtime.sendMessage({ type: 'scrapedData', data: scrapedData });

            // Close the navbar by clicking the button again
            const button = document.querySelector('#headlessui-menu-button-\\:r7\\:');
            if (button) {
                button.click(); // Simulate a click on the button to close the navbar
            } else {
                console.log('Button not found to close navbar.');
            }
        } else {
            console.error('One or more elements are still missing.');
        }
    } catch (error) {
        console.error('Error scraping data:', error);
    }
}

// Function to click the button to expand the menu and then scrape data
function clickButtonAndScrape() {
    // Click the button to expand menu
    const button = document.querySelector('#headlessui-menu-button-\\:r7\\:');
    if (button) {
        button.click(); // Simulate a click on the button to expand the menu

        // Wait for a brief moment to allow menu to expand (adjust timing as needed)
        setTimeout(scrapeLeetCodeData, 1000); // Call scrape function after delay
    } else {
        console.log('Button not found to expand menu.');
    }
}

// Trigger the process when the window is fully loaded
window.onload = function () {
    setTimeout(clickButtonAndScrape, 1000);
};
