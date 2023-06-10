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

if ($username && $password){
    $sql = "select * from register where username = '$username' and password='$password'";
    $result = mysqli_query($con,$sql);
    $rows=mysqli_num_rows($result);
    if($rows){
          header("refresh:0;url=../sniffer.html");
          exit;
    }else{
     echo "
        <script type='text/javascript'>
            alert('username or password is wrong!');
         </script>
         ";
     echo "
       <script>
           setTimeout(function(){window.location.href='../login.html
     ";
    }

}else{
     echo "
        <script type='text/javascript'>
             alert('username or password is empty!');
        </script>
        ";
     echo "
        <script>
           setTimeout(function(){window.location.href='../login.html';},100);
        </script>";
}


mysqli_close($con);
?>