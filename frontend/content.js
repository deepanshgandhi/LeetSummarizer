function scrapeLeetCodeData() {
    try {
        const titleElement = document.querySelector('.css-v3d350[data-cy="question-title"]');
        const descriptionElement = document.querySelector('.content__u3I1');

        if (!titleElement) console.log('Title element not found.');
        if (!descriptionElement) console.log('Description element not found.');

        if (titleElement && descriptionElement) {
            const title = titleElement.textContent.trim();
            const description = descriptionElement.innerHTML.trim();
            const problemUrl = window.location.href;
            const user = null; // Set user to null for now

            const scrapedData = {
                user,
                title,
                description,
                problemUrl
            };

            // Send the scraped data to the background script
            chrome.runtime.sendMessage({ type: 'scrapedData', data: scrapedData });
        } else {
            console.error('One or more elements are still missing.');
        }
    } catch (error) {
        console.error('Error scraping data:', error);
    }
}

function waitForContent() {
    const targetNode = document.body;

    if (!targetNode) {
        console.error('Target node not found.');
        return;
    }

    const config = { childList: true, subtree: true, attributes: true, characterData: true };

    const callback = function(mutationsList, observer) {
        console.log('Observing changes...');
        const titleElement = document.querySelector('.css-v3d350[data-cy="question-title"]');
        const descriptionElement = document.querySelector('.content__u3I1');

        if (titleElement && descriptionElement) {
            console.log('Required elements found. Stopping observer.');
            observer.disconnect();
            scrapeLeetCodeData();
            return;
        } else {
            console.log('Elements not found yet. Continuing to observe.');
        }
    };

    const observer = new MutationObserver(callback);
    observer.observe(targetNode, config);

    setTimeout(() => {
        observer.disconnect();
        console.log('Stopped observing after timeout.');
    }, 15000); 
}

window.onload = waitForContent;
