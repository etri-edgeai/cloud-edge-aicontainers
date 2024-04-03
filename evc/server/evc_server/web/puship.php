<?php

// echo GetClientIP(true);

function GetClientIP($validate = False) {
  $ipkeys = array(
  'REMOTE_ADDR',
  'HTTP_CLIENT_IP',
  'HTTP_X_FORWARDED_FOR',
  'HTTP_X_FORWARDED',
  'HTTP_FORWARDED_FOR',
  'HTTP_FORWARDED',
  'HTTP_X_CLUSTER_CLIENT_IP'
  );

  /*
  Now we check each key against $_SERVER if containing such value
  */
  $ip = array();
  foreach ($ipkeys as $keyword) {
    if (isset($_SERVER[$keyword])) {
      if ($validate) {
        if (ValidatePublicIP($_SERVER[$keyword])) {
          $ip[] = $_SERVER[$keyword];
        }
      }
      else{
        $ip[] = $_SERVER[$keyword];
      }
    }
  }

  $ip = ( empty($ip) ? 'Unknown' : implode(", ", $ip) );
  return $ip;
}

function ValidatePublicIP($ip){
  if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
    return true;
  }
  else {
    return false;
  }
}

//--------------------------------------------------------
// 사용 예시
//
//  curl http://evc.re.kr:20080/puship.php?hostname=macos
//
//

$hostname = $_GET['hostname'];
$temperature = $_GET['temperature'];
$cpuclock = $_GET['cpuclock'];
$mem = $_GET['mem'];
$json_str = $_GET['json_str'];

$accessed_ip = GetClientIP();
print( $accessed_ip.' ' );


# Include connection
require_once "./config_log.php";

$sql = "INSERT INTO data (ip, hostname, temperature, cpuclock, mem, json_str) VALUES ('{$accessed_ip}', '{$hostname}', '{$temperature}', '{$cpuclock}', '{$mem}', '{$json_str}')";

$result = mysqli_query($conn, $sql);

if($result === false){
    echo mysqli_error($conn);
}

mysqli_close($conn);

//--------------------------------------------------------
?>
