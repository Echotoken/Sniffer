<?php 
    session_start();

    $name_input=$_GET['mlaas_name'];

    include "connect.php";
    header("Content-Type: text/html; charset=utf8");

    $sql1="select cloud,probe_module,api,sample_space,attack_datasets,feature_num,feature_range from mlaas_attack where mlaas_name = '$name_input'";
    $retval1 = mysqli_query($con, $sql1);
    $row1 = mysqli_fetch_assoc($retval1);
    $cloud = $row1['cloud'];
    $probe_module = $row1['probe_module'];
    $api = $row1['api'];
    $sample_space = $row1['sample_space'];
    $attack_datasets = $row1['attack_datasets'];
    $feature_num = $row1['feature_num'];
    $feature_range = $row1['feature_range'];
    
    $arr=explode(",",$probe_module);
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

    $sql2 = "select tree_num,svm_num,linear_num,nn_num,tree_time,svm_time,linear_time,nn_time,tree_conf,svm_conf,linear_conf,nn_conf,cnn_conf,rnn_conf,gnn_conf,type from mlaas_result where mlaas_name = '$name_input'";
    $retval2 = mysqli_query($con, $sql2);
    $row2 = mysqli_fetch_assoc($retval2);
    $tree_num = $row2['tree_num'];
    $svm_num = $row2['svm_num'];
    $linear_num = $row2['linear_num'];
    $nn_num = $row2['nn_num'];
    $tree_time = $row2['tree_time'];
    $svm_time = $row2['svm_time'];
    $linear_time = $row2['linear_time'];
    $nn_time = $row2['nn_time'];
    $tree_conf = $row2['tree_conf'];
    $svm_conf = $row2['svm_conf'];
    $linear_conf = $row2['linear_conf'];
    $nn_conf = $row2['nn_conf'];
    $cnn_conf = $row2['cnn_conf'];
    $rnn_conf = $row2['rnn_conf'];
    $gnn_conf = $row2['gnn_conf'];
    $type = $row2['type'];
    $already_num = 0;
    if($tree_num != 0){
        $already_num = $already_num + 1;
    }
    if($svm_num != 0){
        $already_num = $already_num + 1;
    }
    if($linear_num != 0){
        $already_num = $already_num + 1;
    }
    if($nn_num != 0){
        $already_num = $already_num + 1;
    }
    $already_time = 0;
    if($tree_time != 0){
        $already_time = $already_time + 1;
    }
    if($svm_time != 0){
        $already_time = $already_time + 1;
    }
    if($linear_time != 0){
        $already_time = $already_time + 1;
    }
    if($nn_time != 0){
        $already_time = $already_time + 1;
    }
    if($type == "Tree" || $type == "SVM" || $type == "Linear"){
        $typer = true;
    }
    if($already_num == $models){
        $numr = true;
    }
    if($already_time == $models){
        $timer = true;
    }
    $param = "name_input=".$name_input."&tree_num=".$tree_num."&svm_num=".$svm_num."&linear_num=".$linear_num."&nn_num=".$nn_num."&tree_time=".$tree_time."&svm_time=".$svm_time."&linear_time=".$linear_time."&nn_time=".$nn_time."&tree_conf=".$tree_conf."&svm_conf=".$svm_conf."&linear_conf=".$linear_conf."&nn_conf=".$nn_conf."&cnn_conf=".$cnn_conf."&rnn_conf=".$rnn_conf."&gnn_conf=".$gnn_conf."&type=".$type;
?>
<DOCTYPE html>
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
              <a href="../local_attack1.php">Local Simulation</a></li>
          </ul>
          <em>?</em>
        </div>
      </div>
      
    <div class="container">
        <div class="container_div">
            <div class="container_input">
            <label for="name_input" id="name_input">Name:</label>
            <input type="text" name="name_input" value="<?php echo $name_input; ?>"
            onfocus="if(this.value=='Experiment Name'){this.value='';this.style.color='#424242';}"
            onblur="if(this.value==''){this.value='Experiment Name';this.style.color='#999';}">
            </div>

            <div class="container_checkbox">
            <label for="cloud_input" id="cloud_input">Cloud:</label>
            <input class="cloud_radio" name="cloud_input" value="Google" type="radio" <?php if($cloud=='Google') echo "checked" ; ?>>Google
            <input class="cloud_radio" name="cloud_input" value="Aliyun" type="radio" <?php if($cloud=='Aliyun') echo "checked" ; ?>>Aliyun
            <input class="cloud_radio" name="cloud_input" value="Tencent" type="radio" <?php if($cloud=='Tencent') echo "checked" ; ?>>Tencent
            <input class="cloud_radio" name="cloud_input" value="Huawei" type="radio" <?php if($cloud=='Huawei') echo "checked" ; ?>>Huawei
            </div>

            <div class="container_input">
            <label for="api_input" id="api_input">API:</label>
            <input type="text" name="api_input" value="<?php echo $api; ?>"
            onfocus="if(this.value=='MLaaS Interface site'){this.value='';this.style.color='#424242';}"
            onblur="if(this.value==''){this.value='MLaaS Interface site';this.style.color='#999';}">
            </div>

            <div class="container_checkbox">
            <label for="model_input[]" id="models_input">Probe Modules:</label>
            <input class="model_radio" name="model_input[]" value="Decision Tree" type="checkbox"  <?php if($models0=="1") echo "checked" ; ?> >Decision Tree
            <input class="model_radio" name="model_input[]" value="Kernel Model" type="checkbox"   <?php if($models1=="1") echo "checked" ; ?> >Kernel Model
            <input class="model_radio" name="model_input[]" value="Linear Model" type="checkbox"   <?php if($models2=="1") echo "checked" ; ?> >Linear Model
            <input class="model_radio" name="model_input[]" value="Neural Network" type="checkbox" <?php if($models3=="1") echo "checked" ; ?> >Neural Network
            </div>

            <div class="container_checkbox">
            <label for="space_input" id="space_input">Sample Space:</label>
            <input class="model_radio" name="space_input" value="CommonDatasets" type="radio" <?php if($sample_space=='CommonDatasets') echo "checked" ; ?> >Common Datasets
            <input class="model_radio" name="space_input" value="ManualInput" type="radio" <?php if($sample_space=='ManualInput') echo "checked" ; ?> >Manual Input
            </div>

            <div id="attack_datasets" class="container_input" <?php if($sample_space=='ManualInput') echo " style='display:none;'" ; ?> >
            <label for="attack_datasets_input" id="attack_datasets_input">Attack Datasets:</label>
            <select name="attack_datasets_input" id="datasets">
                <option  value="0"><?php echo $attack_datasets; ?></option>
            </select>
            </div>

            <div id="feature_range" class="container_input" <?php if($sample_space=='CommonDatasets') echo " style='display:none;'" ; ?>>
            <label for="feature_range_input" id="feature_range_input">Feature Range:</label>
            <input type="text" name="feature_range_input" value="<?php echo $feature_range; ?>"
            onfocus="if(this.value=='The Range of Each Feature:(-1,1),(-2,2)'){this.value='';this.style.color='#424242';}"
            onblur="if(this.value==''){this.value='The Range of Each Feature:(-1,1),(-2,2)';this.style.color='#999';}">
            </div>

            <div class="container_submit">
            <div class="container_submit1">
                <button onclick = "window.location.href = 'history_mlaas.php'">Return</button>
            </div>
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
  <script id="test" type="text/javascript" src="../css/js/mlaas_attack.js" data="<?php echo $param;?>"></script>

</html>
