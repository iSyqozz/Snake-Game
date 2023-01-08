#!/usr/bin/env python3
from tkinter import *
import time
from collections import deque
import random
import tracemalloc

def poly_roundrect(x, y, width, height, radius, canv, act,resolution=64):

    radius = min(min(width, height), radius*2)
    points = [x, y,
                x+radius, y,
                x+(width-radius), y,
                x+width, y,
                x+width, y+radius,
                x+width, y+(height-radius),
                x+width, y+height,
                x+(width-radius), y+height,
                x+radius, y+height,
                x, y+height,
                x, y+(height-radius),
                x, y+radius,
                x, y]
          
    rect = canv.create_polygon(points, outline='#1d6096' , fill = '#040817' , activefill = '#051a2b' if act else '#040817', smooth=True, splinesteps=resolution)
    return rect

#quitting
def Quit(e,root):
    print(tracemalloc.get_traced_memory())
    time.sleep(0.2)
    #root.destroy()

def get_speed(canv,e,m,h):
    time.sleep(0.2)
    vals = {e:150,m:100,h:40}
    for val in [e,m,h]:
        if canv.itemcget(val,'fill') == '#051a2b':
            return vals[val]


#start of application <Main Menu>
def run():
    print(tracemalloc.get_traced_memory())
    
    #start window
    root = Tk()
    root.config(bg = '#9dd1fc')
    root.resizable(False,False)
    root.geometry('500x500')
    root.title('Snake Game')

    start_menu = Frame(master = root , bg = '#040817' )
    
    #title and author
    title = Label(master = start_menu,bg ='#040817',text = 'Snake Game' , font=('Adobe Heiti Std R',25),fg = '#9dd1fc')
    title.pack(side = TOP,pady=(5,0))
    author = Label(master = start_menu,bg ='#040817',text = 'Game By Fares Hassen' , font=('Adobe Heiti Std R',12),fg = '#9dd1fc')
    author.pack(side = TOP,pady=(0,2))
    
    
    #Play Button
    play_canvas = Canvas(master = start_menu,cursor='hand2', width=125,height = 55 , bd = 0, highlightthickness=0,bg ='#040817' )
   
    play_canvas_oval = poly_roundrect(4,4,120,50,20,play_canvas,act=True)
    play_canvas.create_text(64,30,text = 'Launch',font=('Adobe Heiti Std R',20),fill ='#9dd1fc')
    play_canvas.bind('<Enter>', lambda e: play_canvas.itemconfig(play_canvas_oval,fill = '#051a2b'))
    play_canvas.bind('<Leave>', lambda e: play_canvas.itemconfig(play_canvas_oval,fill = '#040817'))
    play_canvas.bind('<ButtonPress-1>', lambda e: run_game(root,start_menu,get_speed(difficulty_canvas,easy,medium,hard)))

    play_canvas.pack(side = TOP,pady=(30,0))

    #Difficulty menu

    difficulty_canvas = Canvas(master = start_menu, width=360,height = 105 , bd = 0 , highlightthickness=0,bg ='#040817' )

    difficulty_canvas.create_text(183,30,text = 'Choose Difficulty:',font=('Adobe Heiti Std R',10),fill ='#9dd1fc')

    easy = poly_roundrect(12,50,100,40 ,20,difficulty_canvas,act = False)
    medium = poly_roundrect(132,50,100,40 ,20,difficulty_canvas,act=False)
    hard = poly_roundrect(252,50,100,40 ,20,difficulty_canvas,act=False)

    difficulty_canvas.itemconfig(easy,fill = '#051a2b' )
    for val in [easy,medium,hard]:
        difficulty_canvas.itemconfig(val,tag = 'choice')

    #Chossing a button
    def choose(e,m,h,ID,canv):
        #temp = [e,m,h]
        #for cand in temp:
        #    if ID == cand:
        #        canv.itemconfig(cand,fill = '#051a2b' ,activefill = '#051a2b')
        #    else:
        #        canv.itemconfig(cand,fill = '#040817' ,activefill = '#051a2b')
        temp = None
        print(tracemalloc.get_traced_memory())
    
    for ID in [easy,medium,hard]:
        difficulty_canvas.tag_bind(ID, '<ButtonPress-1>',lambda event,ID=ID: choose(easy,medium,hard,ID,difficulty_canvas))
        
    difficulty_canvas.create_text(62,70,text = 'Easy',font=('Adobe Heiti Std R',10),fill ='#9dd1fc',tags = 'choice')
    difficulty_canvas.create_text(182,70,text = 'Medium',font=('Adobe Heiti Std R',10),fill ='#9dd1fc',tags = 'choice')
    difficulty_canvas.create_text(302,70,text = 'Hard',font=('Adobe Heiti Std R',10),fill ='#9dd1fc',tags = 'choice')

    difficulty_canvas.tag_bind('choice','<Enter>',lambda e: difficulty_canvas.config(cursor = 'hand2'))
    difficulty_canvas.tag_bind('choice','<Leave>',lambda e: difficulty_canvas.config(cursor = ''))
    
    difficulty_canvas.pack(side = TOP,pady=(20,0))

    #Quit Button
    quit_canvas = Canvas(cursor='hand2',master = start_menu, width=125,height = 55 , bd = 0 , highlightthickness=0,bg ='#040817' )

    quit_canvas_oval = poly_roundrect(4,4,120,50,20,quit_canvas,act=True)
    quit_canvas.create_text(64,30,text = 'Quit',font=('Adobe Heiti Std R',20),fill ='#9dd1fc')
    quit_canvas.bind('<Enter>', lambda e: quit_canvas.itemconfig(quit_canvas_oval,fill = '#051a2b'))
    quit_canvas.bind('<Leave>', lambda e: quit_canvas.itemconfig(quit_canvas_oval,fill = '#040817'))

    quit_canvas.bind('<Button>', lambda e: Quit(e,root))

    quit_canvas.pack(side = TOP,pady=(30,0))

    start_menu.pack(fill = BOTH,expand = 1,padx=1,pady=1)


    #main game
    def run_game(root,start_menu,speed):


        print(tracemalloc.get_traced_memory())

        start_menu.pack_forget()
        #game frame
        game_frame = Frame(master = root , bg = '#040817')
        game_frame.pack(fill = BOTH,expand = 1,padx=1,pady=1)


        #score
        score = Label(master = game_frame,bg ='#040817',text = 'Score: 0 ' , font=('Adobe Heiti Std R',15),fg = '#9dd1fc')
        score.pack(side = TOP,pady=(5,0),padx=(10,0))

        #game canvas
        game_canv = Canvas(master = game_frame, width=400,height = 400,bd = 0 , highlightthickness=0,bg = '#040817')

        # getting direction info from input
        mapping = {'<Left>':(0,-1),'<Right>':(0,1),'<Up>':(-1,0),'<Down>':(1,0)}
        curr_dir = [(-1,0)]

        def change_dir(e,curr_dir,mapping,arrow):
            a,b = curr_dir[0] ; c,d = mapping[arrow]
            new = (a+c,b+d)
            curr_dir[0] = mapping[arrow] if new != (0,0) else curr_dir[0]
        
        for arrow in ['<Left>','<Right>','<Up>','<Down>']:
            root.bind_all(arrow,lambda e,arrow=arrow: change_dir(e,curr_dir,mapping,arrow) )
        job = [None]
        def move(canvas,q,curr_dir,mat,root,speed,empty,score,job):
            x1,y1 = q[0]
            dx,dy = curr_dir[0]
            next_slot = ((x1+dx)%40,(y1+dy)%40)
            gameover = False
            if canvas.itemcget(mat[next_slot[0]][next_slot[1]],'fill') == '#ad0f07':
                new_score = str(int(score['text'].split(':')[1])+1)
                score.config(text = f'Score:{new_score}')
                
                new_apple = random.sample(empty,1)[0]
                game_canv.itemconfig(mat[new_apple[0]][new_apple[1]],fill = '#ad0f07')
                
                q.appendleft(next_slot)
                empty.remove(next_slot)
                canvas.itemconfig(mat[q[0][0]][q[0][1]],fill = '#9dd1fc')
            
            elif next_slot in empty:

                q.appendleft(next_slot)
                empty.remove(next_slot)
                canvas.itemconfig(mat[q[0][0]][q[0][1]],fill = '#9dd1fc')
                prev = q.pop()
                empty.add(prev)
                canvas.itemconfig(mat[prev[0]][prev[1]],fill = '#041436')

            elif next_slot not in empty:
                gameover=True
                root.winfo_children()[1].destroy()
                root.winfo_children()[0].pack(fill = BOTH,expand = 1,padx=1,pady=1)
                canvas.after_cancel(job[0])

            if not gameover:

                job[0] = canvas.after(speed, lambda: move(canvas,q,curr_dir,mat,root,speed,empty,score,job))

             

        #creating the grid for the game and saving the coordinates
        
        mat = [[0]*40 for _ in range(40)]        
        y=0
        for i in range(40):
            x=0
            for j in range(40):
                mat[i][j] = game_canv.create_rectangle(x,y,x+10,y+10,fill = '#041436')
                x+=10
            y+=10

        q = deque([(20,26),(21,26),(22,26)])

        empty = {(i,j) for i in range(40) for j in range(40) if (i,j) not in q}
        init_apple = random.sample(empty,1)[0]
        game_canv.itemconfig(mat[init_apple[0]][init_apple[1]],fill = '#ad0f07')
        
        for i,j in q:
            game_canv.itemconfig(mat[i][j],fill = '#9dd1fc' )


        game_canv.pack(side=TOP,pady=(8,0))

        help = Label(master = game_frame,bg ='#040817',text = 'Movement: ← ↑ → ↓ Keys ' , font=('Adobe Heiti Std R',15),fg = '#9dd1fc')
        help.pack(side = BOTTOM,pady=(0,20))
        
        move(game_canv,q,curr_dir,mat,root,speed,empty,score,job)
    root.mainloop()



if __name__ == '__main__':
    tracemalloc.start()
    run()