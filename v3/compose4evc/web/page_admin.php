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
                                <label for="tab-1">admin.cmdb</label>
                                <div class="tabby-content">

                                <iframe src="http://evc.re.kr/admin/overview.html" width=100% height=100%> </iframe>

                                </div>
                            </div>

                            <div class="tabby-tab">
                                <input type="radio" id="tab-2" name="tabby-tabs">
                                <label for="tab-2">semaphore</label>
                                <div class="tabby-content">
                                <iframe src="http://evc.re.kr:23000" width=100% height=100%> </iframe>
                                </div>
                            </div> 


                            <div class="tabby-tab">
                                <input type="radio" id="tab-3" name="tabby-tabs">
                                <label for="tab-3">docker registry</label>
                                <div class="tabby-content">

                                    <p><a href="https://deepcase.mynetgear.com:20050/v2/_catalog" target="_blank"> [pass] Docker Registry Catalog </a></p>

                                    <p><a href="https://deepcase.mynetgear.com:20050/v2/python/tags/list" target="_blank"> [pass] Docker Registry tags list </a></p>

                                    <p><a href="http://deepcase.mynetgear.com:28083/" target="_blank"> [not yet] Docker Registry Browser </a></p>

                                    <p><a href="http://ketiabcs.iptime.org:39080/d/KTkDshJ4z/registry?orgId=1&from=1687114419389&to=1687136019389&theme=light" target="_blank"> [not yet] Docker Registry + Grafana </a></p>


                                            <p> <a href="https://huggingface.co/facebook" target="_blank"> Model Registry (e.g. Huggingface)</a></p>
                                        <img src='img4doc/model.jpg' width=100%>

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