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
                    <div class="container">
                        <div class="tabs">
                    
                            <div class="tabby-tab">
                                <input type="radio" id="tab-1" name="tabby-tabs" checked>
                                <label for="tab-1"> 배포할 런타임 환경 관리 (e.g. 도커이미지) </label>
                                <div class="tabby-content">
                                    <iframe src="http://evc.re.kr:20080/grafana/d/faf2bff2-f918-4544-b0e2-0216659dae35/00-evc-user-container?orgId=1&kiosk" width=100% height=100%> </iframe>
                                </div>
                            </div>  
                                    
                                
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