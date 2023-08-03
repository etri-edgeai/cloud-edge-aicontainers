                    <div class="container">
                        <!-- 로그인 인증 -->
                        <div class="alert alert-success my-5">
                            Welcome ! You are now signed in to your account.
                        </div>

                        <!-- User profile -->
                        <div class="row justify-content-center">
                            <div class="col-lg-5 text-center">
                                <img src="./img/blank-avatar.jpg" class="img-fluid rounded" alt="User avatar" width="180">
                                <h4 class="my-4">Hello, <?= htmlspecialchars($_SESSION["username"]); ?></h4>
                                <a href="./logout.php" class="btn btn-primary">Log Out</a>
                            </div>
                        </div>
                        
                        <br/><br/>
                        <!-- 메뉴 -->
                        <ul class="list-group">
                            <li class="list-group-item"> <a href='page_admin.php'> [관리자 UI] </a> </li>
                            <li class="list-group-item"> <a href='page_chatbot.php'> [챗봇 도우미] </a> </li>
                            <li class="list-group-item"> <a href='page_newdevice.php'> [신규 에지 장치 등록] </a> 
                            <li class="list-group-item"> <a href='page_monitoring.php'> [모니터링] </a> </li>
                            <li class="list-group-item"> todo </li>
                            <li class="list-group-item"> todo </li>
                            <li class="list-group-item"> <a href='page_empty.php'> [EMPTY] </a> 
                        </ul>
    
                    </div>