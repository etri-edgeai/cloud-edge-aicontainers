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
        <table style="text-align:center; border:none; width: 100%; height: 100vh; ">
            <tr>
                <?php include 'body_header.php'; ?>
            </tr>
            
            <tr>
                <?php include 'body_navi.php'; ?>

                
                <td style="background-color:#222325; color:white; text-align:left">
                    <div style='width:100%; height:100%'>
                    <iframe src="http://evc.re.kr/chatbot" width=100% height=100%> </iframe>
                    </div>
                    <!--
                    <div class="container">
                        <div class="tabs">

                            <div class="tabby-tab">
                                <input type="radio" id="tab-1" name="tabby-tabs" checked>
                                <label for="tab-1"> reserved </label>
                                <div class="tabby-content">
                                    <iframe src="http://evc.re.kr/chatbot" width=100% height=100%> </iframe>
                                </div>
                            </div>
                                    
                            
                        </div>
                    </div>
                    -->
                </td>   
            </tr>
                    
            <tr>
                <?php include 'body_footer.php'; ?>
            </tr>
        </table>
    </body>
</html>
