import sys, json
from client import AgentSyntheticTrajectoryEvaluator

def main():
    evaluator = AgentSyntheticTrajectoryEvaluator()
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        try:
            req = json.loads(line)
            method = req.get("method")
            rid = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "evaluate_trajectory", "description": "Evaluate trajectory.", "inputSchema": {"type": "object", "properties": {"agent_actions": {"type": "array"}, "reference_actions": {"type": "array"}}, "required": ["agent_actions", "reference_actions"]}},
                        {"name": "run_benchmark_trajectory_evaluator", "description": "Run self-test.", "inputSchema": {"type": "object"}}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "evaluate_trajectory":
                    out = evaluator.evaluate_trajectory(args.get("agent_actions", []), args.get("reference_actions", []))
                elif tname == "run_benchmark_trajectory_evaluator":
                    out = evaluator.run_benchmark_trajectory_evaluator()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
