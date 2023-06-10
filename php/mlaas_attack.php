<?php
    session_start();
    include "connect.php";
    header("Content-Type: text/html; charset=utf8");

    $json_data = json_decode(file_get_contents('../configuration.json'), true);

    $py_exe = $json_data["MLaaS"]["python_directory"];
    $py_file = "../attack/sniffer_mlaas.py";
    
    $_SESSION["py_exe"] = $py_exe;
    $_SESSION["py_file"] = $py_file;
    $_SESSION["name_input"] = $_POST['name_input'];
    $_SESSION["cloud_input"] = $_POST['cloud_input'];
    $_SESSION["api_input"] = $_POST['api_input'];
    $_SESSION["space_input"] = $_POST['space_input'];
    @$name_input = $_SESSION["name_input"];
    @$cloud_input = $_SESSION["cloud_input"];
    $model_input1 = $_POST['model_input'];
    @$api_input = $_SESSION["api_input"];
    @$space_input = $_SESSION["space_input"];

    $model_input = implode(",",$model_input1);

    if($space_input == "CommonDatasets"){
        $_SESSION["attack_datasets_input"] = $_POST['attack_datasets_input'];
        $attack_datasets_input = $_SESSION["attack_datasets_input"];
        $feature_num_input = "-";
        $feature_range_input = "-";
    }
    else if($space_input == "ManualInput"){
        $_SESSION["feature_num_input"] = $_POST['feature_num_input'];
        $_SESSION["feature_range_input"] = $_POST['feature_range_input'];
        $feature_num_input = $_SESSION["feature_num_input"];
        $feature_num_input = str_replace('(', '', $feature_num_input);
        $feature_num_input = str_replace(')', '', $feature_num_input);
        $feature_num_input = str_replace(' ', '', $feature_num_input);
        $feature_range_input = $_SESSION["feature_range_input"];
        $feature_range_input = str_replace('(', '', $feature_range_input);
        $feature_range_input = str_replace(')', ',', $feature_range_input);
        $feature_range_input = str_replace(' ', '', $feature_range_input);
        $attack_datasets_input = "-";
    }

    $sql1="INSERT INTO mlaas_attack (mlaas_name,cloud,probe_module,api,sample_space,attack_datasets,feature_num,feature_range) VALUES('$name_input','$cloud_input','$model_input','$api_input','$space_input','$attack_datasets_input','$feature_num_input','$feature_range_input')";
    $sql2="INSERT INTO mlaas_result VALUES(0,0,0,NULL,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,'$_POST[name_input]','type')";
    $retval1 = mysqli_query($con,$sql1);
    $retval2 = mysqli_query($con,$sql2);
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

    $api = explode(",",$api_input);
    $arr = explode(",",$model_input);
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

    
    // echo "sudo $py_exe $py_file $models0 $models1 $models2 $models3 $name_input $space_input $attack_datasets_input $feature_range_input $cloud_input $api[0] $feature_num_input";

    if($cloud_input == "Aliyun"){
        exec("sudo $py_exe $py_file $models0 $models1 $models2 $models3 $name_input $space_input $attack_datasets_input $feature_range_input $cloud_input $api[0] $api[1] $feature_num_input",$out,$res);
    }
    else{
        exec("sudo $py_exe $py_file $models0 $models1 $models2 $models3 $name_input $space_input $attack_datasets_input $feature_range_input $cloud_input $api[0] $feature_num_input",$out,$res);
    }

    
    mysqli_close($con);
?>













<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Sniffer-login</title>
    <link rel="stylesheet" href="../css/mlaas_attack.css">
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

            <div class="container_checkbox">
            <label for="cloud_input" id="cloud_input">MLaaS Cloud:</label>
            <input class="cloud_radio" name="cloud_input" value="Google" type="radio" <?php if($_POST['cloud_input']=='Google') echo "checked" ; ?>>Google
            <input class="cloud_radio" name="cloud_input" value="Amazon" type="radio" <?php if($_POST['cloud_input']=='Amazon') echo "checked" ; ?>>Amazon
            <input class="cloud_radio" name="cloud_input" value="Aliyun" type="radio" <?php if($_POST['cloud_input']=='Aliyun') echo "checked" ; ?>>Aliyun
            <input class="cloud_radio" name="cloud_input" value="Tencent" type="radio" <?php if($_POST['cloud_input']=='Tencent') echo "checked" ; ?>>Tencent
            <input class="cloud_radio" name="cloud_input" value="Huawei" type="radio" <?php if($_POST['cloud_input']=='Huawei') echo "checked" ; ?>>Huawei
            </div>

            <div class="container_input">
            <label for="api_input" id="api_input">Prediction API:</label>
            <input type="text" name="api_input" value="<?php echo $_POST['api_input']; ?>"
            onfocus="if(this.value=='The Interface of Target Model in MLaaS'){this.value='';this.style.color='#424242';}"
            onblur="if(this.value==''){this.value='The Interface of Target Model in MLaaS';this.style.color='#999';}">
            </div>

            <div class="container_checkbox">
            <label for="model_input[]" id="models_input">Probe Modules:</label>
            <input class="model_radio" name="model_input[]" value="DecisionTree" type="checkbox"  <?php if($models0=="1") echo "checked" ; ?> >Decision Tree
            <input class="model_radio" name="model_input[]" value="KernelModel" type="checkbox"   <?php if($models1=="1") echo "checked" ; ?> >Kernel Model
            <input class="model_radio" name="model_input[]" value="LinearModel" type="checkbox"   <?php if($models2=="1") echo "checked" ; ?> >Linear Model
            <input class="model_radio" name="model_input[]" value="NeuralNetwork" type="checkbox" <?php if($models3=="1") echo "checked" ; ?> >Neural Network
            </div>

            <div class="container_checkbox">
            <label for="space_input" id="space_input">Sample Space:</label>
            <input class="model_radio" name="space_input" value="CommonDatasets" type="radio" <?php if($_POST['space_input']=='CommonDatasets') echo "checked" ; ?> >Common Datasets
            <input class="model_radio" name="space_input" value="ManualInput" type="radio" <?php if($_POST['space_input']=='ManualInput') echo "checked" ; ?> >Manual Input
            </div>



            <div id="attack_datasets" class="container_input" <?php if($_POST['space_input']=='ManualInput') echo " style='display:none;'" ; ?> >
            <label for="attack_datasets_input" id="attack_datasets_input">Attack Datasets:</label>
            <select name="attack_datasets_input" id="datasets">
                <option  value="0"><?php echo $_POST['attack_datasets_input']; ?></option>
            </select>
            </div>



            <div id="feature_num" class="container_input" <?php if($_POST['space_input']=='CommonDatasets') echo " style='display:none;'" ; ?>>
            <label for="feature_num_input" id="feature_num_input">Feature Num:</label>
            <input type="text" name="feature_num_input"value="<?php echo $_POST['feature_num_input']; ?>"
            onfocus="if(this.value=='The Number of Feature'){this.value='';this.style.color='#424242';}"
            onblur="if(this.value==''){this.value='The Number of Feature';this.style.color='#999';}">
            </div>

            <div id="feature_range" class="container_input" <?php if($_POST['space_input']=='CommonDatasets') echo " style='display:none;'" ; ?>>
            <label for="feature_range_input" id="feature_range_input">Feature Range:</label>
            <input type="text" name="feature_range_input" value="<?php echo $_POST['feature_range_input']; ?>"
            onfocus="if(this.value=='The Range of Each Feature:(-1,1),(-2,2)'){this.value='';this.style.color='#424242';}"
            onblur="if(this.value==''){this.value='The Range of Each Feature:(-1,1),(-2,2)';this.style.color='#999';}">
            </div>

            <div class="container_submit">
            <div class="container_submit1">
                <button type="submit">ATTACK</button>
            </div>
            <div class="container_submit2">
                <a href="../history_mlaas.php" id="history">Attack History</a>
            </div>
            </div>

            <div id="log_div" class="container_log" >
            <label for="result_log" id="result_log">Demo Log:</label>
            <textarea style="font-family: Times New Roman;font-size: large" name="result_log" rows="20"><?php 
                  $file="../mlaas_log/$name_input.txt";
                  $txt = file($file);
                  for($i=0;$i<count($txt);$i++){
                    echo $txt[$i];
                  }
              ?></textarea>
            </div>
        

            <div id="result_div" class="container_results">
                <label id="final_result" for="results">Results: <?php  
                      include "connect.php";
                      $sql1="select type from mlaas_result where mlaas_name='$name_input'";
                      $retval1 = mysqli_query($con, $sql1);
                      $row1 = mysqli_fetch_assoc($retval1);
                      $type = $row1['type'];
                      echo $type;?></label>
                    
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
      $sql = "select tree_num,svm_num,linear_num,nn_num,tree_time,svm_time,linear_time,nn_time,tree_conf,svm_conf,linear_conf,nn_conf,cnn_conf,rnn_conf,gnn_conf,type from mlaas_result where mlaas_name = '$name_input'";
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
