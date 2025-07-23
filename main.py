from vpython import *
import math

#GLOBAL STATIC 
gravity = 9.8

class Ball:
    def __init__(self , mass , radius , position , force , drag_c , elasticity , color ,fps):
        self.dt = 1 / fps
        self.radius = radius
        self.position = position
        self.mass = mass
        self.weight = mass * gravity
        self.acc = force / self.mass * self.dt
        self.drag = drag_c * self.dt
        self.friction = self.drag * self.weight * self.dt
        self.elasticity = elasticity
        self.color = color
        self.sphere = sphere(radius=self.radius, pos=self.position, color=self.color)

    def draw_ball(self):
        self.sphere.pos = self.position

    def init_postion(self , vertical_angle, horizontal_angle):
        v_angle = math.radians(vertical_angle)
        h_angle = math.radians(horizontal_angle)
        
        dx = math.cos(v_angle) * math.sin(h_angle) 
        dy = math.sin(v_angle) 
        dz = math.cos(v_angle) * math.cos(h_angle) 
        
        #if downwards a
        if math.sin(v_angle) > 0 :
            vy = (self.acc * dy) 
        #if upwards -a
        elif math.sin(v_angle) < 0 :
            vy = (-self.acc * dy) 
        
        vx = self.acc * dx
        vz = self.acc * dz

        self.velocity = vector(vx, vy , vz) 
    
    def move_ball(self, velocity):
        # Apply gravity to the vertical component of the velocity
        velocity.y -= gravity * self.dt

        if self.position.y == dbound and velocity.y < 0.1:
            velocity.y = 0

        # Limit the vertical component of the position to the bounds
        self.position.y = max(dbound, min(ubound, self.position.y + (velocity.y * self.dt * 5)))

        if velocity.y != 0:
            # Limit the horizontal and depth components of the position to the bounds
            self.position.x = max(lbound, min(rbound, self.position.x + velocity.x))
            self.position.z = max(bbound, min(fbound, self.position.z + velocity.z))

        elif velocity.y == 0:
            # Apply friction to the horizontal component of the velocity
            if not math.isclose(velocity.x, 0, abs_tol=1e-3):
                if velocity.x > 0:
                    velocity.x -= self.friction * self.dt
                    if velocity.x < 0:
                        velocity.x = 0
                else:
                    velocity.x += self.friction * self.dt
                    if velocity.x > 0:
                        velocity.x = 0
            else:
                velocity.x = 0

            # Z-axis friction
            if not math.isclose(velocity.z, 0, abs_tol=1e-3):
                if velocity.z > 0:
                    velocity.z -= self.friction * self.dt
                    if velocity.z < 0:
                        velocity.z = 0
                else:
                    velocity.z += self.friction * self.dt
                    if velocity.z > 0:
                        velocity.z = 0
            else:
                velocity.z = 0


        print(f"Velocity X: {velocity.x} | Velocity Z : {velocity.z} | Velocity Y : {velocity.y}")

        # Update the horizontal and depth positions based on the velocity
        self.position.x = max(lbound, min(rbound, self.position.x + velocity.x))
        self.position.z = max(bbound, min(fbound, self.position.z + velocity.z))
        return self.position

def init_space(xAxis_pos , yAxis_pos , zAxis_pos , axis):
    screen = canvas(height = 900, width = 1500, background = color.white)

    xAxis = curve(color=color.black, pos=[vector(0,0,0), xAxis_pos] ,radius = 0.01)  # X-axis
    xLabel = label(pos = vector(10.5, 0 , 0) , text = 'X-axis', background= color.black , color=color.white)
    draw_grid(xAxis_pos, 'x' , axis)

    yAxis = curve(color=color.black, pos=[vector(0,0,0), yAxis_pos], radius = 0.01)  # Y-axis
    yLabel = label(pos = vector(0,10.5,0), text = 'Y-axis', background= color.black , color=color.white)
    draw_grid(yAxis_pos, 'y' , axis)

    zAxis = curve(color=color.black, pos=[vector(0,0,0), zAxis_pos], radius = 0.01)  # Z-axis
    zLabel = label(pos = vector(0,0,10.5), text = 'Z-axis', background= color.black , color=color.white)
    draw_grid(zAxis_pos, 'z' , axis)

    box(color = color.cyan , height = 10 , width = 10 , length = 0.01 , pos= vector(0 , 5 , 5))
    box(color = color.cyan , height = 10 , width = 0.01 , length = 10 , pos= vector(5 , 5 , 0))
    box(color = color.cyan , height = 0.01 , width = 10 , length = 10 , pos= vector(5 , 0 , 5))

    return xAxis_pos , yAxis_pos , zAxis_pos

def draw_grid(position, xyz , axis):
    label(text = '0, 0, 0' , pos = vector(0 , 0, 0) , background = color.black , color = color.white , height = 8)
    end  = axis
    for line in range(end + 1):
        match xyz:
            case 'x':
                curve(color=color.white, pos=[vector(line, 0, 0), vector(line, end, 0)], radius=0.008)
                curve(color=color.white, pos=[vector(0, line, 0), vector(end, line, 0)], radius=0.008)
                #label(color=color.white, text=f'{line},0,0', pos=vector(line , 0, -0.3),height=8 , background = color.black)
            case 'y':
                curve(color=color.white, pos=[vector(0, line, 0), vector(0, line, end)], radius=0.008)
                curve(color=color.white, pos=[vector(0, 0, line), vector(0, end, line)], radius=0.008)
                #label(color=color.white, text=f'0,{line},0', pos=vector(-0.3, line, 0),height=8 , background = color.black)
            case 'z':
                curve(color=color.white, pos=[vector(line, 0, 0), vector(line, 0, end)], radius=0.008)
                curve(color=color.white, pos=[vector(0, 0, line), vector(end, 0, line)], radius=0.008)
                #label(color=color.white, text=f'0,0,{line}', pos=vector(-0.3, 0, line),height=8 , background = color.black)

def reflect_vector(normal , vector):
    final_vector = vector - (2  * (vector.dot(norm(normal))) * normal)
    return final_vector

#Axis Initilization
xAxis_pos = vector(10,0,0)
yAxis_pos = vector(0,10,0)
zAxis_pos = vector(0,0,10)
axis = 10

#Set the space
init_space(xAxis_pos ,yAxis_pos ,zAxis_pos , axis)

"""Ball Properties"""
#With X axis 
vertical_angle = 80
#With Z axis
horizontal_angle = 90
#Force
force = 100
#Fps
fps = 60
#Mass
mass = 2.5
#Ball radius
radius = 1
#Ball position
position = vector(7 , 8 , 5)
#Drag coefficient
drag = 0.25
#Ball elasticity
elasticity = 0.9
#Create Ball
ball = Ball(mass=mass , radius= radius , position= position , force= force , drag_c= drag , elasticity = elasticity ,color=color.green ,fps=fps)
#Intiliaze Velocity (Once at the start of the program)
ball.init_postion(vertical_angle , horizontal_angle)

"""Boundries of The 3d Space"""
lbound = xAxis_pos.y + ball.radius
rbound = xAxis_pos.x - ball.radius

dbound = yAxis_pos.x + ball.radius
ubound = yAxis_pos.y - ball.radius

fbound = zAxis_pos.z - ball.radius
bbound = zAxis_pos.x + ball.radius

#Normals Used For Reflection
normal = {"up" : vector(0,1,0) , 
          "down" : vector(0,-1,0) , 
          "right" : vector(1,0,0) , 
          "left" : vector(-1,0,0) , 
          "front" : vector(0,0,1) , 
          "back" : vector(0,0,-1) }

while True:
    #FPS 
    rate(fps)
    #Draw Ball (Position of ball used at first)
    ball.draw_ball()
    #Velocity Update (Gravity + Drag), then update position of the ball for (draw_ball) 
    ball.move_ball(ball.velocity)

    #Bounce Check, if ball touches a wall, reflect_vector is called which reflects the vector across the plane, depending on the normal
    if ball.position.x >= rbound and ball.velocity.x > 0:
        ball.velocity = reflect_vector(normal['right'], ball.velocity)
        ball.velocity.x *= ball.elasticity
    elif ball.position.x <= lbound and ball.velocity.x < 0:
        ball.velocity = reflect_vector(normal['left'], ball.velocity)
        ball.velocity.x *= ball.elasticity

    elif ball.position.y >= ubound and ball.velocity.y > 0:
        ball.velocity = reflect_vector(normal['up'], ball.velocity)
        ball.velocity.y *= ball.elasticity
    elif ball.position.y <= dbound and ball.velocity.y < 0:
        ball.velocity = reflect_vector(normal['down'], ball.velocity)
        ball.velocity.y *= ball.elasticity
    
    elif ball.position.z <= bbound and ball.velocity.z < 0:
        ball.velocity = reflect_vector(normal['back'], ball.velocity)
        ball.velocity.z *= ball.elasticity
    elif ball.position.z >= fbound and ball.velocity.z > 0:
        ball.velocity = reflect_vector(normal['front'], ball.velocity)
        ball.velocity.z *= ball.elasticity
