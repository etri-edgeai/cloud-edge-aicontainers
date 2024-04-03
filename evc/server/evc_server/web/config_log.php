<?php
define("DB_SERVER", "mariadb");
define("DB_USERNAME", "test");
define("DB_PASSWORD", "test");
define("DB_NAME", "beacon_ip");

# Connection
$conn = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);

# Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
