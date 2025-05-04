from bottle import route, run

@route('/')
def main():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plant Watering Schedule</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/@tailwindcss/browser@latest"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 10;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.5);
        }
        .modal-content {
            background-color: #fff;
            margin: 10% auto;
            padding: 20px;
            border-radius: 10px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            animation-name: fadeIn;
            animation-duration: 0.4s;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        .input-error {
            border-color: #e53e3e;
        }
        .error-message {
            color: #e53e3e;
            font-size: 0.8rem;
            margin-top: 0.5rem;
            display: none;
        }
        .error-message.active {
            display: block;
        }
    </style>
</head>
<body class="bg-green-100 p-6">
    <h1 class="text-3xl font-bold text-green-600 text-center mb-8">Plant Watering Schedule</h1>

    <div class="max-w-3xl mx-auto bg-white rounded-lg shadow-md p-8">
        <div class="mb-6">
            <button id="addPlantButton" class="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-full shadow-md focus:outline-none focus:shadow-outline">
                Add Plant
            </button>
        </div>

        <div id="plantList" class="space-y-4">
            </div>
    </div>

    <div id="addPlantModal" class="modal">
        <div class="modal-content">
            <h2 class="text-2xl font-semibold text-gray-800 mb-6">Add New Plant</h2>
            <form id="addPlantForm" class="space-y-4">
                <div>
                    <label for="plantName" class="block text-gray-700 text-sm font-bold mb-2">Plant Name:</label>
                    <input type="text" id="plantName" name="plantName" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    <div id="plantNameError" class="error-message"></div>
                </div>
                <div>
                    <label for="plantDescription" class="block text-gray-700 text-sm font-bold mb-2">Plant Description:</label>
                    <textarea id="plantDescription" name="plantDescription" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"></textarea>
                    <div id="plantDescriptionError" class="error-message"></div>
                </div>
                <div>
                    <label for="wateringFrequency" class="block text-gray-700 text-sm font-bold mb-2">Watering Frequency (days):</label>
                    <input type="number" id="wateringFrequency" name="wateringFrequency" min="1" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    <div id="wateringFrequencyError" class="error-message"></div>
                </div>
                <div>
                    <label for="wateringAmount" class="block text-gray-700 text-sm font-bold mb-2">Watering Amount (ml):</label>
                    <input type="number" id="wateringAmount" name="wateringAmount" min="1" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    <div id="wateringAmountError" class="error-message"></div>
                </div>
                <div class="flex justify-end">
                    <button type="button" id="cancelAddPlant" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded-full shadow-md focus:outline-none focus:shadow-outline mr-2">
                        Cancel
                    </button>
                    <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-full shadow-md focus:outline-none focus:shadow-outline">
                        Add Plant
                    </button>
                </div>
            </form>
        </div>
    </div>

    <script>
        const addPlantButton = document.getElementById("addPlantButton");
        const addPlantModal = document.getElementById("addPlantModal");
        const cancelAddPlantButton = document.getElementById("cancelAddPlant");
        const addPlantForm = document.getElementById("addPlantForm");
        const plantList = document.getElementById("plantList");

        let plants = [];

        if (localStorage.getItem("plants")) {
            plants = JSON.parse(localStorage.getItem("plants"));
        }

        function calculateNextWateringDate(lastWateringDate, wateringFrequency) {
            const date = new Date(lastWateringDate);
            date.setDate(date.getDate() + wateringFrequency);
            return date.toLocaleDateString();
        }

        function addPlant(newPlant) {
            plants.push(newPlant);
            localStorage.setItem("plants", JSON.stringify(plants));
            renderPlants();
        }

        function markPlantWatered(index) {
            plants[index].lastWateringDate = new Date().toLocaleDateString();
            plants[index].nextWateringDate = calculateNextWateringDate(plants[index].lastWateringDate, plants[index].wateringFrequency);
            localStorage.setItem("plants", JSON.stringify(plants));
            renderPlants();
        }

        function deletePlant(index) {
            plants.splice(index, 1);
            localStorage.setItem("plants", JSON.stringify(plants));
            renderPlants();
        }

        function renderPlants() {
            plantList.innerHTML = "";
            plants.forEach((plant, index) => {
                const plantCard = document.createElement("div");
                plantCard.classList.add("bg-white", "rounded-lg", "shadow-md", "p-6", "flex", "justify-between", "items-start");

                const plantInfo = document.createElement("div");
                plantInfo.classList.add("space-y-2");
                plantInfo.innerHTML = `
                    <h3 class="text-xl font-semibold text-green-600">${plant.name}</h3>
                    <p class="text-gray-700">${plant.description}</p>
                    <p class="text-gray-500 text-sm">Watering Frequency: ${plant.wateringFrequency} days</p>
                    <p class="text-gray-500 text-sm">Watering Amount: ${plant.wateringAmount} ml</p>
                    <p class="text-gray-500 text-sm">Last Watering Date: ${plant.lastWateringDate}</p>
                    <p class="text-gray-500 text-sm">Next Watering Date: ${plant.nextWateringDate}</p>
                `;

                const actionsDiv = document.createElement("div");
                actionsDiv.classList.add("space-y-2", "flex", "flex-col", "items-end");

                const waterButton = document.createElement("button");
                waterButton.textContent = "Watered";
                waterButton.className = "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full shadow-md focus:outline-none focus:shadow-outline text-sm";
                waterButton.addEventListener("click", () => {
                    markPlantWatered(index);
                });

                const deleteButton = document.createElement("button");
                deleteButton.textContent = "Delete";
                deleteButton.className = "bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-full shadow-md focus:outline-none focus:shadow-outline text-sm";
                deleteButton.addEventListener("click", () => {
                    deletePlant(index);
                });

                actionsDiv.appendChild(waterButton);
                actionsDiv.appendChild(deleteButton);
                plantCard.appendChild(plantInfo);
                plantCard.appendChild(actionsDiv);
                plantList.appendChild(plantCard);
            });
        }

        addPlantButton.addEventListener("click", () => {
            addPlantModal.style.display = "block";
        });

        cancelAddPlantButton.addEventListener("click", () => {
            addPlantModal.style.display = "none";
        });

        window.addEventListener("click", (event) => {
            if (event.target === addPlantModal) {
                addPlantModal.style.display = "none";
            }
        });

        addPlantForm.addEventListener("submit", (event) => {
            event.preventDefault();

            let hasErrors = false;

            const plantName = document.getElementById("plantName").value.trim();
            const plantDescription = document.getElementById("plantDescription").value.trim();
            const wateringFrequency = document.getElementById("wateringFrequency").value.trim();
            const wateringAmount = document.getElementById("wateringAmount").value.trim();

            document.getElementById("plantNameError").classList.remove("active");
            document.getElementById("plantDescriptionError").classList.remove("active");
            document.getElementById("wateringFrequencyError").classList.remove("active");
            document.getElementById("wateringAmountError").classList.remove("active");

            if (plantName === "") {
                document.getElementById("plantNameError").textContent = "Please enter plant name";
                document.getElementById("plantNameError").classList.add("active");
                hasErrors = true;
            }

            if (plantDescription === "") {
                document.getElementById("plantDescriptionError").textContent = "Please enter plant description";
                document.getElementById("plantDescriptionError").classList.add("active");
                hasErrors = true;
            }

            if (wateringFrequency === "" || isNaN(wateringFrequency) || parseInt(wateringFrequency) <= 0) {
                document.getElementById("wateringFrequencyError").textContent = "Please enter a valid watering frequency";
                document.getElementById("wateringFrequencyError").classList.add("active");
                hasErrors = true;
            }

            if (wateringAmount === "" || isNaN(wateringAmount) || parseInt(wateringAmount) <= 0) {
                document.getElementById("wateringAmountError").textContent = "Please enter a valid watering amount";
                document.getElementById("wateringAmountError").classList.add("active");
                hasErrors = true;
            }

            if (hasErrors) {
                return;
            }

            const newPlant = {
                name: plantName,
                description: plantDescription,
                wateringFrequency: parseInt(wateringFrequency),
                wateringAmount: parseInt(wateringAmount),
                lastWateringDate: new Date().toLocaleDateString(),
                nextWateringDate: calculateNextWateringDate(new Date().toLocaleDateString(), parseInt(wateringFrequency)),
            };

            addPlant(newPlant);
            addPlantModal.style.display = "none";
            addPlantForm.reset();
        });

        renderPlants();
    </script>
</body>
</html>

        '''

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
