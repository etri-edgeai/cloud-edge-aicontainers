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
                            <label for="tab-1">EVC Server Status</label>
                            <div class="tabby-content">

                                <iframe
                                    src="http://evc.re.kr:20080/grafana/d/rYdddlPWk/demo02-evc-monitoring?orgId=1&theme=dark&kiosk"
                                    width=100% height=100%> </iframe>
                            </div>
                        </div>

                        <div class="tabby-tab">
                            <input type="radio" id="tab-2" name="tabby-tabs">
                            <label for="tab-2">EVC Prometheus</label>
                            <div class="tabby-content">
                                <iframe src="http://evc.re.kr:29090/" width=100% height=100%> </iframe>
                            </div>
                        </div>


                        <div class="tabby-tab">
                            <input type="radio" id="tab-3" name="tabby-tabs">
                            <label for="tab-3">admin.cmdb</label>
                            <div class="tabby-content">

                                <iframe src="http://evc.re.kr:20080/admin/overview.html" width=100% height=100%> </iframe>

                            </div>
                        </div>

                        <div class="tabby-tab">
                            <input type="radio" id="tab-4" name="tabby-tabs">
                            <label for="tab-4">semaphore</label>
                            <div class="tabby-content">
                                <!-- <iframe src="http://evc.re.kr/semaphore" width=100% height=100%> </iframe> -->
                                <iframe src="http://evc.re.kr:28009" width=100% height=100%> </iframe>
                            </div>
                        </div>

                        <!--
                        <div class="tabby-tab">
                            <input type="radio" id="tab-5" name="tabby-tabs">
                            <label for="tab-5">docker registry</label>
                            <div class="tabby-content">

                                <p><a href="https://deepcase.mynetgear.com:20050/v2/_catalog" target="_blank"> [pass]
                                        Docker Registry Catalog </a></p>

                                <p><a href="https://deepcase.mynetgear.com:20050/v2/python/tags/list" target="_blank">
                                        [pass] Docker Registry tags list </a></p>

                                <p><a href="http://deepcase.mynetgear.com:28083/" target="_blank"> [not yet] Docker
                                        Registry Browser </a></p>

                                <p><a href="http://ketiabcs.iptime.org:39080/d/KTkDshJ4z/registry?orgId=1&from=1687114419389&to=1687136019389&theme=light"
                                        target="_blank"> [not yet] Docker Registry + Grafana </a></p>


                                <p> <a href="https://huggingface.co/facebook" target="_blank"> Model Registry (e.g.
                                        Huggingface)</a></p>
                                <img src='img4doc/model.jpg' width=100%>

                            </div>
                        </div>
                        


                        <div class="tabby-tab">
                            <input type="radio" id="tab-6" name="tabby-tabs">
                            <label for="tab-6">PMA</label>
                            <div class="tabby-content">
                                <p><a href="http://evc.re.kr:20080/pma" target="_blank"> phpmyadmin </a></p>
                            </div>
                        </div>

                                
                        <div class="tabby-tab">
                            <input type="radio" id="tab-7" name="tabby-tabs">
                            <label for="tab-7">Redis</label>
                            <div class="tabby-content">
                                
                                <h5> <font color = 'black'> 
                                    Redis 명령어 : <a href='https://redis.io/commands/'> https://redis.io/commands/ </a>
                                </font> </h5>
                                <h5> <font color = 'black'> 
                                    Redis 명령어 : <a href='https://tgyun615.com/192'> https://tgyun615.com/192 </a>
                                </font> </h5> <br/>
                                <iframe src="http://evc.re.kr:20080/redis/" width=100% height=80%> </iframe>
                            </div>
                        </div>
                        -->

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