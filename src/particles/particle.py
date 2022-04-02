from src.particles.flower import FlowerParticle

def flower_explosion(game, x, y):
    for i in range(20):
        game.particle_list.append(FlowerParticle(game, center_x=x, center_y=y))
