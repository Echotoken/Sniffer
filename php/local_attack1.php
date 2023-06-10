<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Sniffer-login</title>
    <link rel="stylesheet" href="../css/local_attack.css">
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
          <ul class="nav">
            <li class="list_item1">
              <a href="../mlaas_attack.html">MLaaS Platform Attack</a></li>
          </ul>
          <em>or</em>
          <ul class="nav">
            <li class="list_item2">
              <a href="local_attack.php">Local Simulation</a></li>
          </ul>
          <em>?</em>
        </div>
      </div>

      <form id="form1" name="form1" action="local_attack.php" method="post" enctype="multipart/form-data">
          <div class="container">
            <div class="container_div">
              <div class="container_input">
                <label for="name_input" id="name_input">Name:</label>
                <input type="text" name="name_input" value="Experiment Name"
                onfocus="if(this.value=='Experiment Name'){this.value='';this.style.color='#424242';}"
                onblur="if(this.value==''){this.value='Experiment Name';this.style.color='#999';}">
              </div>

              <div class="container_checkbox" id="choose_model_div">
                <label for="choose_model">Attacked Model:</label>
                <input class="choose_model" name="choose_model" value="Upload" type="radio" onclick="choose_upload();" required>Upload
                <input class="choose_model" name="choose_model" value="Existing"type="radio" onclick="choose_exist();" required>Existing
              </div>

              <div class="container_uploadbox" id="upload_model_div" style="display: none;">
                <label for="upload_model_label">Upload Model:</label>
                <input id="upload_model" value="upload_model" name="upload_model" type="file" accept=".pkl" onchange="upload_file();">
              </div>

              <div class="container_choose_exist" id="exist_div" style="display:none;">
                <label for="exist" id="exist_label">Existing Model:</label>
                <select name="exist" id="exist">
                  <option value="0">--Please choose an option--</option>
                  <?php 
                    include "connect.php";
                    header("Content-Type: text/html; charset=utf8");
                    $sql1="select model from choose_model";
                    $retval = mysqli_query($con, $sql1);
                    if (!$retval) {
                        printf("Error: %s\n", mysqli_error($conn));
                        exit();
                        }
                        $row_length = mysqli_num_rows($retval);
                        for ($i=0; $i<$row_length; $i++) {
                            $row = mysqli_fetch_assoc($retval);
                            $model = $row['model'];
                            echo '<option value="'.$model.'">'.$model.'</option>';
                            }
                        mysqli_close($con);
                    ?>
                </select>
              </div>
              <div class="container_checkbox">
                <label for="model_input" id="models_input">Probe Modules:</label>
                <input class="model_radio" name="model_input[]" value="Decision Tree"type="checkbox">Decision Tree
                <input class="model_radio" name="model_input[]" value="Kernel Model" type="checkbox">Kernel Model
                <input class="model_radio" name="model_input[]" value="Linear Model" type="checkbox">Linear Model
                <input class="model_radio" name="model_input[]" value="Neural Network" type="checkbox">Neural Network
              </div>
              <div class="container_input">
                <label for="feature_num_input" id="feature_num_input">Attack Datasets:</label>
                <select name="datasets" id="datasets">
                  <option value="0">--Please choose an option--</option>
                  <option value="Iris">Iris (4)</option>
                  <option value="wine">Wine (13)</option>
                  <option value="Adult">Adult (14)</option>
                  <option value="cancer">Cancer (30)</option>
                  <option value="digits">Digits (8,8)</option>
                  <option value="MNIST">MNIST (28,28)</option>
                  <option value="fashion">Fashion-MNIST (28,28)</option>
                  <option value="CIFAR10">CIFAR10 (3,32,32)</option>
                </select>
              </div>

          <div class="container_submit">
            <div class="container_submit1">
              <button type="submit">ATTACK</button>
            </div>
            <div class="container_submit2">
              <a href="history_local.php" id="history">Attack History</a>
            </div>
          </div>

          <div id="log_div" class="container_log" style="display:none;">
            <label for="result_log" id="result_log">Demo Log:</label>
            <textarea id="result_log" name="result_log" rows="10"></textarea>
          </div>

          <div id="result_div" class="container_results" style="display:none;">
            <label for="results">Results:</label>
            <textarea id="results" name="results" rows="10"></textarea>
          </div>

        </div>
      </from>
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

      <script type="text/javascript">
        function choose_upload(){
          document.getElementById("upload_model_div").style.display="block";
          document.getElementById("exist_div").style.display="none";
        }
        function choose_exist(){
          document.getElementById("exist_div").style.display="block";
          document.getElementById("upload_model_div").style.display="none";
        }
      </script>











  </body>
</html>
