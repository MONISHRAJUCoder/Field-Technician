"""Small test harness to run `vision.detect_issue` with verbose output.

Usage:
    python scripts/test_detection.py path/to/image.jpg
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vision.vision import detect_issue


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_detection.py path/to/image.jpg")
        sys.exit(2)

    image = sys.argv[1]
    print("Env: HF token present?", bool(os.getenv("HF_API_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")))
    print("Env: QWEN_ENDPOINT present?", bool(os.getenv("QWEN_ENDPOINT")))

    # Call detect_issue with verbose True by passing through YOLO verbose flag via kwargs
    # detect_issue will prefer LLaVA or QWEN endpoints according to env vars
    result = detect_issue(image)
    print("Result:", result)


if __name__ == "__main__":
    main()
