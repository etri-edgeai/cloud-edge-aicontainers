<?php
$host = 'localhost';
$user = 'root';
$pass = 'mypass';
 
$conn = mysqli_connect($host, $user, $pass, 3300);
if (!$conn) {
    exit('Connection failed: '.mysqli_connect_error().PHP_EOL);
}
 
echo 'Successful database connection!'.PHP_EOL;