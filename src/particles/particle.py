from src.particles.flower import FlowerParticle
from src.particles.smoke import SmokeParticle

def flower_explosion(game, x, y, n_flowers=20, muted=False):
    for i in range(n_flowers):
        game.particle_list.append(FlowerParticle(game, center_x=x, center_y=y))
    if not muted:
        game.ass.play_sound("explosion")

def smoke(game, x, y):
    game.particle_list.append(SmokeParticle(game, center_x=x, center_y=y))
