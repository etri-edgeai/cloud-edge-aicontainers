<?php
    
echo('[config.01]');

define("DB_SERVER", "db");
define("DB_USERNAME", "evc");
define("DB_PASSWORD", "evc");
define("DB_NAME", "evc");

echo('[config.02]');

# Connection
$link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);

echo('[config.03]');

# Check connection
if (!$link) {
  die("Connection failed: " . mysqli_connect_error());
}


echo('[config.04]');
