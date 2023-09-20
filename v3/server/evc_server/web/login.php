<?php
# Initialize session
session_start();

# Check if user is already logged in, If yes then redirect him to index page
if (isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] == TRUE) {
    echo "<script>" . "window.location.href='./'" . "</script>";
    exit;
}

# Include connection
require_once "./config.php";

# Define variables and initialize with empty values
$user_login_err = $user_password_err = $login_err = "";
$user_login = $user_password = "";

# Processing form data when form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty(trim($_POST["user_login"]))) {
        $user_login_err = "Please enter your user_name or an email id.";
    } else {
        $user_login = trim($_POST["user_login"]);
    }

    if (empty(trim($_POST["user_password"]))) {
        $user_password_err = "Please enter your password.";
    } else {
        $user_password = trim($_POST["user_password"]);
    }

    # Validate credentials 
    if (empty($user_login_err) && empty($user_password_err)) {
        # Prepare a select statement
        $sql = "SELECT id, user_name, password, user_apikey FROM user WHERE user_name = ? OR email = ?";

        if ($stmt = mysqli_prepare($link, $sql)) {
            # Bind variables to the statement as parameters
            mysqli_stmt_bind_param($stmt, "ss", $param_user_login, $param_user_login);

            # Set parameters
            $param_user_login = $user_login;
            
            # Execute the statement
            if (mysqli_stmt_execute($stmt)) {
                
                # Store result
                mysqli_stmt_store_result($stmt);

                # Check if user exists, If yes then verify password
                if (mysqli_stmt_num_rows($stmt) == 1) {
                    
                    # Bind values in result to variables
                    mysqli_stmt_bind_result($stmt, $id, $user_name, $hashed_password, $user_apikey);

                    if (mysqli_stmt_fetch($stmt)) {
                        # Check if password is correct
                        if (password_verify($user_password, $hashed_password)) {

                            # Store data in session variables
                            $_SESSION["id"] = $id;
                            $_SESSION["user_name"] = $user_name;
                            $_SESSION["loggedin"] = TRUE;
                            $_SESSION["user_apikey"] = $user_apikey;

                            # Redirect user to index page
                            echo "<script>" . "window.location.href='./'" . "</script>";
                            exit;
                        } else {
                            # If password is incorrect show an error message
                            $login_err = "The email or password you entered is incorrect.";
                        }
                    }
                } else {
                    # If user doesn't exists show an error message
                    $login_err = "Invalid user_name or password.";
                }
            } else {
                echo "<script>" . "alert('Oops! Something went wrong. Please try again later.');" . "</script>";
                echo "<script>" . "window.location.href='./login.php'" . "</script>";
                exit;
            }

            # Close statement
            mysqli_stmt_close($stmt);
        }
    }
    echo ('h09');
    # Close connection
    mysqli_close($link);
}
?>




<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge Vision Cluster : evc.re.kr </title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    <link rel="stylesheet" href="./css/main.css">
    <link rel="shortcut icon" href="./img/favicon-16x16.png" type="image/x-icon">
    <script defer src="./js/script.js"></script>
</head>

<body style="background-color:#222325;">
    <div class="container">
        <div class="row min-vh-100 justify-content-center align-items-center">
            <div class="col-lg-5">
                <?php
                if (!empty($login_err)) {
                    echo "<div class='alert alert-danger'>" . $login_err . "</div>";
                }
                ?>
                <div class="form-wrap border rounded p-4" style='color:white'>
                    <h1>Log In</h1>
                    <h5>클라우드-엣지 연동분석 프레임워크, EVC</h5>
                    <br /><br />
                    <p>Please login to continue </p>
                    <p>developer id and password is <b>
                            <font color='orange'> {id : 'test', pw : 'test'} </font>
                        </b> </p>
                    <!-- form starts here -->
                    <form action="<?= htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post" novalidate>
                        <div class="mb-3">
                            <label for="user_login" class="form-label">Email or user_name</label>
                            <input type="text" class="form-control" name="user_login" id="user_login"
                                value="<?= $user_login; ?>">
                            <small class="text-danger">
                                <?= $user_login_err; ?>
                            </small>
                        </div>
                        <div class="mb-2">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" name="user_password" id="password">
                            <small class="text-danger">
                                <?= $user_password_err; ?>
                            </small>
                        </div>
                        <div class="mb-3 form-check">
                            <input type="checkbox" class="form-check-input" id="togglePassword">
                            <label for="togglePassword" class="form-check-label">Show Password</label>
                        </div>
                        <div class="mb-3">
                            <input type="submit" class="btn btn-primary form-control" name="submit" value="Log In">
                        </div>
                        <p class="mb-0">Don't have an account ? <a href="./register.php">Sign Up</a></p>
                    </form>
                    <!-- form ends here -->
                </div>
            </div>
        </div>
    </div>
</body>

</html>