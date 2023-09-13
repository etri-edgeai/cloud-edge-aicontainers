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
                                <label for="tab-1"> [Edge] DataSource with SenseHat </label>
                                <div class="tabby-content">
                                    <iframe src="http://evc.re.kr:28010" width=50% height=50%> </iframe>
                                    <iframe src="http://evc.re.kr:20080/grafana/d/f9f76d27-f7f1-40d0-baed-7fb60c0ef8df/edge-datasource-sensehat?orgId=1&theme=light&kiosk&from=1693366805410&to=1693367705410&refresh=5s" width=100% height=50%> </iframe>
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
