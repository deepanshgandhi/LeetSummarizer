document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    // Dummy Questions
    const questions = [
        { id: 1, title: 'Two Sum', summary: 'Find two numbers that add up to a target value.' },
        { id: 2, title: 'Add Two Numbers', summary: 'Add two numbers represented by linked lists.' },
    ];

    const questionsList = document.getElementById('questions-list');
    const summaryPopup = document.getElementById('summary-popup');
    const summaryContent = document.getElementById('summary-content');
    const closeSummaryButton = document.getElementById('close-summary');

    console.log('questions:', questions);

    if (!questionsList) {
        console.error('questions-list element not found');
        return;
    }

    questions.forEach(question => {
        const listItem = document.createElement('li');
        listItem.textContent = question.title;
        listItem.dataset.summary = question.summary;
        listItem.addEventListener('click', function() {
            summaryContent.textContent = this.dataset.summary;
            summaryPopup.classList.add('visible');
        });
        questionsList.appendChild(listItem);
    });

    closeSummaryButton.addEventListener('click', function() {
        summaryPopup.classList.remove('visible');
    });
});
