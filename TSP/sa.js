/*
  Demonstracja dziaĹania algorytmu:
  symulowane wyĹźarzanie (SA)
  na problemie komiwojaĹźera (TSP)
  M.Makuchowski
*/

var nodeN=40;             // liczba miast
var node=[];              // dane instancji
var saPath=[];            // rozwiÄzanie
var saDataDist=[];        // dane wykresu Dist
var saDataPraw=[];        // dane wykresu Praw
var saDataTemp=[];        // dane wykresu Temp
var saBestDist;           // najlepsze znalezione rozwiazanie (Dist)
var saBestPath;           // najlepsze znalezione rozwiazanie (path)
var saTempStart=10000;    // temperatura Startowa
var saTempAlpha=0.976;    // wspĂłĹczynnik zmiany temperatury
var saTemp;               // bieĹźÄca temperatura

var loopN=0;              // ile pozostalo krokĂłw do wykonania
var loopDelay=10;         // opoĹşnienie pÄtli

////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
////                                                    ////
////  GĹĂłwna pÄtla programu                             ////
////                                                    ////
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////

function Run()
{
  var startPath= RandPath();
  var startDist= PathDist(startPath);
  saPath= Array.from(startPath);
  saDataDist=[]; saDataDist.push(startDist);
  saBestDist=startDist; saBestPath= Array.from(startPath);

  loopN=400;
  saTemp=saTempStart;
  saDataTemp=[];
  saDataPraw=[];
  Loop();
}

function Loop()
{
  if(loopN==0)return;
  loopN--;
  SaStep( saPath, saTemp );
  saTemp = saTemp*saTempAlpha;
  if(loopN==0)
  { //w ostatnim kroku algorytmu wyĹwietlam najlepszr rozwiÄzanie
    saDataDist.push( saBestDist );
    saPath= saBestPath;
  }
  Draw();
  setTimeout(Loop,loopDelay);
}

//////////////////////////////////////////////////////////////
//                         SA                               //
//////////////////////////////////////////////////////////////
function SaStep(path,temp)
{
  var c0 = PathDist(path);
  var praw=0,akce=0;
  for(var i=0; i<100; i++)
  {
    var move = RandAB();
    PathMove( path, move );
    var c1 = PathDist(path);
    if(c1>c0)
    { praw = Math.exp( (c0-c1)/temp );
      akce = ( Math.random()<praw );
    }
    if(c1<=c0||akce)  c0=c1; //akceptuje ruch
    else     PathMove( path,move ); //odrzucenie ruchu
    if(saBestDist>c0)
    {
      saBestDist=c0;
      saBestPath=Array.from( path );
    }
  }
  saDataDist.push( c0 );
  saDataTemp.push( saTemp );
  saDataPraw.push( [praw,akce] );
}

//////////////////////////////////////////////////////////////
// inne                                                     //
//////////////////////////////////////////////////////////////
function RandAB()
{
  var a=Math.floor(Math.random()*node.length);
  var b=Math.floor(Math.random()*(node.length-1)); if(b>=a)b++;
  if(a>b) [a,b]=[b,a];
  return [a,b];
}

function PathMove(path,move)
{
  var a=move[0], b=move[1];
  while(a<b){[path[a],path[b]]=[path[b],path[a]]; a++;b--;}
}

function PathDist(path)
{
  var dist=0;
  for(var i=0; i<path.length; i++)
  { var n0 = path[i];
    var n1 = path[(i+1)%path.length];
    var x0 = node[n0][0];
    var y0 = node[n0][1];
    var x1 = node[n1][0];
    var y1 = node[n1][1];
    dist += Math.round(Math.sqrt((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1)));
  }
  return dist;
}

function NodeRand()
{
  loopN=0;
  node=[];
  saPath=[]; saBestPath=[];
  saDataDist=[]; saDataPraw=[]; saDataTemp=[];
  for(i=0;i<nodeN;i++)
    node.push([ Math.floor(Math.random()*400), Math.floor(Math.random()*200) ]);
  Draw();
}

//////////////////////////////////////////////////////////////
//            Losowanie rozwiazania startowego              //
//////////////////////////////////////////////////////////////
function RandPath()
{
  var path=[];
  for( i=0; i<node.length; i++) path.push(i);
  for (let i = path.length - 1; i > 0; i--)
  { const j = Math.floor(Math.random()*i+1 );
    [path[i], path[j]] = [path[j], path[i]];
  }
  return path;
}

///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
////                                                  /////
////  Grafika                                         /////
////                                                  /////
///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////

function NodeXY(id)
{
  var scale=   1;
  var shiftX=  20;
  var shiftY=  20;
  return [ shiftX+scale*node[id][0], shiftY+scale*node[id][1] ];
}
function SvgKrata()
{
  svg="";
  svg+='<g style="stroke: #242424; stroke-width:1; fill: none;">';
  svg+='<path d="M 20 20';
  for(var i=0;i<25;i++)svg+='m -10 0, l 420 0, m -410 8';
  svg+='M 20 20';
  for(var i=0;i<50;i++)svg+='m 0 -10, l 0 220, m 8 -210';
  svg+='"/></g>';

  svg+='<g style="stroke: #2e2e2e; stroke-width:1; fill: none;">';
  svg+='<path d="M 20 20';
  for(var i=0;i<=5;i++)svg+='m -10 0, l 420 0, m -410 40';
  svg+='M 20 20';
  for(var i=0;i<=10;i++)svg+='m 0 -10, l 0 220, m 40 -210';
  svg+='"/></g>';
  return svg;
}

function SvgPath(path)
{
  var svg = '<svg width="440" height="240">';
  svg+=SvgKrata();
  if(path.length>0)
  { //Path
    svg+='<g style="stroke: #cc7; stroke-width:3; fill: none; stroke-linejoin:bevel ">';
    var x,y; [x,y] = NodeXY(path[0]);
    svg+='<path d="M '+x+' '+y;
    for(var i=1; i<path.length; i++ )
    { [x,y]= NodeXY(path[i]);
      svg+=', L '+x+' '+y;
    } svg+=',Z"/></g>';
  }
  //Node
  for(var i=0; i<node.length; i++ )
  { [x,y]= NodeXY(i);
    svg+='<circle cx="'+x+'" cy="'+y
       +'" r="4" stroke=none fill=#474 />'
  }
  svg+='</svg>';
  return svg;
}

function SvgDataDist(data)
{
  var svg= '<svg width="440" height="240">';
  svg+=SvgKrata();
  svg+='<line x1="10" y1="220" x2="430" y2="220" style="stroke:#707070;stroke-width:1" />';
  svg+='<line x1="20" y1="230" x2="20"  y2="10" style="stroke:#707070;stroke-width:1" />';

  if(data.length>0){
    var scala = 160/data[0];
    svg+='<g style="stroke: #c0c070; stroke-width:2; fill: none;">';
    svg+='<path d="M 20 60';
    for(var i=1;i<data.length;i++)
      svg+=',L '+(20+i)+' '+(220-scala*data[i]);
    svg+='"/></g>';
    svg+='<text x="350" y="35" fill="#707070" font-size="16" >'+
          +(data[data.length-1])+'</text>';
  }
  svg+='</svg>';
  return svg;
}

function SvgDataPraw(data)
{
  var svg= '<svg width="440" height="240">';
  svg+=SvgKrata();
  svg+='<line x1="10" y1="220" x2="430" y2="220" style="stroke:#707070;stroke-width:1" />';
  svg+='<line x1="20" y1="230" x2="20"  y2="10" style="stroke:#707070;stroke-width:1" />';

  for(var i=0;i<data.length;i++)
    if(data[i][1]) svg+='<circle cx="'+(20+i)+'" cy="'+(220-200*data[i][0])
                      +'" r="1.5" stroke=#447744 stroke-width="1" fill=#447744 />';
    else           svg+='<circle cx="'+(20+i)+'" cy="'+(220-200*data[i][0])
                      +'" r="1.5" stroke=#bb6666 stroke-width="1" fill=#bb6666 />';
  //if(data.length>0) svg+='<text x="320" y="45" fill="#707070" font-size="12" >'
  //+(Math.round(100*data[data.length-1][0]))+'%</text>';
  svg+='</svg>';
  return svg;
}

function SvgDataTemp(data)
{
  var svg= '<svg width="440" height="240">';
  svg+=SvgKrata();
  svg+='<line x1="10" y1="220" x2="430" y2="220" style="stroke:#707070;stroke-width:1" />';
  svg+='<line x1="20" y1="230" x2="20"  y2="10" style="stroke:#707070;stroke-width:1" />';

  if(data.length>0){
    var scala = 200/data[0];
    svg+='<g style="stroke: #c0c070; stroke-width:2; fill: none;">';
    svg+='<path d="M 20 20';
    for(var i=1;i<data.length;i++)
      svg+=',L '+(20+i)+' '+(220-scala*data[i]);
    svg+='"/></g>';
    svg+='<text x="350" y="35" fill="#707070" font-size="16" >'+
          +(Math.round(100*data[data.length-1])/100)+'</text>';
  }
  svg+='</svg>';
  return svg;
}

function Draw()
{
  document.getElementById("pathSvg").innerHTML=SvgPath(saPath);
  document.getElementById("distSvg").innerHTML=SvgDataDist(saDataDist);
  document.getElementById("tempSvg").innerHTML=SvgDataTemp(saDataTemp);
  document.getElementById("prawSvg").innerHTML=SvgDataPraw(saDataPraw);
}

///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
////                                                  /////
////  Start strony                                    /////
////                                                  /////
///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////

function Init()
{
  document.onselectstart = function(){return false;};
  document.getElementById('rand').addEventListener('click',NodeRand);
  document.getElementById('run').addEventListener('click',Run);

  document.getElementById('path').innerHTML= '<div id="pathTxt">ĹcieĹźka</div> <div id="pathSvg">path:svg</div>';
  document.getElementById('dist').innerHTML= '<div id="distTxt">dĹugoĹÄ</div> <div id="distSvg">dist:svg</div>';
  document.getElementById('praw').innerHTML= '<div id="prawTxt">prawdopodobieĹstwo</div> <div id="prawSvg">praw:svg</div>';
  document.getElementById('temp').innerHTML= '<div id="tempTxt">temperatura</div> <div id="tempSvg">temp:svg</div>';
  NodeRand();
}

Init();