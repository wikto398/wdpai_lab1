// requests.js

// Function to send GET request
function sendGetRequest() {
    const input = document.getElementById("getInputField").value;
    const url = `http://localhost:8000/${input}`; // Assumes the server is running on localhost:8000

    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById("getResponse").textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => console.error('Error:', error));
}

// Function to send POST request
function sendPostRequest() {
    const name = document.getElementById("postNameField").value;
    const data = {
        name: name
    };

    fetch("http://localhost:8000/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("postResponse").textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Error:', error));
}
