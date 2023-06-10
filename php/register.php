<?php
session_start();
header("content-type:text/html;charset=utf-8");

$json_data = json_decode(file_get_contents('../configuration.json'), true);

$port = $json_data["database"]["port"];
$server = $json_data["database"]["server"];
$db_username = $json_data["database"]["username"];
$db_password = $json_data["database"]["password"];
$database = $json_data["database"]["database"];

$con = mysqli_connect($server,$db_username,$db_password,$database,$port);
mysqli_Set_charset($con,'utf-8');
if (mysqli_connect_errno($con)) 
{ 
  mysqli_connect_error(); 
}
else{
}
 
$username = $_REQUEST['username'];
$password = $_REQUEST['password'];

$sql_select = "SELECT * FROM register WHERE username = '$username'";
$select = mysqli_query($con,$sql_select);
$num = mysqli_num_rows($select);

if($username == "" || $password == ""){
   echo "
      <script type='text/javascript'>
           alert('username or password is empty!');
      </script>
      ";
   echo "
      <script>
         setTimeout(function(){window.location.href='../register.html';},100);
      </script>";
}
else if($num){
   echo "
      <script type='text/javascript'>
           alert('username is used!');
      </script>
      ";
      echo "
      <script>
         setTimeout(function(){window.location.href='../register.html';},100);
      </script>";
}
else{
    $sql = "INSERT INTO register(username,password) VALUES ('$username','$password')";
    $result = mysqli_query($con,$sql);
    if($result){
          header("refresh:0;url=../login.html");
          exit;
    }else{
     echo "
        <script type='text/javascript'>
            alert('error!');
         </script>
         ";
     echo "
       <script>
           setTimeout(function(){window.location.href='../register.html';},1000);
       </script>
     ";
    }
}

mysqli_close($con);
?>