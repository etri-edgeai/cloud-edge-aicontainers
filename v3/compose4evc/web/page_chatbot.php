<?php
# Initialize the session
session_start();

# If user is not logged in then redirect him to login page
if (!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== TRUE) {
  echo "<script>" . "window.location.href='./login.php';" . "</script>";
  exit;
}
?>
    
<!DOCTYPE html>
<html>

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <head>
        <!-- tab ui -->
        <link href="./css/style.css" rel="stylesheet" type="text/css">

        <!-- login -->
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
        <link rel="stylesheet" href="./css/main.css">
        <link rel="shortcut icon" href="./img/favicon-16x16.png" type="image/x-icon">
    </head>

    <body>
        <table width="100%" style="text-align:center; border:none">
            <tr>
                <td colspan="2" style="background-color:lightgrey"> <h2> EVC</h2> </td>
            </tr>
            
            <tr>
                <td style="background-color:gray; color:white; width:20%">
                    <div class="container">
                        <!-- 로그인 인증 -->
                        <div class="alert alert-success my-5">
                            Welcome ! You are now signed in to your account.
                        </div>

                        <!-- User profile -->
                        <div class="row justify-content-center">
                            <div class="col-lg-5 text-center">
                                <img src="./img/blank-avatar.jpg" class="img-fluid rounded" alt="User avatar" width="180">
                                <h4 class="my-4">Hello, <?= htmlspecialchars($_SESSION["username"]); ?></h4>
                                <a href="./logout.php" class="btn btn-primary">Log Out</a>
                            </div>
                        </div>
                        
                        <br/><br/>
                        <!-- 메뉴 -->
                        <ul class="list-group">
                            <li class="list-group-item"> <a href='page_admin.php'> [관리자 UI] </a> </li>
                            <li class="list-group-item"> <a href='page_chatbot.php'> [챗봇 도우미] </a> </li>
                            <li class="list-group-item"> <a href='page_newdevice.php'> [신규 에지 장치 등록] </a> </li>
                            <li class="list-group-item"> todo </li>
                            <li class="list-group-item"> todo </li>
                        </ul>
    
                    </div>
                </td>

                <td style="color:white; text-align:left">
                    <div class="container">
                        <div class="tabs">
    
    
                        </div>
                    </div>
                </td>   
            </tr>
                    
            <tr>
                <td colspan="2" style="background-color:#FFCC00"><h5>Footer 영역</h5></td>
            </tr>
        </table>

    </body>
</html>
