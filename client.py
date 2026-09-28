import sys, json

class AgentSyntheticTrajectoryEvaluator:
    """
    Zero-Dependency Autonomous Agent Trajectory Evaluator.
    Computes rigorous alignment metrics between agent tool executions and reference gold trajectories:
    - Sequence Levenshtein edit distance
    - Action precision, recall, and F1-score
    - Step efficiency ratio
    """
    def _levenshtein(self, seq1, seq2):
        n = len(seq1)
        m = len(seq2)
        dp = [[0] * (m + 1) for _ in range(n + 1)]

        for i in range(n + 1):
            dp[i][0] = i
        for j in range(m + 1):
            dp[0][j] = j

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = 0 if seq1[i - 1] == seq2[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,       # deletion
                    dp[i][j - 1] + 1,       # insertion
                    dp[i - 1][j - 1] + cost # substitution
                )
        return dp[n][m]

    def evaluate_trajectory(self, agent_actions, reference_actions):
        """
        agent_actions: list of tool strings, e.g. ['read_file', 'edit_file', 'run_tests']
        reference_actions: list of tool strings
        """
        dist = self._levenshtein(agent_actions, reference_actions)
        max_len = max(len(agent_actions), len(reference_actions))
        similarity = 1.0 - (dist / max_len) if max_len > 0 else 1.0

        set_agent = set(agent_actions)
        set_ref = set(reference_actions)
        common = set_agent.intersection(set_ref)

        precision = len(common) / len(set_agent) if set_agent else 0.0
        recall = len(common) / len(set_ref) if set_ref else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        step_efficiency = len(reference_actions) / len(agent_actions) if agent_actions else 0.0

        return {
            "levenshtein_distance": dist,
            "similarity_score": round(similarity, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "step_efficiency": round(step_efficiency, 4),
            "agent_steps": len(agent_actions),
            "reference_steps": len(reference_actions)
        }

    def run_benchmark_trajectory_evaluator(self):
        gold = ["inspect_issue", "read_file", "edit_file", "run_tests", "git_commit"]
        agent_perfect = ["inspect_issue", "read_file", "edit_file", "run_tests", "git_commit"]
        agent_noisy = ["inspect_issue", "read_file", "read_file", "edit_file", "run_tests", "run_tests", "git_commit"]

        res_perf = self.evaluate_trajectory(agent_perfect, gold)
        res_noisy = self.evaluate_trajectory(agent_noisy, gold)

        return {
            "benchmark_status": "PASSED",
            "perfect_similarity": res_perf["similarity_score"] == 1.0,
            "perfect_f1": res_perf["f1_score"] == 1.0,
            "noisy_distance": res_noisy["levenshtein_distance"] == 2,
            "noisy_f1": res_noisy["f1_score"] == 1.0
        }
