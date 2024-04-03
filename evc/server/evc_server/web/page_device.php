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
                                <label for="tab-1">Edge Monitoring</label>
                                <div class="tabby-content">
                                    
                                    <iframe src="http://evc.re.kr:20080/grafana/d/ac02df67-cfd6-42b3-9683-4930f78d485e/demo01-device-management?orgId=1&refresh=5s&theme=dark" width = 100% height=100%> </iframe>
                                    
                                    
                                    <!--
                                    <a href="http://ketiabcs.iptime.org:39080/d/sP0nIDTVz/rpi-6402?orgId=1&refresh=5s&from=1687109419697&to=1687131019697&theme=dark" target="_blank"> 모니터링 UI</a>
                                    <iframe src="http://evc.re.kr:28004/docs" width=100% height=100%> </iframe>
                                    -->
                                </div>
                            </div>  
                                   
                                    
                    
                            <div class="tabby-tab">
                                <input type="radio" id="tab-2" name="tabby-tabs">
                                <label for="tab-2">User APIKEY</label>
                                <div class="tabby-content">
                                    <h7><font color = 'black'> 
                                        Your APIKEY is 
                                            <font color='orange'> <b> <?= htmlspecialchars($_SESSION["user_apikey"]); ?> </b> </font>
                                        .</br>
                                        Please keep the APIKEY carefully. <br/>
APIKEY is important for device management, builing cluster, and model distribution. </br>
                                    </font> </h7>
                                </div>
                            </div>
                                    
                            <div class="tabby-tab">
                                <input type="radio" id="tab-3" name="tabby-tabs">
                                <label for="tab-3">Add New Device</label>
                                <div class="tabby-content">

                                  <p> <font color = "black"> 😊 1. EVC를 통해 서비스 하려는 에지장치(edge device)에 터미널로 진입합니다.</font> </p>


                                  <p> <font color = "black"> 😊 2. 아래 명령어를 관리자 권한(sudo 권한)으로 실행하여 sshd 서버를 비롯한 필수 패키지를 설치하고, EVC가 제공하는 공개키를 에지장치에 등록합니다.</font> </p>

                                  <blockquote><p> <font color = "blue"> $ wget http://evc.re.kr/new.sh -O new.sh</font> </p></blockquote>
                                  <blockquote><p> <font color = "blue"> $ bash new.sh </font> </p></blockquote>


                                  <p> <font color = "black"> 😊 3. 에지 장치를 EVC에 등록하기 위한 설정을 수행합니다.</font> </p>

                                  <blockquote><p> <font color = "blue"> $ wget http://evc.re.kr/join.sh -O join.sh</font> </p></blockquote>
                                  <blockquote><p> <font color = "blue"> $ bash join.sh </font> </p></blockquote>

                                  <font color = "gray" size=1>                     
            📌 주의 및 참고 : 
            EVC와 연동하기 위해서는 적절한 사용자 계정이 있어야 합니다.
            단, 사용자 계정의 권한 설정은 매우 신중해야 합니다.
            에지 디바이스의 특정 사용자 계정이 정상적으로 EVC에 등록되면, EVC는 사용자 계정이 가진 시스템 권한 만큼 에지 디바이스를 제어할 수 있습니다.
            예컨데, 에지 디바이스의 root 권한을 가진 사용자 정보를 EVC에 제공한다면, EVC는 에지 디바이스의 root 권한을 위임 받게 됩니다. 혹은 일반 권한을 가진 사용자 정보를 EVC에 제공한다면, EVC는 시스템을 최신 상태로 업데이트 하거나 필요한 패키지를 설치하지 못할 수 있습니다.
            따라서 어떤 권한을 EVC에 제공할지는 EVC 프레임워크 기술을 사용하려는 사용자의 선택에 달려 있습니다.
            시스템을 제어할 수 있는 권한이 강할수록 EVC는 다양한 기능을 제공하고 사용자는 편리하게 자신의 에지 디바이스를 클러스터 구성원으로 활용할 수 있습니다. 다만 에지 디바이스를 등록한 사용자 입장에서는 시스템의 보안 측면에서 염려도 커질 수 있습니다.
            반대로 보안을 우려하여 제한된 권한을 가진 사용자 정보를 제공한다면, 그 만큼 사용상의 제한이 따르게 됩니다. 📌

                                      </font>

                                </div>
                            </div>   

                            <!--
                            <div class="tabby-tab">
                                <input type="radio" id="tab-4" name="tabby-tabs">
                                <label for="tab-4">List of Edges</label>
                                <div class="tabby-content">

                                    <iframe src=http://evc.re.kr:20080/grafana/d/adddbbaa-6906-4b82-aff6-d308f9825c0a/evc-user-devices?orgId=1&var-user_apikey=<?=htmlspecialchars($_SESSION["user_apikey"]);?>&kiosk width=100% height=100%> </iframe>

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
