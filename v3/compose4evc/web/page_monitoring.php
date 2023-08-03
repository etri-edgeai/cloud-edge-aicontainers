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
                            <div class="tabby-tab">
                            <input type="radio" id="tab-1" name="tabby-tabs" checked>
                            <label for="tab-1">monitoring</label>
                            <div class="tabby-content">

                                <a href="http://ketiabcs.iptime.org:39080/d/sP0nIDTVz/rpi-6402?orgId=1&refresh=5s&from=1687109419697&to=1687131019697&theme=light" target="_blank"> 모니터링 UI</a>
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