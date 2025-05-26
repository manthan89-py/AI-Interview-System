from utils.llm_call import get_response_from_llm, parse_json_response
from utils.prompts import next_question_generation, feedback_generation


def get_next_question(
    previous_question, candidate_response, resume_highlights, job_description
):
    # Use LLM to generate next question
    final_prompt = next_question_generation.format(
        previous_question=previous_question,
        candidate_response=candidate_response,
        resume_highlights=resume_highlights,
        job_description=job_description,
    )
    response = get_response_from_llm(final_prompt)
    response = parse_json_response(response)
    next_question = response["next_question"]
    return next_question


def get_feedback_of_candidate_response(
    question, candidate_response, job_description, resume_highlights
):
    # Use LLM to generate feedback
    final_prompt = feedback_generation.format(
        question=question,
        candidate_response=candidate_response,
        job_description=job_description,
        resume_highlights=resume_highlights,
    )
    response = get_response_from_llm(final_prompt)
    response = parse_json_response(response)
    feedback = response["feedback"]
    score = response["score"]
    return {"feedback": feedback, "score": score}


def analyze_candidate_response_and_generate_new_question(
    question, candidate_response, job_description, resume_highlights
):
    # Get feedback for current response
    feedback = get_feedback_of_candidate_response(
        question, candidate_response, job_description, resume_highlights
    )

    # Generate next question
    next_question = get_next_question(
        question, candidate_response, resume_highlights, job_description
    )

    return next_question, feedback
