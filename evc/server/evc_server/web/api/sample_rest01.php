<?php

// 헤더 설정
header("Content-Type: application/json");

// JSON 데이터 생성
$data = [
    "name" => "John Doe",
    "age" => 30,
    "address" => "Seoul, South Korea"
];

// JSON 데이터 반환
echo json_encode($data);

?>