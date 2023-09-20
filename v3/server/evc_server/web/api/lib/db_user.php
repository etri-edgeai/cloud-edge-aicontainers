<?php
include 'database.php';

function get_all_user_list()
{
    $pdo = Database::connect();
    $sql = "SELECT * FROM user";

    try {
        $query = $pdo->prepare($sql);
        $query->execute();
        $all_user_info = $query->fetchAll(PDO::FETCH_ASSOC);

    } catch (PDOException $e) {
        print "Error!: " . $e->getMessage() . "<br/>";
        die();
    }

    Database::disconnect();
    return json_encode($all_user_info);
}

function get_single_user_info($id)
{
    $pdo = Database::connect();
    $sql = "SELECT * FROM user where id = {$id} ";

    try {

        $query = $pdo->prepare($sql);
        $query->execute();
        $user_info = $query->fetchAll(PDO::FETCH_ASSOC);

    } catch (PDOException $e) {

        print "Error!: " . $e->getMessage() . "<br/>";
        die();
    }

    Database::disconnect();
    return json_encode($user_info);
}


function add_user_info($user_name, $email, $password)
{
    // echo 'user_name is '.$user_name;
    // echo 'emaile is '.$email;
    
    //echo $password;
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);
    // hash('sha256', $data['password'] );
    
    $pdo = Database::connect();
    $sql = "INSERT INTO user(`user_name`,`email`,`password`) VALUES('{$user_name}', '{$email}', '{$hashed_password}')";
    //echo ($sql);
    $status = [];

    try {
        $query = $pdo->prepare($sql);
        $result = $query->execute();
        if($result)
        {
            $status['message'] = "Data inserted";
        }
        else{
            $status['message'] = "Data is not inserted";
        }

    } catch (PDOException $e) {

        $status['message'] = $e->getMessage(); 
    }

    Database::disconnect();
    return json_encode($status);
}


function update_user_info($id, $user_name, $email)
{
    $pdo = Database::connect();
    $sql = "UPDATE user SET user_name = '{$user_name}', email = '{$email}' where id = '{$id}'";
    $status = [];
    
    echo( $id );
    echo( get_single_user_info($id) );
    
    try {

        $query = $pdo->prepare($sql);
        $result = $query->execute();
        if($result)
        {
            $status['message'] = "Data updated";
        }
        else{
            $status['message'] = "Data is not updated";
        }

    } catch (PDOException $e) {

        $status['message'] = $e->getMessage(); 
    }

    Database::disconnect();
    return $status;
}



function delete_user_info($id)
{
    $pdo = Database::connect();
    $sql ="DELETE FROM user where id = '{$id}'";
    $status = [];

    // echo( $id );
    // echo( get_single_user_info($id) );
    
    try {

        $query = $pdo->prepare($sql);
        $result = $query->execute();
        if($result)
        {
            $status['message'] = "Data deleted";
        }
        else{
            $status['message'] = "Data is not deleted";
        }

    } catch (PDOException $e) {

        $status['message'] = $e->getMessage(); 
    }

    Database::disconnect();
    return $status;
}
