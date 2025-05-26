def get_overall_evaluation_score(conversations):
    if not conversations:
        return 0

    total_score = 0
    for conversation in conversations:
        total_score += conversation["Evaluation"]
    return total_score / len(conversations)
