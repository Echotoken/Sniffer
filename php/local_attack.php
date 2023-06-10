<?php
    session_start();
    include "connect.php";
    header("Content-Type: text/html; charset=utf8");

    $json_data = json_decode(file_get_contents('../configuration.json'), true);

    $py_exe = $json_data["Local"]["python_directory"];
    $py_file = "../attack/sniffer_local.py";
    
    $_SESSION["py_exe"] = $py_exe;
    $_SESSION["py_file"] = $py_file;
    $_SESSION["name_input"] = $_POST['name_input'];
    $_SESSION["choose_model"] = $_POST['choose_model'];
    $_SESSION["model_input"] = $_POST['model_input'];
    $_SESSION["datasets"] = $_POST['datasets'];
    @$name_input = $_SESSION["name_input"];
    @$choose_model = $_SESSION["choose_model"];
    $model_input1 = $_POST['model_input'];
    @$datasets = $_SESSION["datasets"];

    $model_input = implode(",", $model_input1);

    echo $_FILES["upload_model"]["name"];
    if($_FILES["upload_model"]["name"]==NULL){
      $file_name = $_POST['exist'];
      $file_url = "upload/".$file_name;
    }
    else{
      $temp = explode(".", $_FILES["upload_model"]["name"]);
      $extension = end($temp);
      move_uploaded_file($_FILES["upload_model"]["tmp_name"], "upload/" . $_FILES["upload_model"]["name"]);
      $file_url="upload/".$_FILES["upload_model"]["name"];
      $file_name=$_FILES["upload_model"]["name"];
    }
    

    if($choose_model == "Upload"){
        $model = "Upload";
    }
    else if($choose_model == "Existing"){
        $_SESSION["exist"] = $_POST['exist'];
        $model = $_SESSION["exist"];
    }

    $sql1="INSERT INTO local_attack (local_name,attacked_model,probe_modules,attack_datasets,upload_model) VALUES('$name_input','$model','$model_input','$datasets','$choose_model')";
    $sql2="INSERT INTO local_result VALUES(0,0,0,NULL,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'$_POST[name_input]','type')";
    $sql3="INSERT INTO choose_model (model) VALUES('$file_name')";
    $retval1 = mysqli_query($con,$sql1);
    $retval2 = mysqli_query($con,$sql2);
    $retval3 = mysqli_query($con,$sql3);
    if($retval1 && $retval2){
        echo "
        <script type='text/javascript'>
            alert('Insert successfully!');
         </script>";
    }
    else{
        echo "
        <script type='text/javascript'>
            alert('Insert error!');
         </script>";
    }
    
    $arr=explode(",",$model_input);
    $models = array();
    if(in_array("Decision Tree",$arr)){$models[0] = "1";}else{$models[0] = "0";}
    if(in_array("Kernel Model",$arr)){$models[1] = "1";}else{$models[1] = "0";}
    if(in_array("Linear Model",$arr)){$models[2] = "1";}else{$models[2] = "0";}
    if(in_array("Neural Network",$arr)){$models[3] = "1";}else{$models[3] = "0";}
    $_SESSION["models0"] = $models[0];
    $_SESSION["models1"] = $models[1];
    $_SESSION["models2"] = $models[2];
    $_SESSION["models3"] = $models[3];
    
    $models0 = $_SESSION["models0"];
    $models1 = $_SESSION["models1"];
    $models2 = $_SESSION["models2"];
    $models3 = $_SESSION["models3"];

    // echo "sudo $py_exe $py_file $models0 $models1 $models2 $models3 $name_input $file_url $datasets ";
    
    exec("sudo $py_exe $py_file $models0 $models1 $models2 $models3 $name_input $file_url $datasets ",$out,$res);
  
    mysqli_close($con);
?>




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
          <a href="../sniffer.html"><div class="logo">SNIFFER</div></a>
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
              <a href="local_attack1.php">Local Simulation</a></li>
          </ul>
          <em>?</em>
        </div>
      </div>

    <div class="container">
        <div class="container_div">
            <div class="container_input">
            <label for="name_input" id="name_input">Name:</label>
            <input type="text" name="name_input" value="<?php echo $_POST['name_input']; ?>"
            onfocus="if(this.value=='Experiment Name'){this.value='';this.style.color='#424242';}"
            onblur="if(this.value==''){this.value='Experiment Name';this.style.color='#999';}">
            </div>

            <div class="container_checkbox" id="choose_model_div">
            <label for="choose_model">Attacked Model:</label>
            <input class="choose_model" name="choose_model" value="Upload" type="radio" <?php if($_POST['choose_model']=='Upload') echo "checked" ; ?>>Upload
            <input class="choose_model" name="choose_model" value="Existing" type="radio" <?php if($_POST['choose_model']=='Existing') echo "checked" ; ?>>Existing
            </div>

            <div class="container_checkbox" id="choose_upload_div" <?php if($_POST['choose_model']=='Existing') echo " style='display:none;'" ; ?>>
            <label for="upload_model">Upload Model:</label>
            <input id="upload_model" value="upload" name="upload_model" type="file" accept=".pkl" onchange="upload_file();">
            </div>

            <div class="container_choose_exist" id="exist1" <?php if($_POST['choose_model']=='Upload') echo " style='display:none;'" ; ?>>
            <label for="exist">Existing Model:</label>
            <select name="exist" id="exist">
                <option value="0"><?php echo $_POST['exist']; ?></option>
            </select>
            </div>
            
            <div class="container_checkbox">
            <label for="model_input" id="models_input">Probe Modules:</label>
            <input class="model_radio" name="model_input" value="DecisionTree" type="checkbox" <?php if($models0=="1") echo "checked" ; ?>>Decision Tree
            <input class="model_radio" name="model_input" value="KernelModel"  type="checkbox" <?php if($models1=="1") echo "checked" ; ?>>Kernel Model
            <input class="model_radio" name="model_input" value="LinearModel"  type="checkbox" <?php if($models2=="1") echo "checked" ; ?>>Linear Model
            <input class="model_radio" name="model_input" value="NeuralNetwork" type="checkbox"<?php if($models3=="1") echo "checked" ; ?>>Neural Network
            </div>

            <div class="container_input">
            <label for="feature_num_input" id="feature_num_input">Attack Datasets:</label>
            <select name="datasets" id="datasets">
                <option value="0"><?php echo $_POST['datasets']; ?></option>
            </select>
            </div>
          
          <div class="container_submit">
            <div class="container_submit1">
              <button type="submit">ATTACK</button>
            </div>
            <div class="container_submit2">
              <a href="../history_local.php" id="history">Attack History</a>
            </div>
          </div>

          <div id="log_div" class="container_log">
            <label for="result_log" id="result_log">Processing Log:</label>
            <textarea style="font-family: Times New Roman;font-size: large" id="result_log" name="result_log" rows="20"><?php 
                  $file="../local_log/$name_input.txt";
                  $txt = file($file);
                  for($i=0;$i<count($txt);$i++){
                    echo $txt[$i];
                  }
              ?></textarea>
          </div>

          <div id="result_div" class="container_results">
              <label id="final_result" for="results">Results: <?php  
                    include "connect.php";
                    $sql1="select type from local_result where local_name='$name_input'";
                    $retval1 = mysqli_query($con, $sql1);
                    $row1 = mysqli_fetch_assoc($retval1);
                    $type = $row1['type'];
                    echo $type;
                    ?></label>
              <div class="result_container1">
                  <canvas id="canvas" name="canvas" width="520" height="340" ></canvas>
                  <canvas id="canvas1" name="canvas1" width="520" height="340" ></canvas>
              </div>
              <div class="result_container2">
                  <canvas id="barChart" name="barChart" width="500" height="300" ></canvas>
                  <canvas id="barChart1" name="barChart1" width="500" height="300" ></canvas>
              </div>
          </div>

        </div>
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
  <?php
      include "connect.php";
      $sql = "select tree_num,svm_num,linear_num,nn_num,tree_time,svm_time,linear_time,nn_time,tree_conf,svm_conf,linear_conf,nn_conf,cnn_conf,rnn_conf,gnn_conf,type from local_result where local_name = '$name_input'";
      $retval = mysqli_query($con, $sql);
      $row = mysqli_fetch_assoc($retval);
      $tree_num = $row['tree_num'];
      $svm_num = $row['svm_num'];
      $linear_num = $row['linear_num'];
      $nn_num = $row['nn_num'];
      $tree_time = $row['tree_time'];
      $svm_time = $row['svm_time'];
      $linear_time = $row['linear_time'];
      $nn_time = $row['nn_time'];
      $tree_conf = $row['tree_conf'];
      $svm_conf = $row['svm_conf'];
      $linear_conf = $row['linear_conf'];
      $nn_conf = $row['nn_conf'];
      $cnn_conf = $row['cnn_conf'];
      $rnn_conf = $row['rnn_conf'];
      $gnn_conf = $row['gnn_conf'];
      $type = $row['type'];
      $param = "name_input=".$name_input."&tree_num=".$row["tree_num"]."&svm_num=".$row["svm_num"]."&linear_num=".$row["linear_num"]."&nn_num=".$row["nn_num"]."&tree_time=".$row["tree_time"]."&svm_time=".$row["svm_time"]."&linear_time=".$row["linear_time"]."&nn_time=".$row["nn_time"]."&tree_conf=".$row["tree_conf"]."&svm_conf=".$row["svm_conf"]."&linear_conf=".$row["linear_conf"]."&nn_conf=".$row["nn_conf"]."&cnn_conf=".$row["cnn_conf"]."&rnn_conf=".$row["rnn_conf"]."&gnn_conf=".$row["gnn_conf"]."&type=".$row["type"];
  ?>
  <script id="test" type="text/javascript" src="../css/js/mlaas_attack.js" data="<?php echo $param;?>"></script>
</html>
