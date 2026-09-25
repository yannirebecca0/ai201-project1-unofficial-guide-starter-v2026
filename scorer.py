def judge(question, expects, answer, results):
    if not expects:
        return False

    return expects.lower() in answer.lower()