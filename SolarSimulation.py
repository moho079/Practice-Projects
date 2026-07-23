from vpython import *
import math

meters_per_pixel = 2
G_const = 1
FPS = 60
dt = 1 / FPS

def init_space():
    screen = canvas(title='Planets', width=1200, height=700, center=vector(0,0,0), background=color.black)
    axis_range = [-10 , 10]
    for line in range(axis_range[0] , axis_range[1]+1):
        curve(color=color.white, pos=[vector(line, 0, -10), vector(line, 0, 10)], radius=0.05)
    for line in range(axis_range[0] , axis_range[1]+1):
        curve(color=color.white, pos=[vector(-10, 0, line), vector(10, 0, line)], radius=0.05)
        
class Planets:
    def __init__(self, name , mass, position, color, radius, Vertical=0, Horizontal=0, velocity=0):
        self.mass = mass
        self.position = position  # in meters
        self.color = color
        self.name = name
        self.radius = radius
        if velocity != 0:
            self.angles = [math.radians(Vertical), math.radians(Horizontal)]
            dx = math.cos(self.angles[0]) * math.sin(self.angles[1])
            dy = math.sin(self.angles[0])
            dz = math.cos(self.angles[0]) * math.cos(self.angles[1])
            # velocity in m/s, so convert velocity input directly (velocity assumed in m/s)
            self.velocity = vector(dx, dy, dz) * velocity 
        else:
            self.velocity = vector(0, 0, 0)
        self.lable = label(pos=self.position + vector(0, self.radius + 0.5, 0), text=f"{self.name}", height=15)
        self.sphere = sphere(radius=self.radius, pos=self.position, color=self.color)
    def draw_planet(self):
        self.sphere.pos = self.position
        self.lable.pos = self.position + vector(0, self.radius + 0.5, 0)
        print(self.position)
    
    @staticmethod
    def find_distance_slope(first_position, second_position):
        # Both positions in meters
        slope = first_position - second_position  # vector difference (meters)
        distance = mag(slope)  # distance in meters
        return distance, slope
    
    def update(self, other_mass):
        #Get distance and slope vector (both in meters)
        distance, slope = Planets.find_distance_slope(other_mass.position, self.position)
        if distance <= self.radius + other_mass.radius:
            return 0
        distance = 1  
        force_mag = ((G_const * self.mass * other_mass.mass) / (distance ** 2)) 
        #Normalize slope vector to get direction
        force_dir = slope / distance  
        #Compute force vector 
        force_vec = force_dir * force_mag / meters_per_pixel
        acc = force_vec / self.mass
        self.velocity += acc * dt
        self.position += self.velocity * dt
        return 1
      
init_space()
#Central Planet
CentralPlanet_mass = 1
CentralPlanet_Pos = vector(0 , 5 , 0)
CentralPlanet_name = "Earth"
CentralPlanet_radius = 1
CentralPlanet_color = color.green
CentralPlanet = Planets(name= CentralPlanet_name ,mass = CentralPlanet_mass , position = CentralPlanet_Pos, color = CentralPlanet_color , radius = CentralPlanet_radius)

#Planet1
Planet1_mass = 0.0123
Planet1_Pos = vector(5 , 5 , -5)
Planet1_name = "Moon"
Planet1_vertical = 20
Planet1_horizontal = 50
Planet1_radius = 0.4
Planet1_color = color.white
Planet1_velocity = 2
Planet1 = Planets(name = Planet1_name ,mass = Planet1_mass , position = Planet1_Pos, color = Planet1_color , radius = Planet1_radius ,
                   velocity = Planet1_velocity , Vertical= Planet1_vertical, Horizontal= Planet1_horizontal)

while True:
    rate(FPS)    
    State = Planet1.update(CentralPlanet)
    if State == 0:
        Planet1.sphere.visible = False
    elif State == 1:
        Planet1.draw_planet()
        