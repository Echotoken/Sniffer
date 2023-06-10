<?php
include "connect.php";
header("Content-Type: text/html; charset=utf8");

$local_name=$_GET['local_name'];
$filepath1="../local_log/".$local_name.".txt";
unlink($filepath1);
$sql1 = "DELETE FROM local_attack WHERE local_name='$local_name'";
$sql2 = "DELETE FROM local_result WHERE local_name='$local_name'";


if(mysqli_query($con,$sql1) && mysqli_query($con,$sql2))
{
echo "<script>
          setTimeout(function(){window.location.href='history_local.php';},1);
       </script>";
}
else{
}
?>