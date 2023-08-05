<?php
include('./lib/functions.php');
header('content-type: application/json');

print('hi01 <br/>');

if ($_SERVER['REQUEST_METHOD'] == "GET") {

    print('hi02 <br/>');
    if (isset($_GET['id'])) {
        print('hi03a <br/>');
        $id =  $_GET['id'];
        $json = get_single_user_info($id);
        if (empty($json))
            header("HTTP/1.1 404 Not Found");
        echo json_encode($json);
    } else {
        print('hi03b <br/>');
        $json = get_all_user_list();
        print('hi03c <br/>');
        echo json_encode($json);
        print('hi03d <br/>');
    }
}


if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $data = json_decode(file_get_contents('php://input'), true);

    $name = $data['name'];
    $email = $data['email'];

    $json = add_user_info($name, $email);
    echo json_encode($json);
}

if ($_SERVER['REQUEST_METHOD'] == "PUT") {
    $data = json_decode(file_get_contents('php://input'), true);

    $id = $data['id'];
    $name = $data['name'];
    $email = $data['email'];

    $json = update_user_info($id, $name, $email);
    echo json_encode($json);
}

if ($_SERVER['REQUEST_METHOD'] == "DELETE") {
    $data = json_decode(file_get_contents('php://input'), true);

    $id = $data['id'];

    $json = delete_user_info($id);
    echo json_encode($json);
}
