#!/usr/bin/env python3

import subprocess
import sys


def test_dynamic_query(query):
    """Test the main.py with a specific query"""
    try:
        # Run main.py with the query as input
        process = subprocess.Popen(
            ["uv", "run", "python", "main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        try:
            stdout, stderr = process.communicate(input=query + "\n", timeout=60)
        except subprocess.TimeoutExpired:
            print("❌ TIMEOUT - Process took too long")
            process.kill()
            return

        print(f"Query: {query}")
        print(f"Exit code: {process.returncode}")

        if process.returncode == 0:
            print("✅ SUCCESS")
            # Check if tools were used
            if "Tool calls made:" in stdout and "Tool calls made: 0" not in stdout:
                print("✅ TOOLS WERE USED")
            else:
                print("❌ NO TOOLS USED")

            print("Output:")
            print(stdout)
        else:
            print("❌ FAILED")
            print("STDERR:", stderr)
            print("STDOUT:", stdout)

    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT - Process took too long")
        process.kill()
    except Exception as e:
        print(f"❌ ERROR: {e}")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    print("Testing Dynamic Query Tool Usage")
    print("=" * 80)

    test_queries = [
        "What is the capital of France?",
        "What are the latest AI developments?",
        "Tell me about climate change",
    ]

    for query in test_queries:
        test_dynamic_query(query)
