function scrapeLeetCodeData() {
    try {
        const titleElement = document.querySelector('.text-title-large');
        const descriptionElement = document.querySelector('div[data-track-load="description_content"]');
        const userElement = document.querySelector('#web-user-menu > div > div.flex.shrink-0.items-center > a');
        const button = document.querySelector('#headlessui-menu-button-\\:r7\\:');

        if (!titleElement) console.log('Title element not found.');
        if (!descriptionElement) console.log('Description element not found.');
        if (!userElement) console.log('User element not found.');
        if (!button) console.log('Menu button not found.');

        if (titleElement && descriptionElement && userElement) {
            const title = titleElement.textContent.trim();
            const description = descriptionElement.innerHTML.trim();
            const problemUrl = window.location.href;
            const user = userElement.href;
            const question = descriptionElement.textContent.trim();

            const scrapedData = {
                user,
                title,
                description,
                problemUrl,
                question
            };

            // Store scraped data in local storage
            chrome.storage.local.set({ scrapedData }, () => {
                console.log('Scraped data stored successfully:', scrapedData);
            });

            // Send scraped data to background script (optional)
            chrome.runtime.sendMessage({ type: 'scrapedData', data: scrapedData });

            // Close the menu by clicking the button again
            if (button) button.click();
        } else {
            console.error('One or more elements are still missing.');
        }
    } catch (error) {
        console.error('Error scraping data:', error);
    }
}

function scrapeSubmissionData(retries = 5) {
    try {
        const codeContainer = document.querySelector('#editor > div.flex.flex-1.flex-col.overflow-hidden.pb-2 > div.flex-1.overflow-hidden > div > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs-dark');

        if (!codeContainer) {
            console.error('Code container not found.');

            if (retries > 0) {
                setTimeout(() => scrapeSubmissionData(retries - 1), 1000);
            } else {
                console.error('Max retries reached. Code container not found.');
            }
            return;
        }

        let collectedCode = '';
        let lastScrollTop = -1;
        let noMoreContentCounter = 0; // Counter to detect no more content

        function scrollAndCollect(container) {
            // Select all lines of code
            const codeElements = document.querySelectorAll('#editor > div.flex.flex-1.flex-col.overflow-hidden.pb-2 > div.flex-1.overflow-hidden > div > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs-dark > div.lines-content.monaco-editor-background > div.view-lines.monaco-mouse-cursor-text > div.view-line');

            let newContent = false; // Flag to check if new content was added

            codeElements.forEach(codeElement => {
                const codeLine = codeElement.innerText; // innerText preserves spaces and newlines
                if (!collectedCode.includes(codeLine)) { // Check if line is already collected
                    collectedCode += codeLine + '\n';
                    newContent = true;
                }
            });

            // Save the current scroll position
            const currentScrollTop = container.scrollTop;

            // If the scroll position has not changed
            if (currentScrollTop === lastScrollTop) {
                noMoreContentCounter++;
                if (noMoreContentCounter > 2) { 
                    console.log('Collected code:', collectedCode);

                    chrome.storage.local.get(['scrapedData'], (result) => {
                        const data = result.scrapedData || {};
                        data.submittedCode = collectedCode;

                        const postData = {
                            question: data.question,
                            userId: data.user,
                            code: collectedCode
                        };

                        console.log('Posted code:', postData);

                        chrome.storage.local.set({ scrapedData: data }, () => {
                            console.log('Submission data stored successfully:', data);

                            fetch('http://localhost:3000/upload', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(postData)
                            })
                                .then(response => response.json())
                                .then(responseData => {
                                    console.log('POST request successful. Response:', responseData);

                                    data.summary = responseData.summary;

                                    chrome.storage.local.set({ scrapedData: data }, () => {
                                        chrome.runtime.sendMessage({ type: 'showSubmission', data });
                                    });
                                })
                                .catch(error => {
                                    console.error('Error in POST request:', error);
                                });
                        });
                    });

                    return;
                }
            } else {
                noMoreContentCounter = 0;
            }

            lastScrollTop = currentScrollTop;
            container.scrollTop += container.clientHeight;
            setTimeout(() => scrollAndCollect(container), 1000); 
        }
        codeContainer.scrollTop = 0;
        scrollAndCollect(codeContainer);
    } catch (error) {
        console.error('Error scraping submission data:', error);
    }
}

function clickButtonAndScrape() {
    const button = document.querySelector('#headlessui-menu-button-\\:r7\\:');
    if (button) {
        button.click();
        setTimeout(scrapeLeetCodeData, 1000);
    } else {
        console.log('Button not found to expand menu.');
    }
}

function determinePageAndScrape() {
    console.log('Current URL:', window.location.href);
    if (window.location.href.includes('/submissions/')) {
        scrapeSubmissionData();
    } else if (window.location.href.includes('/description/')) {
        clickButtonAndScrape();
    }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('Message received:', message);
    if (message.type === 'scrapeSubmission') {
        scrapeSubmissionData();
    }
});

window.onload = function () {
    setTimeout(determinePageAndScrape, 1000);
    console.log('Window loaded and determinePageAndScrape triggered.');
};
