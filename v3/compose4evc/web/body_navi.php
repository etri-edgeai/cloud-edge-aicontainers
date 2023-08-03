
<td style="background-color:#222325; color:white; width:20%">
    <div class="container">
                        <!-- 로그인 인증 -->
                        <!--
                        <div class="alert alert-success my-5">
                            Welcome !
                        </div>
                        -->

                        <!-- User profile -->
                        <div class="row justify-content-center">
                            <div class="col-lg-7 text-center">
                                <img src="./img/blank-avatar.jpg" class="img-fluid rounded" alt="User avatar" width="180">
                                <h7 class="my-1">Hello, <?= htmlspecialchars($_SESSION["username"]); ?></h7><br/>
    
                                <a href="./logout.php" class="btn btn-primary"> Log Out </a>
                            </div>
                        </div>
                        
                        <br/><br/>
                        <!-- 메뉴 -->
                        <ul class="list-group">    
                          <a href='page_chatbot.php' class="list-group-item" style="color:gray-dark"> 챗 </a>
                          <a href='page_admin.php' class="list-group-item"> 관리자 UI </a>
                          <a href='page_newdevice.php' class="list-group-item"> 신규 에지 </a>
                          <a href='page_monitoring.php' class="list-group-item"> 모니터링 </a>
                          <a href='page_empty.php' class="list-group-item"> todo </a>
                        </ul>
    
    </div>
</td>