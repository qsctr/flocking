from vector import average, Vector

class Boid:

    max_speed = 4
    max_force = 0.05

    separation_radius = 100
    neighbor_radius = 200

    separation_weight = 5
    alignment_weight = 1
    cohesion_weight = 1

    speed_multiplier = 1

    width = 40
    height = 20
    color = 255, 255, 255

    def __init__(self, position, velocity=(0, 0)):
        self.position = Vector(position)
        self.velocity = Vector(velocity)

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

    def mouse(self, mouse_pos):
        if mouse_pos is None:
            return Vector()
        difference = Vector(mouse_pos) - self.position
        return difference.normalize() / max(difference.magnitude, 100)

    def update(self, flock, mouse_pos):
        others = list(filter(lambda boid: boid is not self, flock))
        velocity = (self.velocity +
                    self.separation(others) * self.separation_weight +
                    self.alignment(others) * self.alignment_weight +
                    self.cohesion(others) * self.cohesion_weight +
                    self.mouse(mouse_pos) * 20
                    ).limit(self.max_speed) * self.speed_multiplier
        position = self.position + velocity
        return Boid(position, velocity)
