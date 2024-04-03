<?php

// 헤더 설정
header("Content-Type: application/json");

// 데이터베이스 연결
$db = new PDO("mysql:host=localhost;dbname=evc", "root", "");

// 데이터 가져오기
$query = "SELECT * FROM user";
$result = $db->query($query);

// JSON 데이터 생성
$data = [];
foreach ($result as $row) {
    $data[] = [
        "email" => $row["email"],
        "user_apikey" => $row["user_apikey"]
    ];
}

// JSON 데이터 반환
echo json_encode($data);

?>