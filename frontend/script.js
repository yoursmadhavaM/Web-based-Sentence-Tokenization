// Sentence Segmentation Tool - Frontend JavaScript

const API_BASE_URL = 'http://localhost:8000';

// DOM elements
const textInput = document.getElementById('text-input');
const languageSelect = document.getElementById('language-select');
const methodSelect = document.getElementById('method-select');
const segmentBtn = document.getElementById('segment-btn');
const outputSection = document.getElementById('output-section');
const errorSection = document.getElementById('error-section');
const sentencesOutput = document.getElementById('sentences-output');
const sentenceCount = document.getElementById('sentence-count');
const methodInfo = document.getElementById('method-info');
const errorMessage = document.getElementById('error-message');

/**
 * Handle sentence segmentation request
 */
async function segmentSentences() {
    const text = textInput.value.trim();
    
    // Validate input
    if (!text) {
        showError('Please enter some text to segment.');
        return;
    }
    
    // Get selected options
    const language = languageSelect.value;
    const method = methodSelect.value;
    
    // Validate method-language combination
    if (method === 'baseline' && language !== 'en') {
        showError('Baseline method only supports English. Please select English or use spaCy method.');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideError();
    hideOutput();
    
    try {
        // Make API request
        const response = await fetch(`${API_BASE_URL}/segment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                language: language,
                method: method
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Segmentation failed');
        }
        
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}. Make sure the backend server is running on ${API_BASE_URL}`);
    } finally {
        setLoadingState(false);
    }
}

/**
 * Display segmentation results
 */
function displayResults(data) {
    const sentences = data.sentences || [];
    const count = data.count || 0;
    const method = data.method || 'unknown';
    const language = data.language || 'en';
    
    // Update info
    sentenceCount.textContent = `${count} sentence${count !== 1 ? 's' : ''} found`;
    methodInfo.textContent = `Method: ${method.toUpperCase()} | Language: ${language.toUpperCase()}`;
    
    // Clear previous output
    sentencesOutput.innerHTML = '';
    
    // Display sentences
    if (sentences.length === 0) {
        sentencesOutput.innerHTML = '<p style="color: #666; text-align: center; padding: 20px;">No sentences found.</p>';
    } else {
        sentences.forEach((sentence, index) => {
            const sentenceElement = document.createElement('div');
            sentenceElement.className = 'sentence-item';
            sentenceElement.innerHTML = `
                <span class="sentence-number">${index + 1}.</span>
                <span class="sentence-text">${escapeHtml(sentence)}</span>
            `;
            sentencesOutput.appendChild(sentenceElement);
        });
    }
    
    // Show output section
    outputSection.style.display = 'block';
    
    // Scroll to output
    outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    outputSection.style.display = 'none';
    
    // Scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

/**
 * Hide output section
 */
function hideOutput() {
    outputSection.style.display = 'none';
}

/**
 * Set loading state
 */
function setLoadingState(loading) {
    segmentBtn.disabled = loading;
    if (loading) {
        segmentBtn.innerHTML = '<span>Processing...</span>';
        document.body.classList.add('loading');
    } else {
        segmentBtn.innerHTML = '<span>Segment Sentences</span>';
        document.body.classList.remove('loading');
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Handle method change - disable non-English languages for baseline
 */
function handleMethodChange() {
    const method = methodSelect.value;
    const language = languageSelect.value;
    
    if (method === 'baseline' && language !== 'en') {
        languageSelect.value = 'en';
        // Show a brief notification
        const notification = document.createElement('div');
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #667eea; color: white; padding: 15px 20px; border-radius: 6px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); z-index: 1000;';
        notification.textContent = 'Baseline method only supports English. Language switched to English.';
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }
}

// Event listeners
segmentBtn.addEventListener('click', segmentSentences);

// Allow Enter key (Ctrl+Enter or Cmd+Enter) to segment
textInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        segmentSentences();
    }
});

// Handle method change
methodSelect.addEventListener('change', handleMethodChange);

// Handle language change when baseline is selected
languageSelect.addEventListener('change', () => {
    if (methodSelect.value === 'baseline' && languageSelect.value !== 'en') {
        handleMethodChange();
    }
});

// Check API health on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✓ Backend API is running');
        }
    } catch (error) {
        console.warn('⚠ Backend API not reachable. Make sure the server is running.');
    }
});
