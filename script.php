<?php
error_reporting(E_ALL);
ini_set('display_errors', '1');
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve the input values from the form
    $input1 = $_POST["input1"];
    $input2 = $_POST["input2"];
    $input3 = $_POST["input3"];

    // Call the Python script with the input values as parameters
    $pythonScript = "main.py";
    $command = "python3 $pythonScript $input1 $input2 $input3";
    
    // Execute the Python script
    exec($command, $output, $returnCode);

    // Check if the Python script executed successfully
    if ($returnCode === 0) {
        // Display the output from the Python script
        foreach ($output as $line) {
            echo $line . "<br>";
        }
    } else {
        echo "Error executing Python script.";
    }
}
?>

