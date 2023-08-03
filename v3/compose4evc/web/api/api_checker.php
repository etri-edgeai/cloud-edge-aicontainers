<?php
$file = "data.json";
$json_data = json_decode(file_get_contents($file));
// $data = [ 'a', 'b', 'c' ]; /** whatever you're serializing **/;
header('Content-Type: application/json; charset=utf-8');
echo json_encode($json_data);