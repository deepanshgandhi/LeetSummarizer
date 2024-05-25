chrome.runtime.onInstalled.addListener(() => {
    console.log('LeetCode Summarizer extension installed.');
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'fetchQuestions') {
        // Dummy response
        const questions = [
            { id: 1, title: 'Two Sum', summary: 'Find two numbers that add up to a target value.' },
            { id: 2, title: 'Add Two Numbers', summary: 'Add two numbers represented by linked lists.' },
        ];
        sendResponse({ questions });
    }
    return true;
});