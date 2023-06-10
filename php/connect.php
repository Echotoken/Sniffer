<?php
  $json_data = json_decode(file_get_contents('../configuration.json'), true);

  $port = $json_data["database"]["port"];
  $server = $json_data["database"]["server"];
  $db_username = $json_data["database"]["username"];
  $db_password = $json_data["database"]["password"];
  $database = $json_data["database"]["database"];

  $con = mysqli_connect($server, $db_username, $db_password, $database, $port);
  mysqli_set_charset($con,'UTF8');   
  if (mysqli_connect_errno($con))
  { 
      echo  mysqli_connect_error(); 
  }
  else{
    // echo 'connect successfully!';
  }
?>