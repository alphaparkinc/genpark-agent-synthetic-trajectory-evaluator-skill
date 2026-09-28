from client import AgentSyntheticTrajectoryEvaluator
import json

def main():
    evaluator = AgentSyntheticTrajectoryEvaluator()
    res = evaluator.run_benchmark_trajectory_evaluator()
    print("Trajectory Evaluator Benchmark Result:")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
