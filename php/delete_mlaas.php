<?php
include "connect.php";
header("Content-Type: text/html; charset=utf8");

$mlaas_name=$_GET['mlaas_name'];
$filepath1="../mlaas_log/".$mlaas_name.".txt";
unlink($filepath1);
$sql1 = "DELETE FROM mlaas_attack WHERE mlaas_name='$mlaas_name'";
$sql2 = "DELETE FROM mlaas_result WHERE mlaas_name='$mlaas_name'";


if(mysqli_query($con,$sql1) && mysqli_query($con,$sql2))
{
echo "<script>
          setTimeout(function(){window.location.href='history_mlaas.php';},1);
       </script>";
}
else{
}
?>