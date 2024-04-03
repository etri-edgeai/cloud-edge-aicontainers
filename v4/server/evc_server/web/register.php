<?php
# Include connection
require_once "./config.php";

# Define variables and initialize with empty values
$user_name_err = $email_err = $password_err = "";
$user_name = $email = $password = "";

# Processing form data when form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    echo('<font color = "white"> post01 </font>');
    
    # Validate user_name
    if (empty(trim($_POST["user_name"]))) {
        $user_name_err = "Please enter a user_name.";
        
        echo('<font color = "white"> post01a </font>');
    } else {
        $user_name = trim($_POST["user_name"]);
        if (!ctype_alnum(str_replace(array("@", "-", "_"), "", $user_name))) {
            $user_name_err = "user_name can only contain letters, numbers and symbols like '@', '_', or '-'.";
            
            echo('<font color = "white"> post01b </font>');
        } else {
            # Prepare a select statement
            $sql = "SELECT id FROM user WHERE user_name = ?";

            if ($stmt = mysqli_prepare($link, $sql)) {
                # Bind variables to the statement as parameters
                mysqli_stmt_bind_param($stmt, "s", $param_user_name);

                # Set parameters
                $param_user_name = $user_name;

                # Execute the prepared statement 
                if (mysqli_stmt_execute($stmt)) {
                    # Store result
                    mysqli_stmt_store_result($stmt);

                    # Check if user_name is already registered
                    if (mysqli_stmt_num_rows($stmt) == 1) {
                        $user_name_err = "This user_name is already registered.";
                    }
                } else {
                    echo "<script>" . "alert('Oops! Something went wrong. Please try again later.')" . "</script>";
                }

                # Close statement 
                mysqli_stmt_close($stmt);
            }
        }
    }
    
    echo('<font color = "white"> post02 </font>');
    
    # Validate email 
    if (empty(trim($_POST["email"]))) {
        $email_err = "Please enter an email address";
    } else {
        $email = filter_var($_POST["email"], FILTER_SANITIZE_EMAIL);
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $email_err = "Please enter a valid email address.";
        } else {
            # Prepare a select statement
            $sql = "SELECT id FROM user WHERE email = ?";

            if ($stmt = mysqli_prepare($link, $sql)) {
                # Bind variables to the statement as parameters
                mysqli_stmt_bind_param($stmt, "s", $param_email);

                # Set parameters
                $param_email = $email;

                # Execute the prepared statement 
                if (mysqli_stmt_execute($stmt)) {
                    # Store result
                    mysqli_stmt_store_result($stmt);

                    # Check if email is already registered
                    if (mysqli_stmt_num_rows($stmt) == 1) {
                        $email_err = "This email is already registered.";
                    }
                } else {
                    echo "<script>" . "alert('Oops! Something went wrong. Please try again later.');" . "</script>";
                }

                # Close statement
                mysqli_stmt_close($stmt);
            }
        }
    }
    
    echo('<font color = "white"> post03 </font>');
    
    # Validate password
    if (empty(trim($_POST["password"]))) {
        $password_err = "Please enter a password.";
    } else {
        $password = trim($_POST["password"]);
        if (strlen($password) < 8) {
            $password_err = "Password must contain at least 8 or more characters.";
        }
    }
    
    
    echo('<font color = "white"> post04 </font>');
    

    # Check input errors before inserting data into database
    if (empty($user_name_err) && empty($email_err) && empty($password_err)) {
        # Prepare an insert statement
        $sql = "INSERT INTO user(user_name, email, password, user_apikey) VALUES (?, ?, ?, ?)";
    
        echo('<font color = "white"> post04a </font>');
    
        if ($stmt = mysqli_prepare($link, $sql)) {

            echo('<font color = "white"> post04b </font>');
            # Set parameters
            $param_user_name = $user_name;
            $param_email = $email;
            $param_password = password_hash($password, PASSWORD_DEFAULT);

            # API KEY 임의 생성 (수정이 필요합니다.), TODO
            $hash = hash('sha256', 'bsbaf');
            $param_user_apikey = $hash;
            
            
            
            # Bind varibales to the prepared statement as parameters
            mysqli_stmt_bind_param($stmt, "ssss", $param_user_name, $param_email, $param_password, $param_user_apikey);

            echo('<font color = "white"> post04c </font>');
    
            # Execute the prepared statement
            if (mysqli_stmt_execute($stmt)) {
                echo "<script>" . "alert('Registeration completed successfully. Login to continue.');" . "</script>";
                echo "<script>" . "window.location.href='./login.php';" . "</script>";
                echo('<font color = "white"> post04d </font>');
                exit;
            } else {
                echo "<script>" . "alert('Oops! Something went wrong. Please try again later.');" . "</script>";
                echo('<font color = "white"> post04e </font>');
            }

    
            # Close statement
            mysqli_stmt_close($stmt);
        }
    }

    
    echo('<font color = "white"> post05 </font>');
    
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
    <title>User login system</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    <link rel="stylesheet" href="./css/main.css">
    <link rel="shortcut icon" href="./img/favicon-16x16.png" type="image/x-icon">
    <script defer src="./js/script.js"></script>
</head>

<body style="background-color:#222325;">
    <div class="container" style="color:white">
        <div class="row min-vh-100 justify-content-center align-items-center">
            <div class="col-lg-5">
                <div class="form-wrap border rounded p-4">
                    <h1>Sign up</h1>
                    <p>Please fill this form to register</p>
                    <!-- form starts here -->
                    <form action="<?= htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post" novalidate>
                        <div class="mb-3">
                            <label for="user_name" class="form-label">user_name</label>
                            <input type="text" class="form-control" name="user_name" id="user_name"
                                value="<?= $user_name; ?>">
                            <small class="text-danger">
                                <?= $user_name_err; ?>
                            </small>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email Address</label>
                            <input type="email" class="form-control" name="email" id="email" value="<?= $email; ?>">
                            <small class="text-danger">
                                <?= $email_err; ?>
                            </small>
                        </div>
                        <div class="mb-2">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" name="password" id="password"
                                value="<?= $password; ?>">
                            <small class="text-danger">
                                <?= $password_err; ?>
                            </small>
                        </div>
                        <div class="mb-3 form-check">
                            <input type="checkbox" class="form-check-input" id="togglePassword">
                            <label for="togglePassword" class="form-check-label">Show Password</label>
                        </div>
                        <div class="mb-3">
                            <input type="submit" class="btn btn-primary form-control" name="submit" value="Sign Up">
                        </div>
                        <p class="mb-0">Already have an account ? <a href="./login.php">Log In</a></p>
                    </form>
                    <!-- form ends here -->
                </div>
            </div>
        </div>
    </div>
</body>

</html>