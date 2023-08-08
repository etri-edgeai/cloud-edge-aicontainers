<!-- Navigator section -->

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
                <h7 class="my-1">Hello, <?= htmlspecialchars($_SESSION["user_name"]); ?></h7><br/>
                <h7> <br/> </h7>
                <h7 class="my-1">Your API Key : <font color='orange'> <?= htmlspecialchars($_SESSION["user_apikey"]); ?> </font> </h7><br/>
                <h7> <br/> </h7>
                <a href="./logout.php" class="btn btn-primary"> Log Out </a>
            </div>
        </div>
        
        <br/><br/>
        <!-- 메뉴 -->
        <ul class="list-group">   
            <a href='page_device.php' class="list-group-item"> 에지 디바이스 관리 </a>       
            <a href='page_cluster.php' class="list-group-item"> 클러스터 관리 </a>   
            <a href='page_image_registry.php' class="list-group-item"> 컨테이너 이미지 관리</a>  
            <a href='page_model_repository.php' class="list-group-item"> AI 모델 관리</a> 
            <a href='page_chatbot.php' class="list-group-item" style="color:gray-dark"> [참고] 챗 도우미 </a> 
            <a href='page_admin.php' class="list-group-item"> [어드민] 관리자 기능 </a>
            <a href='page_user.php' class="list-group-item"> [TODO] 사용자 정보 수정 </a>
        </ul>

    </div>
</td>
