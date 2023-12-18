import subprocess

def run_tests():
    subprocess.run(["pytest", "--cov=src", "--cov-report=html"])

if __name__ == "__main__":
    run_tests()
