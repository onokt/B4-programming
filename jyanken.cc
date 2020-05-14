#include<iostream>
#include<cstdio>
#include<cstdlib>
#include<ctime>
#include<string>
using namespace std;

class Character{
    string name;
    int skill=rand()%3;
public:
    Character(string s):name(s){};
    void win(){
        cout<<name<<" win!"<<endl;
    }
    void draw(){
        cout<<"This turn is draw"<<endl;
    }
    int Getskill() const{return skill;}

};

//Hero class
class Hero:public Character{
public:
    Hero(string h):Character(h){}
    void sword(){
        cout<<"Hero attacked with sword"<<endl;
    }
    void bow(){
        cout<<"Hero attacked with bow"<<endl;
    }
    void lance(){
        cout<<"Hero attacked with lance"<<endl;
    }
    void attack(){
    if(Getskill()==0) sword();
    
    else if(Getskill()==1) bow();
    
    else  lance();
    }

    };
    

//Monster class
class Monster:public Character{
public:
    Monster(string m):Character(m){};
    void fang(){
        cout<<"Monster attacked with fang"<<endl;
    }
    void claw(){
        cout<<"Monster attacked with claw"<<endl;
    }
    void tail(){
        cout<<"Monster attacked with tail"<<endl;
    }
    void attack(){
        if(Getskill()==0) fang();
        
        else if(Getskill()==1) claw();
        
        else tail();
    }
    void ult(){
        cout<<"Maou win invariably"<<endl;
    }
};

//Judge class
class Judger:public Character{
    int hero_win=0;
    int monster_win=0;
    int hero_mons_draw=0;
public:
    Judger(string s):Character(s){};
    int GetHero_win() const{return hero_win;}
    int GetMons_win() const{return monster_win;}
    int Get_draw() const{return hero_mons_draw;}

    void judge(){

        Hero *hero=new Hero("Yusya");
        Monster *monster=new Monster("Maou");
        hero->attack();
        monster->attack();
        
        int a=(hero->Getskill()-monster->Getskill()+3)%3;

        if(a==0) 
        {
            draw();
            hero_mons_draw++;
        }
        else if(a==1) 
        {
            hero->win();
            hero_win++;
        }
        else if(a==2) 
        {
            monster->win();
            monster_win++;
        }
        

        delete hero,monster;
    }

    };



int main(void)
{
    Monster *monster=new Monster("Maou");
    Judger *judger=new Judger("Judgeman");
    srand((unsigned)time(NULL));
    int Maou_ult_win=0;

    for(int i=0;i<1000;i++){
    cout<<"==============================="<<endl;
    if(i%5==0){
        monster->ult();
        Maou_ult_win++;
        
    }
    else{
        judger->judge();
    }

    cout<<"Yusya : "<<judger->GetHero_win()<<" "<<"Maou : "<<judger->GetMons_win()+Maou_ult_win<<" draw : "<<judger->Get_draw()<<endl;

    }
}