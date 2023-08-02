<?php
define("DB_SERVER", "db");
define("DB_USERNAME", "evc");
define("DB_PASSWORD", "evc");
define("DB_NAME", "evc");
define("DB_PORT", 3300);

# Connection
$link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_PORT);

# Check connection
if (!$link) {
  die("Connection failed: " . mysqli_connect_error());
}
