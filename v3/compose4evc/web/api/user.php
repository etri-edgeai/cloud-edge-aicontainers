<?php
include('./lib/db_user.php');
header('content-type: application/json');

if ($_SERVER['REQUEST_METHOD'] == "GET") {

    if (isset($_GET['id'])) {
        $id =  $_GET['id'];
        $json = get_single_user_info($id);
        if (empty($json))
            header("HTTP/1.1 404 Not Found");
        echo json_encode($json);
    } else {
        $json = get_all_user_list();
        echo json_encode($json);
    }
}


if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $data = json_decode(file_get_contents('php://input'), true);

    $user_name = $data['user_name'];
    $email = $data['email'];
    $password = $data['password'];

    $json = add_user_info($user_name, $email, $password);
    echo json_encode($json);
}

if ($_SERVER['REQUEST_METHOD'] == "PUT") {
    $data = json_decode(file_get_contents('php://input'), true);

    $id = $data['id'];
    $name = $data['user_name'];
    $email = $data['email'];

    $json = update_user_info($id, $name, $email);
    echo json_encode($json);
}

if ($_SERVER['REQUEST_METHOD'] == "DELETE") {
    $data = json_decode(file_get_contents('php://input'), true);

    echo('hohoho');
    $id = $data['id'];

    $json = delete_user_info($id);
    echo json_encode($json);
}
