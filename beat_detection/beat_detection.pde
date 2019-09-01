import ddf.minim.*;
import ddf.minim.analysis.*;

Minim minim;
AudioPlayer song;

PrintWriter output;

boolean record;

String[] lines;

int[] time;

float d;

int nwm;

void setup()
{
  size(512, 200, P3D);
  
  record = true;
  
  d = 0;
  
  time = new int[0];
  
  nwm = -120;
  
  minim = new Minim(this);
  
  song = minim.loadFile("../Geoxor - Euphoria.mp3", 1024);
  song.play();
  song.skip(0);
  if(record){
    output = createWriter("data.txt");  
  }else{
    lines = loadStrings("data.txt");
  }
  
  
}

void draw()
{
  background(0);
  fill(255);
  text(song.position(),50,50);
  
  if(!record){
    
    for(int i = 0;i<lines.length;i++){
      if(song.position() > int(lines[i])-10+nwm && song.position() < int(lines[i])+10+nwm){
        d = 180;
      }else{
         d*=0.99; 
      }
    }
    
    fill(255,0,0);
    ellipse(width/2,height/2,d,d);
    
      
  }
  
}

void keyReleased(){
  
  if(key == ' ' && record){
    data();  
  }
  if(key == 'q'){
    output.flush();
    output.close();
    exit();
  }
}

void data(){
  output.print(song.position());
  output.print(", ");
  println(song.position());
}
