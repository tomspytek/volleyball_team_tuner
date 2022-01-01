import tkinter as tk

class Tuner(tk.Tk):
    
    def __init__(self):
        """Create court, buttons, relevant lists, and zones."""
        super().__init__()
        
        self.players = []
        self.bench = []
        
        
        self.geometry('1150x680')
        self.resizable(False, False)
        
        self.add_players = tk.LabelFrame(self)
        self.add_players.grid(row=0, column=2, sticky='e', pady = 5, padx = 9)
        self.add_label = tk.Label(self.add_players, text='Add Players:')
        self.add_label.grid(row=0,column=0)
        self.add_field = tk.Entry(self.add_players, bg='white')
        self.add_field.grid(row=0, column=1)
        self.add_btn = tk.Button(self.add_players, text='Add',
                                 command=self.add_player)
        self.add_btn.grid(row=0, column=2)
        self.add_field.bind('<Return>',lambda btn: self.add_player())
        
        self.rotate_btn = tk.Button(text='Rotate', width=55, 
                                    font='helvetica 16', bg ='gray',
                                    command=self.rotate)
        self.rotate_btn.grid(row=2, column=0, columnspan=3)
        self.reset_btn = tk.Button(text='Reset', command=self.reset)
        self.reset_btn.grid(row=0,column=3)
        
        
        #creating the court
        self.court = tk.Canvas(self,width=1050, height=550, bg='white')
        self.court.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        #drawing the boundary lines
        self.front = self.court.create_rectangle(100,50,850,200)
        self.back = self.court.create_rectangle(100,200,850,500)
        
        #creating the zones
        self.z1 = self.court.create_rectangle(600,200,850,500, width=0)
        self.z2 = self.court.create_rectangle(600,50,850,200, width=0)
        self.z3 = self.court.create_rectangle(350,50,600,200, width=0)
        self.z4 = self.court.create_rectangle(100,50,350,200, width=0)
        self.z5 = self.court.create_rectangle(100,200,350,500, width=0)
        self.z6 = self.court.create_rectangle(350,200,600,500, width=0)
        
        #listing the zones for location check loops
        self.zones = [self.z1,self.z2,self.z3,self.z4,self.z5,self.z6] 
        
        #key is zone number, value is player assigned to that zone
        self.occupied = {
            1:None,
            2:None,
            3:None,
            4:None,
            5:None,
            6:None
            }
        
        #locations to which players are bumped when rearranging
        self.bump_locs = {
            1:((self.court.coords(self.z1)[2]+self.court.coords(self.z1)[0])/2,
               ((self.court.coords(self.z1)[3]
                 +self.court.coords(self.z1)[1])/2)+170),
            2:((self.court.coords(self.z2)[2]+self.court.coords(self.z2)[0])/2,
               ((self.court.coords(self.z2)[3]
                 +self.court.coords(self.z2)[1])/2)-90),
            3:((self.court.coords(self.z3)[2]+self.court.coords(self.z3)[0])/2,
               ((self.court.coords(self.z3)[3]
                 +self.court.coords(self.z3)[1])/2)-90),
            4:((self.court.coords(self.z4)[2]+self.court.coords(self.z4)[0])/2,
               ((self.court.coords(self.z4)[3]
                 +self.court.coords(self.z4)[1])/2)-90),
            5:((self.court.coords(self.z5)[2]+self.court.coords(self.z5)[0])/2,
               ((self.court.coords(self.z5)[3]
                 +self.court.coords(self.z5)[1])/2)+170),
            6:((self.court.coords(self.z6)[2]+self.court.coords(self.z6)[0])/2,
               ((self.court.coords(self.z6)[3]
                 +self.court.coords(self.z6)[1])/2)+170)
            }
        
    def add_player(self):
        """Add a player to the court and generate button bindings."""
        player_name = self.add_field.get()
        #make sure player name is not an empty string
        if player_name != '' and len(self.players)<8:
            new_player = self.court.create_text(0,0,text=str(player_name), 
                                                font='helvetica 18')
            self.players.append(new_player)
            self.bench_player(new_player)
            self.court.tag_bind(new_player, '<Button-1>',
                                lambda event, player=new_player:
                                    self.select(event,player)
                                    )
            self.court.tag_bind(new_player, '<B1-Motion>', 
                                lambda event, player=new_player:
                                    self.mover(event,player)
                                    )
            self.court.tag_bind(new_player, '<ButtonRelease-1>',
                                lambda event, player=new_player:
                                    self.assign(event,player)
                                    )
            self.court.tag_bind(new_player, '<Button-3>',
                                lambda event, player=new_player:
                                    self.options(event,player)
                                    )
            self.add_field.delete(0,len(player_name))
            if len(self.players) == 8:
                self.add_btn.config(state='disabled')
            else:
                self.add_btn.config(state='normal')
            
    def bench_player(self, player):
        """Add a player to the bench."""
        add_x = 950
        add_y = 0
        if None in self.bench:
            spot = self.bench.index(None)
            add_y = 60+25*spot
            self.bench[spot] = player
            self.court.coords(player, add_x, add_y)
        else:
            add_y = 60+25*len(self.bench)
            self.bench.append(player)
            self.court.coords(player, add_x, add_y)

    def mover(self,e, player):
        """Move the player around the court."""
        self.court.coords(player,e.x,e.y)
        current_zone = self.get_zone(player)
        
        if current_zone is not None:
            self.bump(current_zone)
            self.snap(player, current_zone)
            
        for zone in self.zones:
            zindex = self.get_zindex(zone)
            occ = self.occupied[zindex]
            if zone != current_zone and occ is not None:
                self.snap(occ,zone)
                    
    def get_zone(self, player):
        """Return the zone the player is in. """
        tx = self.court.coords(player)[0]
        ty = self.court.coords(player)[1]
        
        for zone in self.zones:
            xl = self.court.bbox(zone)[0]
            yl = self.court.bbox(zone)[1]
            xh = self.court.bbox(zone)[2]
            yh = self.court.bbox(zone)[3]
            
            if tx > xl and ty > yl and tx < xh and ty < yh:
                return zone
                            
    def snap(self, player, zone):
        """Automatically move player to center of zone 
        when mouse moves player within zone."""
        zindex = self.zones.index(zone)+1
        sx = (self.court.coords(zone)[2]+self.court.coords(zone)[0])/2
        sy = (self.court.coords(zone)[3]+self.court.coords(zone)[1])/2
        self.court.coords(player,sx, sy)
       
    def bump(self, zone):
        """Move player to predefined bump_location outside the sidelines."""
        zindex = self.zones.index(zone)+1
        occ = self.occupied[zindex]
        if occ is not None:
            bx = self.bump_locs[zindex][0]
            by = self.bump_locs[zindex][1]
            self.court.coords(occ,bx,by)
        
    def get_zindex(self, zone):
        """Return index for use with the occupied dictionary."""
        return(self.zones.index(zone)+1)
    
    def select(self,event, player):
        """Remove player from zone or bench when selected."""
        current_zone = self.get_zone(player)
        if current_zone is not None:
            zindex = self.get_zindex(current_zone)
            self.occupied[zindex] = None
        if player in self.bench:
            bench_spot = self.bench.index(player)
            self.bench[bench_spot] = None

    def assign(self, event, player):
        """Assign player as value for zone key in occupied dict."""
        current_zone = self.get_zone(player)
        if current_zone is not None:
            zindex = self.get_zindex(current_zone)
            self.occupied[zindex] = player
        
    def rotate(self):
        """Mimic volleyball rotation by shifting players CW on the court."""
        first = self.occupied[1]
        for i in range(1,7):
            zone = self.zones[i-1]
            if i == 6:
                self.occupied[6] = first
            else:
                self.occupied[i] = self.occupied[i+1]
            if self.occupied[i] is not None:
                self.snap(self.occupied[i],zone)
        
    def options(self,event, player):
        """Crate right click menu options."""
        menu = tk.Menu(self.court, tearoff=False)
        menu.add_command(label="Delete", command=lambda p=player:
                         self.delete_player(p))
        menu.post(event.x_root, event.y_root)
        
    def delete_player(self,player):
        """Remove player from court, relevant lists, 
        and reactivate add button."""
        self.court.delete(player)
        self.players.remove(player)
        if player in self.bench:
            spot = self.bench.index(player)
            self.bench[spot] = None
        if len(self.players)<8:
            self.add_btn.config(state='normal')
        
    def reset(self):
        """Clear the court and relevant lists of players."""
        for player in self.players:
            self.court.delete(player)
        self.players = []
        self.bench = []
        self.add_btn.config(state='normal')
            
        
if __name__ == '__main__':
    tuner = Tuner()
    tuner.mainloop()