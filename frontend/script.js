const API_BASE_URL = 'http://localhost:5000';
let currentLanguage = 'english';

// DOM Elements
const healthForm = document.getElementById('healthForm');
const formSection = document.getElementById('formSection');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const submitBtn = document.getElementById('submitBtn');
const newReportBtn = document.getElementById('newReportBtn');
const englishBtn = document.getElementById('englishBtn');
const gujaratiBtn = document.getElementById('gujaratiBtn');

// Event Listeners
healthForm.addEventListener('submit', handleFormSubmit);
newReportBtn.addEventListener('click', showForm);
englishBtn.addEventListener('click', () => setLanguage('english'));
gujaratiBtn.addEventListener('click', () => setLanguage('gujarati'));

// Language Toggle
function setLanguage(language) {
    currentLanguage = language;
    
    if (language === 'english') {
        englishBtn.classList.add('active');
        gujaratiBtn.classList.remove('active');
    } else {
        gujaratiBtn.classList.add('active');
        englishBtn.classList.remove('active');
    }
}

// Form Submit Handler
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Hide error message
    errorMessage.style.display = 'none';
    
    // Get form data
    const formData = {
        gender: document.getElementById('gender').value,
        age: parseInt(document.getElementById('age').value),
        height: parseFloat(document.getElementById('height').value),
        weight: parseFloat(document.getElementById('weight').value),
        language: currentLanguage
    };
    
    // Validate form data
    if (!validateFormData(formData)) {
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/health-report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display results
            displayResults(data);
        } else {
            // Show error
            showError(data.error || 'Failed to generate health report. Please try again.');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Connection error. Please make sure the server is running.');
    } finally {
        setLoadingState(false);
    }
}

// Validate Form Data
function validateFormData(data) {
    if (!data.gender) {
        showError('Please select your gender');
        return false;
    }
    
    if (data.age < 1 || data.age > 100) {
        showError('Age must be between 1 and 100 years');
        return false;
    }
    
    if (data.height < 30 || data.height > 250) {
        showError('Height must be between 30 and 250 cm');
        return false;
    }
    
    if (data.weight < 5 || data.weight > 200) {
        showError('Weight must be between 5 and 200 kg');
        return false;
    }
    
    return true;
}

// Display Results
function displayResults(data) {
    // Hide form and show results
    formSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Animate health score
    animateHealthScore(data.health_score);
    
    // Display BMI
    document.getElementById('bmiValue').textContent = data.bmi.toFixed(1);
    document.getElementById('bmiCategory').textContent = data.bmi_category;
    
    // Color code BMI category
    const bmiCategoryElement = document.getElementById('bmiCategory');
    if (data.bmi_category === 'Normal weight') {
        bmiCategoryElement.style.color = '#4CAF50';
    } else if (data.bmi_category === 'Underweight' || data.bmi_category === 'Overweight') {
        bmiCategoryElement.style.color = '#FF9800';
    } else {
        bmiCategoryElement.style.color = '#F44336';
    }
    
    // Display recommendations
    displayRecommendations(data.recommendations);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Animate Health Score
function animateHealthScore(targetScore) {
    const scoreValueElement = document.getElementById('scoreValue');
    const scoreCircle = document.getElementById('scoreCircle');
    const circumference = 2 * Math.PI * 90; // radius = 90
    
    let currentScore = 0;
    const duration = 2000; // 2 seconds
    const increment = targetScore / (duration / 16); // 60 FPS
    
    const animation = setInterval(() => {
        currentScore += increment;
        
        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(animation);
        }
        
        // Update score text
        scoreValueElement.textContent = Math.round(currentScore);
        
        // Update circle
        const offset = circumference - (currentScore / 100) * circumference;
        scoreCircle.style.strokeDashoffset = offset;
        
        // Change color based on score
        if (currentScore >= 80) {
            scoreCircle.style.stroke = '#4CAF50'; // Green
        } else if (currentScore >= 60) {
            scoreCircle.style.stroke = '#FF9800'; // Orange
        } else {
            scoreCircle.style.stroke = '#F44336'; // Red
        }
    }, 16);
}

// Display Recommendations
function displayRecommendations(recommendations) {
    const recommendationsElement = document.getElementById('recommendations');
    recommendationsElement.innerHTML = formatRecommendations(recommendations);
}

// Format Recommendations
function formatRecommendations(text) {
    // Add some basic HTML formatting to make it more readable
    let formatted = text
        .replace(/\*\*(.*?)\*\*/g, '$1') // Bold text
        .replace(/\n\n/g, '') // Double line breaks
        .replace(/\n/g, ''); // Single line breaks
    
    return `${formatted}`;
}

// Show Form
function showForm() {
    formSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorMessage.style.display = 'none';
    
    // Reset form
    healthForm.reset();
    
    // Scroll to form
    formSection.scrollIntoView({ behavior: 'smooth' });
}

// Show Error
function showError(message) {
    const errorText = document.getElementById('errorText');
    errorText.textContent = message;
    errorMessage.style.display = 'block';
    
    // Scroll to error
    errorMessage.scrollIntoView({ behavior: 'smooth' });
    
    // Hide after 5 seconds
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000);
}

// Set Loading State
function setLoadingState(isLoading) {
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        submitBtn.disabled = true;
    } else {
        btnText.style.display = 'inline-block';
        btnLoader.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Initialize app
console.log('Health Chatbot initialized');
console.log(`API Base URL: ${API_BASE_URL}`);