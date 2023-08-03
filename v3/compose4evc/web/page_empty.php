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
        <?php include 'head.php'; ?>
    </head>

    <body>
        <table width="100%" style="text-align:center; border:none">
            <tr>
                <?php include 'body_header.php'; ?>
            </tr>
            
            <tr>
                <td style="background-color:gray; color:white; width:20%">
                    <?php include 'nav.php'; ?>
                </td>

                <td style="color:white; text-align:left">
                    <div class="container">
                        <div class="tabs">
    
    
                        </div>
                    </div>
                </td>   
            </tr>
                    
            <tr>
                <?php include 'body_footer.php'; ?>
            </tr>
        </table>
    </body>
</html>
