d<?php
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
                                <label for="tab-1">클러스터 목록</label>
                                <div class="tabby-content">
                                    <iframe src="http://evc.re.kr:20080/grafana/d/f1e4527d-5580-45fe-87f6-088dd3a02e60/00-evc-user-clusters?orgId=1&from=1693428028751&to=1693449628751&kiosk" width=100% height=100%> </iframe>
                                    
                                </div>
                            </div>                


                            <div class="tabby-tab">
                                <input type="radio" id="tab-2" name="tabby-tabs">
                                <label for="tab-2">[todo] 클러스터 생성, 모니터링</label>
                                <div class="tabby-content">
                                    todo
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
