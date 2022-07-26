"""Example with training on SB3"""

import numpy as np
from stable_baselines3 import PPO
from xland import make_env

from simenv import ParallelSimEnv


ALICIA_UNITY_BUILD_URL = "/home/alicia/github/simenv/integrations/Unity/builds/simenv_unity.x86_64"


# TODO: check if seeding works properly and maybe migrate to using rng keys
if __name__ == "__main__":
    n_parallel = 1
    seed = 10
    np.random.seed(seed)

    example_map = np.load("benchmark/examples/example_map_01.npy")
    env_fn = make_env(
        executable=None,
        sample_from=example_map,
        engine="Unity",
        seed=None,
        n_agents=1,
        n_objects=6,
        width=6,
        height=6,
    )

    env = ParallelSimEnv(env_fn=env_fn, n_parallel=n_parallel)
    obs = env.reset()
    model = PPO("CnnPolicy", env, verbose=3)
    model.learn(total_timesteps=100000)

    env.close()