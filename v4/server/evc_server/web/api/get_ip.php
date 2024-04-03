<?php
echo GetClientIP(true);

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


GetClientIP();
?>
