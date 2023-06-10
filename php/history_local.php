<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Sniffer-login</title>
    <link rel="stylesheet" href="../css/history_local.css">
    <link rel="stylesheet" href="../css/bootstrap.min.css">
  </head>
  <body>

      <div class="wrapper1">
        <div class="wrapper-logo">
          <a href=""><div class="logo">SNIFFER</div></a>
        </div>
        <div class="text">
          <p>SNIFFER: Model Detection Attack Demonstration</p>
        </div>
        <div class="logout">
          <a href="../main.html">Logout</a>
        </div>
      </div>

      <div class="wrapper2">
        <div class="wrapper2_div">
          <div id="top2_1">Target:</div>
          <ul class="wrapper2_nav">
            <li class="list_item1">
              <a href="../mlaas_attack.html">MLaaS Platform Attack</a></li>
          </ul>
          <em>or</em>
          <ul class="wrapper2_nav">
            <li class="list_item2">
              <a href="local_attack1.php">Local Simulation</a></li>
          </ul>
          <em>?</em>
        </div>
      </div>

      <div class="container">
        <table class="table table-light table-hover table-borderd" style="border:1px solic #ccc;table-layout:fixed;margin-top:20px;">
          <thead>
              <tr style="text-align:center;">
                  <th style="text-align:center;">Experiment Name</th>
                  <th style="text-align:center;">Attacked Model</th>
                  <th style="text-align:center;">Probe Modules</th>
                  <th style="text-align:center;">Attack Datasets</th>
                  <th style="text-align:center;">Results</th>
                  <th style="text-align:center;">Operation</th>
              </tr>
          </thead>

          
          <tbody style="text-align:center;word-wrap:break-word; word-break:break-all; overflow: hidden;"> 
              <?php
                include "connect.php";
                header("Content-Type: text/html; charset=utf8");
                $sql="select local_name,attacked_model,probe_modules,attack_datasets from local_attack";
                $retval = mysqli_query($con, $sql);
                if (!$retval) {
                  printf("Error: %s\n", mysqli_error($con));
                  exit();
                  }
                $row_length = mysqli_num_rows($retval);
                for ($i=0; $i<$row_length; $i++) {
                  $row = mysqli_fetch_assoc($retval);
                  $local_name = $row['local_name'];
                  $attacked_model = $row['attacked_model'];
                  $probe_modules = $row['probe_modules'];
                  $attack_datasets = $row['attack_datasets'];
                  echo '<tr><td>'.$local_name.'</td><td>'.$attacked_model.'</td><td>'.$probe_modules.'</td><td>'.$attack_datasets.'</td><td>'?>
                  <a style="text-align:center" href="query_local.php?local_name=<?php echo $local_name;?>">Results</a>
                  <br><br>
                  <a style="text-align:center" href="../local_log/<?php echo $local_name?>.txt">Log</a>
                  <?php echo'</td><td>'?>
                  <a style="text-align:center" href="delete_local.php?local_name=<?php echo $row["local_name"];?>" onclick="return confirm('Are you sure?')">Delete</a>
                  <?php echo '</td></tr>';
                };
                
                mysqli_close($con);
              ?>

          </tbody>
        </table>
      </div>





      <div class="wrapper3">
        <div class="footer">
          <p>
            <a href="#">School of Cyber Engineering</a><b>|</b>
            <a href="#">Xidian University</a><b>|</b>
            <a href="#">Xi'an</a><b>|</b>
            <a href="#">China</a>
          </p>
        </div>
      </div>


  </body>
</html>
