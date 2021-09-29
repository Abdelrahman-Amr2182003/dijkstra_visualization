import pygame
import math
import time as t
pygame.init()
INF = 9999999999999999999
class priority_queue:
    def __init__(self):
        self.queue = []  # of tuple

    def is_empty(self):
        if (len(self.queue) == 0):
            return True
        return False

    def insert(self, x):
        self.queue.append(x)

    def pop(self):
        minn = 0
        for i in range(0, len(self.queue)):
            if self.queue[i][0] < self.queue[minn][0]:
                minn = i
        item = self.queue[minn]
        del self.queue[minn]
        return item

class Game:
    def __init__(self):
        self.width=750
        self.height=750
        self.run=True
        self.white=(255,255,255)
        self.rows=50
        self.cols=50
        self.pixel_size=15
        self.black=(0,0,0)
        self.red=(255,0,0)
        self.src=(0,0)
        self.green=(0,255,0)
        self.blue=(0,0,255)
        self.start=0
        self.src_event=pygame.USEREVENT+1
        self.target_event=pygame.USEREVENT+2
        self.target=(self.rows,self.cols)
        self.grid=self.make_grid(self.rows,self.cols)
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_state = pygame.mouse.get_pressed()
        self.clock=pygame.time.Clock()
        self.win=pygame.display.set_mode((self.width,self.height))
        self.dis=[]
        self.par=[]
        self.purpel=(230,36,250)
        pygame.display.set_caption("diskestra visualization")
    def make_grid(self,r,c):
        grid=[]
        for i in range(r):
            grid.append([])
            for _ in range(c):
                grid[i].append(0)
        return grid

    def make_dis(self,r,c):
        dis=[]
        for i in range(r):
            dis.append([])
            for _ in range(c):
                dis[i].append(INF)
        return dis

    def draw_grid(self,draw_lines):
        for i in range(self.rows):
            for j in range(self.cols):
                clrs=[self.white,self.black]
                rec=pygame.Rect(j*self.pixel_size,i*self.pixel_size,self.pixel_size,self.pixel_size)
                if self.mouse_state[0]==1 and self.mouse_state[2]==1:
                    x, y = self.mouse_pos
                    mouse_rec = pygame.Rect(x, y, 1, 1)
                    if mouse_rec.colliderect(rec):
                        self.src=(i,j)
                if self.mouse_state[1]==1 and self.mouse_state[2]==1:
                    x, y = self.mouse_pos
                    mouse_rec = pygame.Rect(x, y, 1, 1)
                    if mouse_rec.colliderect(rec):
                        self.target=(i,j)

                if self.mouse_state[0]==1 and (i,j)!=self.src and (i,j)!=self.target:
                    x,y=self.mouse_pos
                    mouse_rec=pygame.Rect(x,y,1,1)
                    if mouse_rec.colliderect(rec):
                        self.grid[i][j]=1

                try:
                    if self.mouse_state[2] == 1:
                        x, y = self.mouse_pos
                        mouse_rec = pygame.Rect(x, y, 1, 1)
                        if mouse_rec.colliderect(rec):
                            self.grid[i][j] = 0


                except:
                    if self.mouse_state[1] == 1:
                        x, y = self.mouse_pos
                        mouse_rec = pygame.Rect(x, y, 1, 1)
                        if mouse_rec.colliderect(rec):
                            self.grid[i][j] = 0


                color=clrs[self.grid[i][j]]
                if (i,j)==self.src:
                    color=self.green
                if (i,j)==self.target:
                    color=self.red
                pygame.draw.rect(self.win,color,(j*self.pixel_size,i*self.pixel_size,self.pixel_size,self.pixel_size))
        if draw_lines:
            for i in range(self.rows):
                pygame.draw.line(self.win,self.black,(0,i*self.pixel_size),(self.width,i*self.pixel_size))
            for j in range(self.cols):
                pygame.draw.line(self.win,self.black,(j*self.pixel_size,0),(j*self.pixel_size,self.height))

    def eucledian(self,r1,r2,c1,c2):
               return math.sqrt((r1-r2)**2+(c1-c2)**2)
    def valid(self,i,j):
        if(i>=0 and j>=0 and i<self.rows and j<self.cols):
            #sprint(i,j)
            if self.grid[i][j]!=1:
                return True

        return False
    def get_neighbors(self,i,j):
        n=[]
        h=[0,1,0,-1,1,1,-1,-1]
        v=[1,0,-1,0,1,-1,1,-1]
        for t in range(len(h)):
            if self.valid(i+v[t],j+h[t]):
                #sprint(i+v[t],j+h[t])
                n.append((i+v[t],j+h[t]))

        return n
    def dijkstra(self):
        self.dis=self.make_dis(self.rows,self.cols)
        self.par=self.make_grid(self.rows,self.cols)
        self.dis[self.src[0]][self.src[1]]=0
        q=priority_queue()
        q.insert((0,self.src[0],self.src[1]))
        self.par[self.src[0]][self.src[1]]=(-1,-1)
        while(q.is_empty() is not True ):
            c,u,k=q.pop()
            n=self.get_neighbors(u,k)

            if((u,k)==self.target):
                return c

            #print(u,k,"   ",n)
            for i in n:
                vr,vc=i
                w=self.eucledian(u,vr,k,vc)
                if(self.dis[vr][vc]>self.dis[u][k]+w):
                    self.dis[vr][vc]=self.dis[u][k]+w
                    self.par[vr][vc]=(u,k)
                    q.insert((w,vr,vc))

                    #pygame.draw.rect(self.win, self.purpel,
                    #                (vc * self.pixel_size, vr * self.pixel_size, self.pixel_size, self.pixel_size))

        return -1




    def main(self):
        while self.run:
            self.clock.tick()
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_state = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    return
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_s:
                        self.start=1
                    if event.key ==pygame.K_c:
                        self.dis=[]
                        self.grid=self.make_grid(self.rows,self.cols)
                        self.par=[]
                        self.src=(0,0)
                        self.start=0
                        self.target=(self.rows,self.cols)



            #draw
            self.win.fill(self.white)
            self.draw_grid(True)
            #print(self.src, "   ", self.target)
            if(self.start==1):
                d=self.dijkstra()
                if(d==-1):
                    pass
                else:
                    #reconstruct path
                    j=self.target
                    path=[]
                    while(j!=(-1,-1)):
                        path.append(j)
                        j=self.par[j[0]][j[1]]

                    for P in path:
                        r,c=P
                        if((r,c)!=self.src and (r,c)!=self.target):
                            pygame.draw.rect(self.win,self.blue,(c*self.pixel_size,r*self.pixel_size,self.pixel_size,self.pixel_size))
                        #print(path)

            pygame.display.update()


if __name__ == '__main__':
    mygame = Game()
    mygame.main()
