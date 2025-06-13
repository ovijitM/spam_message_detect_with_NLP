document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const checkButton = document.getElementById('checkButton');
    const resultSection = document.getElementById('result');
    const errorMessage = document.getElementById('error');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceValue = document.getElementById('confidenceValue');

    checkButton.addEventListener('click', async () => {
        const message = messageInput.value.trim();
        
        resultSection.classList.add('hidden');
        errorMessage.classList.add('hidden');

        if (!message) {
            errorMessage.classList.remove('hidden');
            return;
        }

        try {
            checkButton.disabled = true;
            checkButton.textContent = 'Checking...';

            const response = await fetch('/check_spam', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Something went wrong');
            }

            statusIcon.className = `status-icon ${data.is_spam ? 'spam' : 'ham'}`;
            statusText.textContent = data.is_spam ? 'Spam Detected' : 'Legitimate Message';
            statusText.style.color = data.is_spam ? 'var(--danger-color)' : 'var(--success-color)';

            const confidence = Math.round(data.probability * 100);
            confidenceFill.style.width = `${confidence}%`;
            confidenceValue.textContent = `${confidence}%`;

            resultSection.classList.remove('hidden');

        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        } finally {
            checkButton.disabled = false;
            checkButton.textContent = 'Check Message';
        }
    });

    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            checkButton.click();
        }
    });
}); 