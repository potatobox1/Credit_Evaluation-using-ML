function submitForm(event) {
    event.preventDefault()
    const form = document.getElementById('prediction-form');
    const formData = new FormData(form);
    const data = {};
    
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Prediction: ${data.prediction}`;
        document.getElementById('description').innerText = `Description: ${data.description}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error making prediction';
    });
}
document.getElementById('prediction-form').addEventListener('submit', submitForm);
