from math import atan2, degrees
from vector import Vector

class Boid:

    max_speed = 3
    max_force = 0.03

    separation_radius = 100
    neighbor_radius = 200

    separation_weight = 1
    alignment_weight = 1
    cohesion_weight = 1

    def __init__(self, position, velocity=Vector()):
        self.position = Vector(position)
        self.velocity = velocity

    @property
    def angle(self):
        return degrees(atan2(*reversed(self.velocity.coordinates)))

    def distance(self, other):
        return (other.position - self.position).magnitude

    def separation(self, others):
        return average([(self.position - other.position).normalize() / self.distance(other)
                        for other in others if self.distance(other) < self.separation_radius])

    def alignment(self, others):
        return average([other.velocity for other in others
                        if self.distance(other) < self.neighbor_radius]).limit(self.max_force)

    def cohesion(self, others):
        return average([other.position - self.position for other in others
                        if self.distance(other) < self.neighbor_radius]).limit(self.max_force)

    def update(self, flock):
        others = filter(lambda boid: boid is not self, flock)
        acceleration = (self.separation(others) * self.separation_weight +
                        self.alignment(others) * self.alignment_weight +
                        self.cohesion(others) * self.cohesion_weight)
        velocity = (self.velocity + acceleration).limit(self.max_speed)
        position = self.position + self.velocity
        return Boid(position, velocity)

def average(vectors):
    return sum(vectors) / len(vectors) if vectors else Vector()