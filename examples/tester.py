# Copyright 2025 EvoBandits
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class Study:
    def __init__(self, direction: int = 1):
        assert direction in (1, -1), "Direction must be 1 (minimize) or -1 (maximize)"
        self._direction = direction
        self._results = []

    def add_result(self, result: dict):
        self._results.append(result)

    @property
    def best_mean_reward(self):
        if not self._results:
            return None
        return max(self._results, key=lambda r: -self._direction * r["mean_reward"])[
            "mean_reward"
        ]

    @property
    def best_params(self):
        if not self._results:
            return None
        best_value = self.best_mean_reward
        # Return first match (stable) with best reward
        for r in self._results:
            if r["mean_reward"] == best_value:
                return r["params"]
        return None

    @property
    def best_trials(self):
        """Returns all trials with n_best == 1 (meaning they are top-ranked)."""
        return [r for r in self._results if r.get("n_best") == 1]


if __name__ == "__main__":
    study = Study(direction=1)  # -1 for maximization

    # Sample input results
    results = [
        {
            "mean_reward": 0.0,
            "num_pulls": 82,
            "params": {"number": [1, 1]},
            "n_best": 1,
        },
        {
            "mean_reward": 1.0,
            "num_pulls": 86,
            "params": {"number": [0, 0]},
            "n_best": 2,
        },
        {
            "mean_reward": 1.0,
            "num_pulls": 85,
            "params": {"number": [2, 4]},
            "n_best": 3,
        },
    ]

    for res in results:
        study.add_result(res)

    print("Best reward:", study.best_mean_reward)  # 1.0
    print("Best params:", study.best_params)  # {'number': [0, 0]}
    print("Best trials (n_best == 1):", study.best_trials)
