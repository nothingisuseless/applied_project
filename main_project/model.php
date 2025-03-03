<?php
if (isset($_POST['submit'])) {
    $category = htmlspecialchars($_POST['categories']);
    $sub_category = htmlspecialchars($_POST['sub_categories']);
	$from_email = htmlspecialchars($_POST['from_email']);
    $ingestion_time = date("Y/m/d h:i:s");

    set_time_limit(0);

    // Validate the email input
    if (!filter_var($from_email, FILTER_VALIDATE_EMAIL)) {
        echo "<html><body><p style='color: #e76f51; text-align: center; font-size: 18px;'>Error: Invalid email format.</p></body></html>";
        exit;
    }

    $data = array($category, $sub_category, $from_email, $ingestion_time);
    $fh = fopen("sample.csv", "a");
    if ($fh === false) {
        echo "<html><body><p style='color: #e76f51; text-align: center; font-size: 18px;'>Error: Unable to write to file.</p></body></html>";
        exit;
    }
    fputcsv($fh, $data);
    fclose($fh);

    // Initial loading screen setup
    echo "<html>";
    echo "<head>";
    echo "<style>";
    echo "body {";
    echo "    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;";
    echo "    background-color: #eef2f3;";
    echo "    display: flex;";
    echo "    justify-content: center;";
    echo "    align-items: center;";
    echo "    height: 100vh;";
    echo "    margin: 0;";
    echo "}";
    echo ".content-box {";
    echo "    background-color: #ffffff;";
    echo "    padding: 30px;";
    echo "    border-radius: 10px;";
    echo "    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);";
    echo "    text-align: center;";
    echo "    max-width: 400px;";
    echo "    width: 100%;";
    echo "}";
    echo "h1 {";
    echo "    color: #2a9d8f;";
    echo "    margin-bottom: 20px;";
    echo "    font-size: 24px;";
    echo "}";
    echo "p {";
    echo "    color: #555;";
    echo "    font-size: 16px;";
    echo "}";
    echo ".spinner {";
    echo "    border: 5px solid #f3f3f3;";
    echo "    border-top: 5px solid #2a9d8f;";
    echo "    border-radius: 50%;";
    echo "    width: 50px;";
    echo "    height: 50px;";
    echo "    animation: spin 1s linear infinite;";
    echo "    margin: 30px auto;";
    echo "}";
    echo "@keyframes spin {";
    echo "    0% { transform: rotate(0deg); }";
    echo "    100% { transform: rotate(360deg); }";
    echo "}";
    echo "</style>";
    echo "</head>";
    echo "<body>";
    echo "<div class='content-box' id='content-box'>";
    echo "<h1>Processing...</h1>";
    echo "<p>Please wait while we process your data.</p>";
    echo "<div class='spinner'></div>";
    echo "</div>";
    echo "</body>";
    echo "</html>";

    // Flush the output buffer to display the loading screen before running the Python script
    ob_flush();
    flush();

    // Execute Python script
    $python_script = 'myscript.py';
    $command = escapeshellcmd("python3 $python_script"); // Use python3 and escape shell command
    exec($command . " 2>&1", $output_array);
    $output = htmlspecialchars(implode("\n", $output_array)); // Ensure output is safe to display

    // Replace the loading screen with the success message
    echo "<script type='text/javascript'>";
    echo "document.getElementById('content-box').innerHTML = \"<h1>Success!</h1><p>Your data has been processed successfully.</p><p>$output</p>\";";
    echo "</script>";

} else {
    echo "<html>";
    echo "<body>";
    echo "<p style='color: #e76f51; text-align: center; font-size: 18px;'>Error: No data submitted.</p>";
    echo "</body>";
    echo "</html>";
}
?>
