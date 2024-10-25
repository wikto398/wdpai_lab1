// requests.js

// Function to send GET request
async function sendGetRequest() {
    const url = `http://localhost:8000`; // Assumes the server is running on localhost:8000
    try {
        const response = await fetch(url);
        const data = await response.json();
        const employeeContainer = document.getElementsByClassName("employee-list")[0];
        employeeContainer.innerHTML = "";
        for (let i = 0; i < data["users"].length; i++) {
            const employee = data["users"][i];
            const newEmployee = document.createElement("div");
            newEmployee.className = "employee";
            newEmployee.dataset.id = employee["id"];
            const innerDiv = document.createElement("div");
            const employeeName = document.createElement("p");
            employeeName.className = "employee-name";
            employeeName.innerHTML = `${employee["first_name"]} ${employee["last_name"]}`;
            const employeeRole = document.createElement("p");
            employeeRole.className = "employee-role";
            employeeRole.innerHTML = employee["role"];
            innerDiv.appendChild(employeeName);
            innerDiv.appendChild(employeeRole);
            const deleteBtn = document.createElement("div");
            deleteBtn.className = "delete-btn";
            deleteBtn.innerHTML = "🗑️";
            deleteBtn.addEventListener("click", () => {
                sendDeleteRequest(employee);
            });
            newEmployee.appendChild(innerDiv);
            newEmployee.appendChild(deleteBtn);
            employeeContainer.appendChild(newEmployee);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to send POST request
async function sendPostRequest() {
    const first_name = document.getElementById("first-name").value;
    const last_name = document.getElementById("last-name").value;
    const role = document.getElementById("role").value;
    const data = { first_name: first_name, last_name: last_name, role: role };
    try {
        const response = await fetch("http://localhost:8000/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        const responseData = await response.json();
        console.log(responseData);
        if (response.status === 200) {
            sendGetRequest();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function sendDeleteRequest(employee) {
    const data = { first_name: employee["first_name"], last_name: employee["last_name"], role: employee["role"], id: employee["id"] };
    try {
        const response = await fetch("http://localhost:8000/", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        const responseData = await response.json();
        console.log(responseData);
        if (response.status === 200) {
            sendGetRequest();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    sendGetRequest();
    document.getElementsByClassName("form")[0].addEventListener("submit", () => {
    event.preventDefault();
    sendPostRequest();});
});