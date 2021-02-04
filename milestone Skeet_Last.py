"""
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Skeet New Game"

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 5
BULLET_COLOR = arcade.color.GREEN
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 25

class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        
class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0

class FlyingObjects:
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0
        self.color = None
        self.alive = True
        
    def draw(self):
        arcade.draw_circle_outline(self.center.x,self.center.y,self.radius,self.color)
        
    def advance(self):
        self.center.y += self.velocity.dy
        self.center.x += self.velocity.dx
        #print("x = " + self.center.x + "y= " + self.center.y)
        
    def is_off_screen(self,w,h):
        if self.center.x > w or self.center.x < 0 or self.center.y > h or self.center.y < 0:
            return True
        else:
            return False
class Bullet(FlyingObjects):
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.color = BULLET_COLOR
        self.angle = 90
        self.time = 0
        
    def draw(self):
        arcade.draw_circle_filled(self.center.x,self.center.y,self.radius,self.color)

    def fire(self,angle):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        self.center.x = RIFLE_WIDTH * math.cos(math.radians(angle))
        self.center.y = RIFLE_WIDTH * math.sin(math.radians(angle))
        
    def advance(self):
        super().advance()
        
        
class Target(FlyingObjects):
    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(0,SCREEN_WIDTH/2)
        self.center.y = random.uniform(SCREEN_HEIGHT,SCREEN_HEIGHT/2)
        self.velocity.dx = random.uniform(1,5)
        self.velocity.dy = random.uniform(-2,5)
        self.color = TARGET_COLOR
        self.radius = TARGET_RADIUS
        self.score = 0
        self.lives = 5
        
    def draw(self):
        #arcade.draw_arc_outline(self.center.x,self.center.y,15,15,self.color,0,90)
        #arcade.draw_arc_outline(self.center.x + 10,self.center.y,15,15,self.radius,90,180)
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)
        
    def hit(self):
        self.score = 1
        self.alive = False
        return self.score

class StrongTarget(Target):
    def __init__(self):    
        super().__init__()
        self.velocity.dx = random.uniform(1,3)
        self.velocity.dy = random.uniform(-2,3)
        self.color = TARGET_SAFE_COLOR
        self.radius = TARGET_SAFE_RADIUS
        self.score = 0
        self.lives = 'BYU'

    def draw(self):
        #arcade.draw_arc_outline(self.center.x,self.center.y,15,15,self.color,0,90)
        #arcade.draw_arc_outline(self.center.x + 10,self.center.y,15,15,self.radius,90,180)
        #arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)
        arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, TARGET_COLOR)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.lives), text_x, text_y, TARGET_COLOR, font_size=20)
        
    def hit(self):
        # do something with lives to increment scofe
        self.score += 1;
        ## self.alive only gets set to false when lives is 0
        ##self.alive = False
        return self.score        
        


class SafeTarget(Target):
    def __init__(self):
        super().__init__()
        self.color = TARGET_SAFE_COLOR
        self.radius = TARGET_SAFE_RADIUS
        self.score = 0
        
    def hit(self):
        self.score = -10
        self.alive = False
        return self.score



### Remove one of these.
class SafeTarget(Target):
    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(SCREEN_WIDTH,SCREEN_WIDTH)
        self.center.y = random.uniform(SCREEN_HEIGHT/2,SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(-1,-3)
        self.velocity.dy = random.uniform(-1,-3)
        self.color = TARGET_SAFE_COLOR
        self.radius = TARGET_SAFE_RADIUS
        self.score = 0
        
    def hit(self):
        self.score = -10
        self.alive = False
        return self.score



class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 0

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, 360 - self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height,title):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height,title)

        self.rifle = Rifle()
        self.score = 0
        

        self.bullets = []
        self.targets = []
        

        arcade.set_background_color(arcade.color.BLACK)
        
    
        
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()
        start_x = 50
        start_y = 450
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 5)
        start_x = 150
        start_y = 350
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 7)
        start_x = 20
        start_y = 50
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 7)
        start_x = 750
        start_y = 350
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 7)
        start_x = 350
        start_y = 450
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 6)
        start_x = 50
        start_y = 240
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 7)
        start_x = 150
        start_y = 50
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 5)
        start_x = 750
        start_y = 50
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 7)
        start_x = 250
        start_y = 350
        arcade.draw_point(start_x, start_y, arcade.color.WHITE, 7)
        start_x = 450
        start_y = 250
        arcade.draw_text("Milestone Skeet",start_x, start_y, arcade.color.WHITE, 17)
        

        for bullet in self.bullets:
            bullet.draw()
            
        for tar in self.targets:
            tar.draw()

        # TODO: iterate through your targets and draw them...


        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()
            
        for target in self.targets:
            target.advance()

        # TODO: Iterate through your targets and tell them to advance

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        mynum = random.randint(1, 3);
        if mynum == 1:
            tar = Target()
        if mynum == 2:
            tar = SafeTarget()
        if mynum == 3:
            tar = StrongTarget()
            
        self.targets.append(tar)
        # TODO: Decide what type of target to create and append it to the list

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """
        

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        #print( "its a hit!")
                        bullet.alive = False
                        target.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
        
        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)
    
    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        # Fire!
        angle = self._get_angle_degrees(x, y)
        ##if button == angle:            
        ##     pass
        bullet = Bullet()
        bullet.fire(angle)
        self.bullets.append(bullet)
        
    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees



# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)

arcade.run()