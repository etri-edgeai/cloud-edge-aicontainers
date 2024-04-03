<?php
    $db_host = "mariadb";
    $db_user = "evc";
    $db_pass = "evc"; # [주의] 비밀번호 해싱방식을 SHA256 password 인증으로 할 것
    $db_name = "evc";

    $conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
    
    /* DB 연결 확인 */
    if($conn){ 
        echo "Connection established"."<br>"; 
    }
    else{ 
        die( 'Could not connect: ' . mysqli_error($conn) ); 
    }

    // TODO
    
    if($conn){
        mysqli_close($conn);
    }
?>
