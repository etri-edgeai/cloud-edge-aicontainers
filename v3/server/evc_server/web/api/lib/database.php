<?php

mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

class Database{
    private static $database_name ='evc';
    private static $database_host = '192.168.1.6';
    private static $database_user = 'evc';
    private static $database_user_password = 'evc';

    private static $connection_status = null;

    public function __construct(){
        die('Init function is not allowed');
    }

    public static function connect()
    {
        if(self::$connection_status == null)
        try{
           self::$connection_status = new PDO('mysql:host='.self::$database_host.';dbname='.self::$database_name.'', self::$database_user, self::$database_user_password);

        }catch(PDOException $e)
        {
            die($e->getMessage());
        }
        return self::$connection_status;
    }
    public static function disconnect()
    {
        self::$connection_status = null;
    }
}

?>
