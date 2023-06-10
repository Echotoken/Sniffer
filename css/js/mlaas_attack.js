  var fin = [];
  function res(n){
    var results = document.getElementById('test').getAttribute('data');
    var result = results.split("&");
    for(i=0;i<17;i++){
      var re = result[i].split("=");
      fin.push(re[1]);
    }
    return function(){
      return(fin[n]);
    }
  }
  
  class PieChart{
      constructor(data){
          this.data=data;
          this.canvas=document.getElementById('canvas');
          this.ctx=this.canvas.getContext('2d');
          this.setRadio();///适应屏幕的分辨率
          this.x0=this.canvas.width/2;//圆心
          this.y0=this.canvas.height/2 - 10;
  
          this.radius=100;//半径
          this.addLine=50;
  
          this.init();
          this.drawPie(this.x0,this.y0);
      }
      setRadio(){
          //让线变清晰 提高分辨率
          let d=window.devicePixelRatio||1;
          let cd=this.ctx.backingStorePixelRatio||1;
          let r=d/cd;
          this.r=r;
          let w=this.canvas.width;
          let h=this.canvas.height;
          this.canvas.width=r*w;
          this.canvas.height=r*h;
          this.canvas.style.width=w+'px';
          this.canvas.style.height=h+'px';
      }
      toAngle(){
          //把数据转成弧度
          let t=0;
          this.data.forEach(item=>{
              t+=item.num
          })
          this.data.forEach((item,i)=>{
              let angle=item.num/t*Math.PI*2;
              item.angle=angle;
              this.color=item.color;
          })
      }
      randomColor(){
          var r = Math.floor(Math.random() * 256);
          var g = Math.floor(Math.random() * 256);
          var b = Math.floor(Math.random() * 256);
          var color = '#' + r.toString(16) + g.toString(16) + b.toString(16);
          return color;
      }
      init(){
          this.toAngle();
      }
      drawPie(x,y){
          //画饼
          let start=0;
          //根据数据画饼
          console.log(this.data)
          this.type = [];
          this.typenum = [];
          this.data.forEach((item,i)=>{
              //结束弧度就是起始值加上自己的弧度
              let end=start+item.angle;
              this.type[i] = item.title;
              this.typenum[i] = item.num;
              this.ctx.beginPath();
              this.ctx.moveTo(this.x0,this.y0); 
              this.ctx.arc(this.x0,this.y0,this.radius,start,end,false);
              this.ctx.closePath();
              if(this.ctx.isPointInPath(x*this.r,y*this.y)){
                  this.ctx.fillStyle='#f00';
                  this.ctx.fill();
                  this.drawTitle(start,this.radius,item,'#f00');
              }
              else{
                  this.ctx.fillStyle=item.color;
                  this.ctx.fill();
                  this.drawTitle(start,this.radius,item,item.color);
              }
              start=end;
          })
          this.drawName(this.x0,this.y0,this.radius);
      }
      drawTitle(start,radius,item,color){
          //写标题
          let lineLength =radius+this.addLine
          let endX=lineLength*Math.cos(start+item.angle/2);
          let endY=lineLength*Math.sin(start+item.angle/2);
          let outX=this.x0+endX;
          let outY=this.y0+endY;
          this.ctx.beginPath();
          this.ctx.moveTo(this.x0,this.y0);
          this.ctx.lineTo(outX,outY);
          this.ctx.strokeStyle=color;
          this.ctx.stroke();
  
          //写字
          this.ctx.font='20px 微软雅黑 sans-serif';
          this.ctx.textAlign =outX>this.x0?'left':'right';
          this.ctx.textBaseline='bottom';//字以底部为基准
          this.ctx.fillStyle=color;
          this.ctx.fillText(item.title+":"+item.num+" times",outX,outY);
  
          //添加下划线
          let textW=this.ctx.measureText(item.title+":"+item.num+" times").width;//获取文字所占宽度
          this.ctx.moveTo(outX,outY);
          let textEndX=outX>this.x0?outX+textW:outX-textW;
          this.ctx.lineTo(textEndX,outY);
          this.ctx.stroke();
      }
      drawLengend(index,item){
          //画lengend
          this.ctx.beginPath();
          this.ctx.rect(10,30*index+30,40,20);//(x,y,w,h)
          this.ctx.fillStyle=item.color;
          this.ctx.fill();
          this.ctx.font='20px 微软雅黑 sans-serif';
          this.ctx.textAlign='left';
          this.ctx.fillText(item.title,60,50+30*index);
      }
  
      drawName(x0,y0,radius){
        //在底部添加标题
        this.ctx.font='normal bold 25px Times New Roman sans-serif';
        let theX = x0 - this.ctx.measureText("Query Times").width/2;
        let theY = y0 - radius + 290;
        this.ctx.beginPath();
        this.ctx.moveTo(theX,theY);
        this.ctx.textBaseline='bottom';
        this.ctx.fillStyle = "Black";
        this.ctx.fillText("Query Times",theX,theY);
        this.ctx.textAlign='center';
      }
  
      drawDesc(type,typenum,x0,y0,radius){
        let name1 = type[0];
        let name2 = type[1];
        let name3 = type[2];
        let name4 = type[3];
        let linearn = typenum[0];
        let svmn = typenum[1];
        let treen = typenum[2];
        let nnn = typenum[3];
        this.ctx.font='normal bold 22px 微软雅黑 sans-serif';
        let theX = x0;
        let theY = y0 + radius + 80;
        this.ctx.beginPath();
        this.ctx.moveTo(theX,theY);
        this.ctx.textBaseline='bottom';
        this.ctx.fillStyle = "Grey";
        this.ctx.fillText(name1+":"+linearn+" times "+name2+":"+svmn+" times "+name3+":"+treen+" times "+name4+":"+nnn+" times",theX,theY);
        this.ctx.textAlign='center';
      }
  
      bindEvent(){
          this.canvas.addEventListener('mousemove',(e)=>{
              //获取鼠标点相对画布的位置
              let x=e.clientX-this.canvas.getBoundingClientRect().left;
              let y=e.clientY-this.canvas.getBoundingClientRect().top;
              this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height);
              this.drawPie(x,y);
          })
      }
  }
  
  function data(){
    var pie_linear0_1 = res(3);
    var pie_linear_1 = pie_linear0_1();
    var pie_svm0_1 = res(2);
    var pie_svm_1 = pie_svm0_1();
    var pie_tree0_1 = res(1);
    var pie_tree_1 = pie_tree0_1();
    var pie_nn0_1 = res(4);
    var pie_nn_1 = pie_nn0_1();
    var data=[{
        title:"LM",num:Number(pie_linear_1),color:'#104680',
    },{
        title:"KM",num:Number(pie_svm_1),color:'#B6D7E8',
    },{
        title:"DT",num:Number(pie_tree_1),color:'#DC6D57',
    },{
        title:"NN",num:Number(pie_nn_1),color:'#B72230',
    },];
    return data;
  }
  let chart = new PieChart(data());

  class PieChart1{
      constructor(data){
          this.data=data;
          this.canvas=document.getElementById('canvas1');
          this.ctx=this.canvas.getContext('2d');
          this.setRadio();///适应屏幕的分辨率
          this.x0=this.canvas.width/2;//圆心
          this.y0=this.canvas.height/2 - 10;
  
          this.radius=100;//半径
          this.addLine=50;
  
          this.init();
          this.drawPie(this.x0,this.y0);
      }
      setRadio(){
          //让线变清晰 提高分辨率
          let d=window.devicePixelRatio||1;
          let cd=this.ctx.backingStorePixelRatio||1;
          let r=d/cd;
          this.r=r;
          let w=this.canvas.width;
          let h=this.canvas.height;
          this.canvas.width=r*w;
          this.canvas.height=r*h;
          this.canvas.style.width=w+'px';
          this.canvas.style.height=h+'px';
      }
      toAngle(){
          //把数据转成弧度
          let t=0;
          this.data.forEach(item=>{
              t+=item.num
          })
          this.data.forEach((item,i)=>{
              let angle=item.num/t*Math.PI*2;
              item.angle=angle;
              this.color=item.color;
          })
      }
      randomColor(){
          var r = Math.floor(Math.random() * 256);
          var g = Math.floor(Math.random() * 256);
          var b = Math.floor(Math.random() * 256);
          var color = '#' + r.toString(16) + g.toString(16) + b.toString(16);
          return color;
      }
      init(){
          this.toAngle();
      }
      drawPie(x,y){
          //画饼
          let start=0;
          //根据数据画饼
          console.log(this.data)
          this.type = [];
          this.typenum = [];
          this.data.forEach((item,i)=>{
              //结束弧度就是起始值加上自己的弧度
              let end=start+item.angle;
              this.type[i] = item.title;
              this.typenum[i] = item.num;
              this.ctx.beginPath();
              this.ctx.moveTo(this.x0,this.y0);
              this.ctx.arc(this.x0,this.y0,this.radius,start,end,false);
              this.ctx.closePath();
              if(this.ctx.isPointInPath(x*this.r,y*this.y)){
                  this.ctx.fillStyle='#f00';
                  this.ctx.fill();
                  this.drawTitle(start,this.radius,item,'#f00');
              }
              else{
                  this.ctx.fillStyle=item.color;
                  this.ctx.fill();
                  this.drawTitle(start,this.radius,item,item.color);
              }
              start=end;
          })
          this.drawName(this.x0,this.y0,this.radius);
      }
      drawTitle(start,radius,item,color){
          //写标题
          let lineLength =radius+this.addLine
          let endX=lineLength*Math.cos(start+item.angle/2);
          let endY=lineLength*Math.sin(start+item.angle/2);
          let outX=this.x0+endX;
          let outY=this.y0+endY;
          this.ctx.beginPath();
          this.ctx.moveTo(this.x0,this.y0);
          this.ctx.lineTo(outX,outY);
          this.ctx.strokeStyle=color;
          this.ctx.stroke();
  
          //写字
          this.ctx.font='20px 微软雅黑 sans-serif';
          this.ctx.textAlign =outX>this.x0?'left':'right';
          this.ctx.textBaseline='bottom';//字以底部为基准
          this.ctx.fillStyle=color;
          this.ctx.fillText(item.title+":"+item.num+"ms",outX,outY);
  
          //添加下划线
          let textW=this.ctx.measureText(item.title+":"+item.num+"ms").width;//获取文字所占宽度
          this.ctx.moveTo(outX,outY);
          let textEndX=outX>this.x0?outX+textW:outX-textW;
          this.ctx.lineTo(textEndX,outY);
          this.ctx.stroke();
      }
      drawLengend(index,item){
          //画lengend
          this.ctx.beginPath();
          this.ctx.rect(10,30*index+30,40,20);//(x,y,w,h)
          this.ctx.fillStyle=item.color;
          this.ctx.fill();
          this.ctx.font='20px 微软雅黑 sans-serif';
          this.ctx.textAlign='left';
          this.ctx.fillText(item.title,60,50+30*index);
      }
      
      drawName(x0,y0,radius){
        //在底部添加标题
        this.ctx.font='normal bold 25px Times New Roman sans-serif';
        let theX = x0 - this.ctx.measureText("Running Time").width/2;
        let theY = y0 - radius + 290;
        this.ctx.beginPath();
        this.ctx.moveTo(theX,theY);
        this.ctx.textBaseline='bottom';
        this.ctx.fillStyle = "Black";
        this.ctx.fillText("Running Time",theX,theY);
        this.ctx.textAlign='center';
      }
  
      drawDesc(type,typenum,x0,y0,radius){
        let name1 = type[0];
        let name2 = type[1];
        let name3 = type[2];
        let name4 = type[3];
        let linearn = typenum[0];
        let svmn = typenum[1];
        let treen = typenum[2];
        let nnn = typenum[3];
        this.ctx.font='normal bold 22px 微软雅黑 sans-serif';
        let theX = x0;
        let theY = y0 + radius + 80;
        this.ctx.beginPath();
        this.ctx.moveTo(theX,theY);
        this.ctx.textBaseline='bottom';
        this.ctx.fillStyle = "Grey";
        this.ctx.fillText(name1+":"+linearn+"ms "+name2+":"+svmn+"ms "+name3+":"+treen+"ms "+name4+":"+nnn+"ms",theX,theY);
        this.ctx.textAlign='center';
      }
  
      bindEvent(){
          this.canvas.addEventListener('mousemove',(e)=>{
              //获取鼠标点相对画布的位置
              let x=e.clientX-this.canvas.getBoundingClientRect().left;
              let y=e.clientY-this.canvas.getBoundingClientRect().top;
              this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height);
              this.drawPie(x,y);
          })
      }
  }
  
  function data1(){
    var pie_linear1_1 = res(7);
    var pie_linear_2 = pie_linear1_1();
    var pie_svm1_1 = res(6);
    var pie_svm_2 = pie_svm1_1();
    var pie_tree1_1 = res(5);
    var pie_tree_2 = pie_tree1_1();
    var pie_nn1_1 = res(8);
    var pie_nn_2 = pie_nn1_1();
    var data1=[{
        title:"LM",num:Number(pie_linear_2),color:'#104680',
    },{
        title:"KM",num:Number(pie_svm_2),color:'#B6D7E8',
    },{
        title:"DT",num:Number(pie_tree_2),color:'#DC6D57',
    },{
        title:"NN",num:Number(pie_nn_2),color:'#B72230',
    },];
    return data1;
  }
  let chart1 = new PieChart1(data1());
  
  
  class BarChart{
      constructor(id){
        this.canvas = document.getElementById(id);
        // 创造绘画环境
        this.ctx = this.canvas.getContext('2d');
        
        this.setRatio()
        this.cPadding = 80;// 内边距
        this.yAxisH = this.canvas.height - this.cPadding * 2;// 纵轴的高度
        this.xAxixW = this.canvas.width  - this.cPadding * 2;// 横轴的宽度
        this.originX = this.cPadding;// 原点的横坐标
        this.originY = this.yAxisH + this.cPadding;//原点的纵坐标
        this.yAxisNum = 5;// 总左边分的段数
        this.xAxisNum = 0;// 横坐标的段数
        this.data = []// 存储传进来的数据
  
        this.count = 0;
      }
      init(){
        this.ctx.font = '20px Arial'
        // 画一个坐标系
        this.drawAxis()
        this.bindEvent();
      }
      setData(ary){
        this.data = ary;
        this.xAxisNum = ary.length;
        this.init()
      }
      setRatio(){
        let device = window.devicePixelRatio || 1;
        let canDevice = this.ctx.backingStorePixelRatio || 1;
        let ratio = device/canDevice;
        let oldW = this.canvas.width,
            oldH = this.canvas.height;
        this.canvas.width = ratio *  oldW;   
        this.canvas.height = ratio *  oldH;  
        this.canvas.style.width = oldW + 'px';
        this.canvas.style.height = oldH + 'px'; 
      }
      drawLine(x,y,x2,y2){
        // xy 对应的其实坐标   x2y2对应终点坐标
        this.ctx.beginPath();
        this.ctx.lineWidth = 1;// 设置线的宽度1个像素
        this.ctx.moveTo(x,y)
        this.ctx.lineTo(x2,y2);
        this.ctx.stroke();
        this.ctx.closePath()
      }
      drawAxis(){
        this.ctx.translate(0.5,0.5);//把 canvas的坐标原点 设置到 0.5,0.5的位置；// 解决 线模糊的问题
  
        //定义一下线条的颜色
        this.ctx.strokeStyle = 'black';
        // 画y轴
        this.drawLine(this.originX,this.originY,this.originX,this.cPadding)
        // 画x轴
        this.drawLine(this.originX,this.originY,this.canvas.width - this.cPadding,this.originY)
  
        // 画刻度
        this.drawMarker()
        this.drawBar()
  
        this.ctx.translate(-0.5,-0.5);
      }
      drawMarker(){
        // 画刻度
        // 画 Y轴
        let oneYVal = this.yAxisH / this.yAxisNum;
        this.ctx.textAlign = 'right';
        for(let i = 0; i <= this.yAxisNum;i++){
          // 写字
          this.ctx.fillText(i/10,this.originX - 10,this.originY - i * oneYVal + 5)
          if(i > 0 ){
            this.ctx.strokeStyle = '#3f3f3f'
            this.drawLine(this.originX,this.originY - i*oneYVal,this.originX - 5,this.originY - i*oneYVal)
            this.ctx.strokeStyle = 'black'
            this.drawLine(this.originX,this.originY - i*oneYVal,this.canvas.width - this.cPadding,this.originY - i*oneYVal)
          }
        }
  
        this.ctx.save();
        this.ctx.font = '25px Times New Romans'
        this.ctx.rotate(-Math.PI/2)
        this.ctx.fillText("Confidence",-this.canvas.height/2+60,20)
        this.ctx.restore()
  
        // 画X轴
        let oneXVal = this.xAxixW / this.xAxisNum;
        this.ctx.strokeStyle = '#3f3f3f';
        this.ctx.textAlign = 'center';
        for(let i = 0; i < this.xAxisNum; i++){
          this.ctx.fillText(this.data[i][0],this.originX + (i+1) * oneXVal - oneXVal/2,this.originY + 20)
          this.drawLine(this.originX + (i+1) * oneXVal,this.originY,this.originX + (i+1) * oneXVal,this.originY+5)
        }
        this.ctx.save();
        this.ctx.font = '25px Times New Romans'
        this.ctx.fillText("Probes",this.canvas.width/2,this.originY + 50)
        this.ctx.restore()
  
      }
      drawRect(x,y,w,h){
        this.ctx.beginPath();
        this.ctx.rect(x,y,w,h);
        let color = this.ctx.createLinearGradient(0,0,0,500);
        color.addColorStop(0,'#3f3f3f')
        color.addColorStop(0.5,'#3f3f3f')
        color.addColorStop(1,'#3f3f3f')
        this.ctx.fillStyle = color;
        this.ctx.strokeStyle = color;
        this.ctx.fill();
        this.ctx.closePath();
      }
      drawBar(){
        let oneXVal = this.xAxixW / this.xAxisNum;
        let barW = oneXVal/2;
        for(let i = 0; i < this.xAxisNum; i++){
          let barH = this.data[i][1]*this.yAxisH/1 * (this.count/100);
          let y = this.originY - barH;
          let x = this.originX + i * oneXVal + barW/2;
          this.drawRect(x,y,barW,barH)
          this.ctx.fillText(this.data[i][1],x+barW/2,y - 10)
        }
        this.animateID = requestAnimationFrame(()=>{this.animate()})
      }
      animate(){
        this.count ++;
        if(this.count <= 100){
          this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height)
          this.drawAxis()
        }else{
          this.count = 100
        }
      }
      bindEvent(){
        this.canvas.addEventListener('click',()=>{
          window.cancelAnimationFrame(this.animateID)
          this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height);
          this.count = 0;
          this.setData(this.data)
        })
      }
  }
  
  let bar = new BarChart('barChart');
  function data3(){
    var bar_linear0 = res(11);
    var bar_linear = bar_linear0();
    var bar_svm0 = res(10);
    var bar_svm = bar_svm0();
    var bar_tree0 = res(9);
    var bar_tree = bar_tree0();
    var bar_nn0 = res(12);
    var bar_nn = bar_nn0();
    var data3 = [["DT", Number(bar_tree)], ["KM", Number(bar_svm)], ["LM", Number(bar_linear)], ["NN", Number(bar_nn)]];
    return data3;
  }
  bar.setData(data3());
  
  
    class BarChart1{
      constructor(id){
        this.canvas = document.getElementById(id);
        // 创造绘画环境
        this.ctx = this.canvas.getContext('2d');
        
        this.setRatio()
        this.cPadding = 80;// 内边距
        this.yAxisH = this.canvas.height - this.cPadding * 2;// 纵轴的高度
        this.xAxixW = this.canvas.width  - this.cPadding * 2;// 横轴的宽度
        this.originX = this.cPadding;// 原点的横坐标
        this.originY = this.yAxisH + this.cPadding;//原点的纵坐标
        this.yAxisNum = 5;// 总左边分的段数
        this.xAxisNum = 0;// 横坐标的段数
        this.data = []// 存储传进来的数据
  
        this.count = 0;
      }
      init(){
        this.ctx.font = '20px Times New Romans'
        // 画一个坐标系
        this.drawAxis()
        this.bindEvent();
      }
      setData(ary){
        this.data = ary;
        this.xAxisNum = ary.length;
        this.init()
      }
      setRatio(){
        let device = window.devicePixelRatio || 1;
        let canDevice = this.ctx.backingStorePixelRatio || 1;
        let ratio = device/canDevice;
        let oldW = this.canvas.width,
            oldH = this.canvas.height;
        this.canvas.width = ratio *  oldW;   
        this.canvas.height = ratio *  oldH;  
        this.canvas.style.width = oldW + 'px';
        this.canvas.style.height = oldH + 'px'; 
      }
      drawLine(x,y,x2,y2){
        // xy 对应的其实坐标   x2y2对应终点坐标
        this.ctx.beginPath();
        this.ctx.lineWidth = 1;// 设置线的宽度1个像素
        this.ctx.moveTo(x,y)
        this.ctx.lineTo(x2,y2);
        this.ctx.stroke();
        this.ctx.closePath()
      }
      drawAxis(){
        this.ctx.translate(0.5,0.5);//把 canvas的坐标原点 设置到 0.5,0.5的位置；// 解决 线模糊的问题
  
        //定义一下线条的颜色
        this.ctx.strokeStyle = 'black';
        // 画y轴
        this.drawLine(this.originX,this.originY,this.originX,this.cPadding)
        // 画x轴
        this.drawLine(this.originX,this.originY,this.canvas.width - this.cPadding,this.originY)
  
        // 画刻度
        this.drawMarker()
        this.drawBar()
  
        this.ctx.translate(-0.5,-0.5);
      }
      drawMarker(){
        // 画刻度
        // 画Y轴
        let oneYVal = this.yAxisH / this.yAxisNum;
        this.ctx.textAlign = 'right';
        for(let i = 0; i <= this.yAxisNum;i++){
          // 写字
          this.ctx.fillText(i/10,this.originX - 10,this.originY - i * oneYVal + 5)
          if(i > 0 ){
            this.ctx.strokeStyle = '#3f3f3f'
            this.drawLine(this.originX,this.originY - i*oneYVal,this.originX - 5,this.originY - i*oneYVal)
            this.ctx.strokeStyle = 'black'
            this.drawLine(this.originX,this.originY - i*oneYVal,this.canvas.width - this.cPadding,this.originY - i*oneYVal)
          }
        }
  
        this.ctx.save();
        this.ctx.font = '25px Times New Romans'
        this.ctx.rotate(-Math.PI/2)
        this.ctx.fillText("Confidence",-this.canvas.height/2+60,20)
        this.ctx.restore()
  
        // 画X轴
        let oneXVal = this.xAxixW / this.xAxisNum;
        this.ctx.strokeStyle = '#3f3f3f';
        this.ctx.textAlign = 'center';
        for(let i = 0; i < this.xAxisNum; i++){
          this.ctx.fillText(this.data[i][0],this.originX + (i+1) * oneXVal - oneXVal/2,this.originY + 20)
          this.drawLine(this.originX + (i+1) * oneXVal,this.originY,this.originX + (i+1) * oneXVal,this.originY+5)
        }
        this.ctx.save();
        this.ctx.font = '25px Times New Romans'
        this.ctx.fillText("Type of NN",this.canvas.width/2,this.originY + 50)
        this.ctx.restore()
  
      }
      drawRect(x,y,w,h){
        this.ctx.beginPath();
        this.ctx.rect(x,y,w,h);
        let color = this.ctx.createLinearGradient(0,0,0,500);
        color.addColorStop(0,'#3f3f3f')
        color.addColorStop(0.5,'#3f3f3f')
        color.addColorStop(1,'#3f3f3f')
        this.ctx.fillStyle = color;
        this.ctx.strokeStyle = color;
        this.ctx.fill();
        this.ctx.closePath();
      }
      drawBar(){
        let oneXVal = this.xAxixW / this.xAxisNum;
        let barW = oneXVal/2;
        for(let i = 0; i < this.xAxisNum; i++){
          let barH = this.data[i][1]*this.yAxisH/1 * (this.count/100);
          let y = this.originY - barH;
          let x = this.originX + i * oneXVal + barW/2;
          this.drawRect(x,y,barW,barH)
          this.ctx.fillText(this.data[i][1],x+barW/2,y - 10)
        }
        this.animateID = requestAnimationFrame(()=>{this.animate()})
      }
      animate(){
        this.count ++;
        if(this.count <= 100){
          this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height)
          this.drawAxis()
        }else{
          this.count = 100
        }
      }
      bindEvent(){
        this.canvas.addEventListener('click',()=>{
          window.cancelAnimationFrame(this.animateID)
          this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height);
          this.count = 0;
          this.setData(this.data)
        })
      }
  }

  
  let bar1 = new BarChart1('barChart1');
  function data4(){
    var bar_cnn0 = res(15);
    var bar_cnn = bar_cnn0();
    var bar_rnn0 = res(14);
    var bar_rnn = bar_rnn0();
    var bar_gnn0 = res(13);
    var bar_gnn = bar_gnn0();
    var data4 = [["CNN", Number(bar_cnn)], ["RNN", Number(bar_rnn)], ["GNN", Number(bar_gnn)]];
    return data4;
  }
  bar1.setData(data4());