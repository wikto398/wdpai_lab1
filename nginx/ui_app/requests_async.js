// requests.js

// Function to send GET request
async function sendGetRequest() {
    const input = document.getElementById("getInputField").value;
    const url = `http://localhost:8000/${input}`; // Assumes the server is running on localhost:8000

    try {
        const response = await fetch(url);
        const data = await response.json();
        document.getElementById("getResponse").textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to send POST request
async function sendPostRequest() {
    const name = document.getElementById("postNameField").value;
    const data = { name: name };

    try {
        const response = await fetch("http://localhost:8000/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        const responseData = await response.json();
        document.getElementById("postResponse").textContent = JSON.stringify(responseData, null, 2);
    } catch (error) {
        console.error('Error:', error);
    }
}
