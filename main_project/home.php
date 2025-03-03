<?php
echo "<!DOCTYPE html>";
echo "<html lang='en'>";
echo "<head>";
echo "<meta charset='UTF-8'>";
echo "<meta name='viewport' content='width=device-width, initial-scale=1.0'>";
echo "<title>Dynamic Selection Form</title>";
echo "<style>";
echo "body {";
echo "    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;";
echo "    background-color: #e9ecef;";
echo "    margin: 0;";
echo "    padding: 20px;";
echo "    display: flex;";
echo "    justify-content: center;";
echo "    align-items: center;";
echo "    height: 100vh;";
echo "}";
echo "form {";
echo "    background: linear-gradient(135deg, #ff7e5f, #feb47b);";
echo "    padding: 30px;";
echo "    border-radius: 12px;";
echo "    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);";
echo "    max-width: 400px;";
echo "    width: 100%;";
echo "    color: #ffffff;";
echo "}";
echo "h2 {";
echo "    margin-bottom: 20px;";
echo "    font-size: 1.75em;";
echo "    text-align: center;";
echo "}";
echo "p {";
echo "    margin-bottom: 10px;";
echo "}";
echo "select, input[type='email'] {";
echo "    width: 100%;";
echo "    padding: 12px;";
echo "    margin-bottom: 15px;";
echo "    border: none;";
echo "    border-radius: 6px;";
echo "    font-size: 1em;";
echo "    color: #333;";
echo "}";
echo "input[type='submit'] {";
echo "    width: 100%;";
echo "    padding: 12px;";
echo "    background-color: #007bff;";
echo "    border: none;";
echo "    border-radius: 6px;";
echo "    font-size: 1.25em;";
echo "    color: white;";
echo "    cursor: pointer;";
echo "    transition: background-color 0.3s ease;";
echo "}";
echo "input[type='submit']:hover {";
echo "    background-color: #0056b3;";
echo "}";
echo "</style>";
echo "</head>";
echo "<body>";

echo '<form method="post" action="model.php">';
echo "<h2>Select Your Preferences</h2>";

function populateDropdown($csvFilePath, $name, $label) {
    if (($CSVfp = fopen($csvFilePath, "r")) !== FALSE) {
        // Skip the header line
        fgetcsv($CSVfp);

        echo "<p>$label</p>";
        echo "<select name='$name'>";
        while (($data = fgetcsv($CSVfp, 1000, ",")) !== FALSE) {
            if (!empty($data)) {
                echo '<option value="' . htmlspecialchars($data[0]) . '">' . htmlspecialchars($data[0]) . '</option>';
            }
        }
        echo "</select>";
        fclose($CSVfp);
    } else {
        echo "<p>Error loading $label options.</p>";
    }
}

// Populate categories dropdown
populateDropdown('categories_input.csv', 'categories', 'Choose a Category');

// Populate sub-categories dropdown
populateDropdown('sub_categories_input.csv', 'sub_categories', 'Choose a Sub-Category');

// Email input field
echo "<p>Enter Your Email</p>";
echo "<input type='email' name='from_email' placeholder='your.email@example.com' required>";

echo '<input type="submit" name="submit" value="Submit">';
echo '</form>';

echo "</body>";
echo "</html>";
?>
