"""
Retraining Strategy:
- Run weekly or daily (cron / scheduler)
- Rebuild embeddings for new articles
- Rebuild FAISS index
"""

import subprocess

def main():
    print("Rebuilding embeddings...")
    subprocess.run(["python", "build_embeddings.py"])

    print("Rebuilding FAISS index...")
    subprocess.run(["python", "build_index.py"])

    print("Retraining complete.")

if __name__ == "__main__":
    main()
