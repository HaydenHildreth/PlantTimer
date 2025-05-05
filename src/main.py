from bottle import route, run

@route('/')
def main():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plant Monitor</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background-color: #f4f7f6;
            color: #333;
            line-height: 1.6;
        }

        .container {
            max-width: 960px;
            margin: 30px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }

        h1 {
            text-align: center;
            color: #5cb85c;
            margin-bottom: 30px;
        }

        h2 {
            color: #337ab7;
            margin-top: 20px;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }

        #plant-list {
            list-style: none;
            padding: 0;
        }

        .plant-item {
            background-color: #fff;
            border: 1px solid #e0e0e0;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .plant-details {
            flex-grow: 1;
        }

        .plant-details strong {
            color: #2e6da4;
        }

        .plant-actions button {
            background-color: #d9534f;
            color: white;
            border: none;
            padding: 8px 12px;
            margin-left: 10px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 0.9em;
            transition: background-color 0.3s ease;
        }

        .plant-actions button:hover {
            background-color: #c9302c;
        }

        .plant-actions button:first-child {
            background-color: #f0ad4e;
        }

        .plant-actions button:first-child:hover {
            background-color: #eea236;
        }

        #add-plant-form, #edit-plant-form {
            margin-top: 30px;
            padding: 20px;
            background-color: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
        }

        #add-plant-form label, #edit-plant-form label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: bold;
        }

        #add-plant-form input[type="text"],
        #add-plant-form input[type="number"],
        #add-plant-form input[type="date"],
        #edit-plant-form input[type="text"],
        #edit-plant-form input[type="number"],
        #edit-plant-form input[type="date"] {
            width: calc(100% - 16px);
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 1em;
        }

        #add-plant-form button, #edit-plant-form button {
            background-color: #5cb85c;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1em;
            transition: background-color 0.3s ease;
            margin-right: 5px;
        }

        #add-plant-form button:hover, #edit-plant-form button:hover {
            background-color: #4cae4c;
        }

        #edit-plant-form {
            display: none; /* Hidden by default */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Plant Monitor</h1>

        <div id="add-plant-form">
            <h2>Add New Plant</h2>
            <label for="new-plant-name">Plant Name:</label>
            <input type="text" id="new-plant-name"><br>

            <label for="new-plant-description">Description:</label>
            <input type="text" id="new-plant-description"><br>

            <label for="new-watering-frequency">Watering Frequency (days):</label>
            <input type="number" id="new-watering-frequency" min="1"><br>

            <label for="new-watering-amount">Watering Amount:</label>
            <input type="text" id="new-watering-amount"><br>

            <label for="new-last-watering-date">Last Watering Date:</label>
            <input type="date" id="new-last-watering-date"><br>

            <button onclick="addPlant()">Add Plant</button>
        </div>

        <div id="edit-plant-form">
            <h2>Edit Plant</h2>
            <input type="hidden" id="edit-plant-index">
            <label for="edit-plant-name">Plant Name:</label>
            <input type="text" id="edit-plant-name"><br>

            <label for="edit-plant-description">Description:</label>
            <input type="text" id="edit-plant-description"><br>

            <label for="edit-watering-frequency">Watering Frequency (days):</label>
            <input type="number" id="edit-watering-frequency" min="1"><br>

            <label for="edit-watering-amount">Watering Amount:</label>
            <input type="text" id="edit-watering-amount"><br>

            <label for="edit-last-watering-date">Last Watering Date:</label>
            <input type="date" id="edit-last-watering-date"><br>

            <button onclick="saveEditedPlant()">Save Changes</button>
            <button onclick="hideEditForm()">Cancel</button>
        </div>

        <ul id="plant-list">
            </ul>
    </div>

    <script>
        let plants = [];

        // Load plants from local storage if available
        const storedPlants = localStorage.getItem('plants');
        if (storedPlants) {
            plants = JSON.parse(storedPlants);
            displayPlants();
        }

        function calculateNextWateringDate(lastWateringDate, frequency) {
            const lastWatering = new Date(lastWateringDate);
            const nextWatering = new Date(lastWatering);
            nextWatering.setDate(lastWatering.getDate() + parseInt(frequency));
            return nextWatering.toLocaleDateString();
        }

        function addPlant() {
            const name = document.getElementById('new-plant-name').value;
            const description = document.getElementById('new-plant-description').value;
            const frequency = document.getElementById('new-watering-frequency').value;
            const amount = document.getElementById('new-watering-amount').value;
            const lastWateringDate = document.getElementById('new-last-watering-date').value;

            if (name && frequency && lastWateringDate) {
                const newPlant = {
                    plantName: name,
                    plantDescription: description,
                    wateringFrequency: frequency,
                    wateringAmount: amount,
                    lastWateringDate: lastWateringDate,
                    nextWateringDate: calculateNextWateringDate(lastWateringDate, frequency)
                };
                plants.push(newPlant);
                savePlants();
                displayPlants();
                clearInputFields();
            } else {
                alert('Please fill in at least the Plant Name, Watering Frequency, and Last Watering Date.');
            }
        }

        function clearInputFields() {
            document.getElementById('new-plant-name').value = '';
            document.getElementById('new-plant-description').value = '';
            document.getElementById('new-watering-frequency').value = '';
            document.getElementById('new-watering-amount').value = '';
            document.getElementById('new-last-watering-date').value = '';
        }

        function displayPlants() {
            const plantList = document.getElementById('plant-list');
            plantList.innerHTML = ''; // Clear the current list

            plants.forEach((plant, index) => {
                const listItem = document.createElement('li');
                listItem.classList.add('plant-item');
                listItem.innerHTML = `
                    <div class="plant-details">
                        <strong>${plant.plantName}</strong><br>
                        ${plant.plantDescription ? plant.plantDescription + '<br>' : ''}
                        Watering Frequency: ${plant.wateringFrequency} days<br>
                        Watering Amount: ${plant.wateringAmount || 'N/A'}<br>
                        Last Watering: ${plant.lastWateringDate}<br>
                        Next Watering: ${plant.nextWateringDate}
                    </div>
                    <div class="plant-actions">
                        <button onclick="editPlant(${index})">Edit</button>
                        <button onclick="deletePlant(${index})">Delete</button>
                    </div>
                `;
                plantList.appendChild(listItem);
            });
        }

        function editPlant(index) {
            const plant = plants[index];
            document.getElementById('edit-plant-index').value = index;
            document.getElementById('edit-plant-name').value = plant.plantName;
            document.getElementById('edit-plant-description').value = plant.plantDescription;
            document.getElementById('edit-watering-frequency').value = plant.wateringFrequency;
            document.getElementById('edit-watering-amount').value = plant.wateringAmount;
            document.getElementById('edit-last-watering-date').value = plant.lastWateringDate;

            document.getElementById('add-plant-form').style.display = 'none';
            document.getElementById('edit-plant-form').style.display = 'block';
        }

        function saveEditedPlant() {
            const index = document.getElementById('edit-plant-index').value;
            const name = document.getElementById('edit-plant-name').value;
            const description = document.getElementById('edit-plant-description').value;
            const frequency = document.getElementById('edit-watering-frequency').value;
            const amount = document.getElementById('edit-watering-amount').value;
            const lastWateringDate = document.getElementById('edit-last-watering-date').value;

            if (name && frequency && lastWateringDate) {
                plants[index] = {
                    plantName: name,
                    plantDescription: description,
                    wateringFrequency: frequency,
                    wateringAmount: amount,
                    lastWateringDate: lastWateringDate,
                    nextWateringDate: calculateNextWateringDate(lastWateringDate, frequency)
                };
                savePlants();
                displayPlants();
                hideEditForm();
            } else {
                alert('Please fill in at least the Plant Name, Watering Frequency, and Last Watering Date.');
            }
        }

        function hideEditForm() {
            document.getElementById('edit-plant-form').style.display = 'none';
            document.getElementById('add-plant-form').style.display = 'block';
        }

        function deletePlant(index) {
            if (confirm('Are you sure you want to delete this plant?')) {
                plants.splice(index, 1);
                savePlants();
                displayPlants();
            }
        }

        function savePlants() {
            localStorage.setItem('plants', JSON.stringify(plants));
        }
    </script>
</body>
</html>
        '''

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
