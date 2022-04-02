from src.particles.flower import FlowerParticle
from src.particles.smoke import SmokeParticle

def flower_explosion(game, x, y):
    for i in range(20):
        game.particle_list.append(FlowerParticle(game, center_x=x, center_y=y))

def smoke(game, x, y):
    game.particle_list.append(SmokeParticle(game, center_x=x, center_y=y))
