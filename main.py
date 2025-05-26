from dotenv import load_dotenv
import os
from datetime import datetime
from utils import (
    record_audio_with_interrupt,
    validate_audio_file,
    reduce_noise,
    transcribe_with_speechmatics,
    extract_resume_info_using_llm,
    get_ai_greeting_message,
    speak_text,
    analyze_candidate_response_and_generate_new_question,
    load_content,
    save_interview_data,
    get_feedback_of_candidate_response,
    get_overall_evaluation_score,
)

load_dotenv()
MAX_QUESTIONS = 5


def record_and_transcribe(candidate_name, question_answer_number):
    # Create audio directory if it doesn't exist
    os.makedirs(f"audio/{candidate_name}", exist_ok=True)

    filename = f"audio/{candidate_name}/{candidate_name}_{question_answer_number}.wav"

    audio_file, fs = record_audio_with_interrupt(filename=filename)

    if not validate_audio_file(audio_file):
        print("Warning: Audio file seems invalid or too quiet")
        return "No valid audio recorded"

    audio_file = reduce_noise(audio_file, fs)

    if not validate_audio_file(audio_file):
        print("Warning: Audio file seems invalid after noise reduction")
        return "No valid audio after processing"

    transcript = transcribe_with_speechmatics(audio_file)
    return transcript


def start_interview_with_ai(
    name, resume_highlights, job_description, max_questions=MAX_QUESTIONS
):
    conversations = []
    question_answer_number = 1

    # Step 1: AI Greeting and first question
    print("Starting AI Interview...")
    ai_greeting_message = get_ai_greeting_message(name)
    speak_text(ai_greeting_message)

    # Step 2: Record and transcribe first response
    print("Please answer the question...")
    candidate_response = record_and_transcribe(name, question_answer_number)

    # Step 3: Analyze first response and generate next question
    next_question, feedback = analyze_candidate_response_and_generate_new_question(
        ai_greeting_message, candidate_response, job_description, resume_highlights
    )

    # Save first conversation
    first_conversation = {
        "Question": ai_greeting_message,
        "Candidate Answer": candidate_response,
        "Evaluation": feedback["score"],
        "Feedback": feedback["feedback"],
    }
    conversations.append(first_conversation)
    question_answer_number += 1

    # Step 4: Continue with remaining questions
    for i in range(max_questions):
        print(f"Question {i+2} of {max_questions + 1}")

        # Ask next question
        speak_text(next_question)

        # Record and transcribe response
        print("Please answer the question...")
        candidate_response = record_and_transcribe(name, question_answer_number)

        # Analyze response and generate next question (for next iteration)
        if i < max_questions - 1:  # Don't generate next question for last iteration
            next_question_temp, feedback = (
                analyze_candidate_response_and_generate_new_question(
                    next_question,
                    candidate_response,
                    job_description,
                    resume_highlights,
                )
            )
            next_question = next_question_temp
        else:
            # For last question, just get feedback
            feedback = get_feedback_of_candidate_response(
                next_question, candidate_response, job_description, resume_highlights
            )

        # Save conversation
        conversation = {
            "Question": next_question,
            "Candidate Answer": candidate_response,
            "Evaluation": feedback["score"],
            "Feedback": feedback["feedback"],
        }
        conversations.append(conversation)
        question_answer_number += 1

    # Step 5: Conclude interview
    closing_message = f"Thank you {name} for your time today. This concludes our interview. We will get back to you soon with the results. Have a great day!"
    print(closing_message)
    speak_text(closing_message)
    print("Interview completed!")

    return conversations


def app():
    print("=== AI Interview System ===")

    # Step 1: Load resume and job description
    print("Step 1: Loading resume and job description...")

    # Check if files exist
    resume_path = "inputs/resume.pdf"
    job_desc_path = "inputs/job_description.txt"

    if not os.path.exists(resume_path):
        print(f"Error: Resume file not found at {resume_path}")
        return

    if not os.path.exists(job_desc_path):
        print(f"Error: Job description file not found at {job_desc_path}")
        return

    resume_content = load_content(resume_path)
    job_description = load_content(job_desc_path)

    if not resume_content or not job_description:
        print("Error: Could not load resume or job description content")
        return

    # Step 2: Extract candidate information using LLM
    print("Step 2: Extracting candidate information...")
    name, resume_highlights = extract_resume_info_using_llm(resume_content)

    # Step 3: Get confirmation to start interview
    print(f"Step 3: Ready to interview {name}")
    start_interview = (
        input("Do you want to start the interview? (y/n): ").lower().strip() == "y"
    )

    if not start_interview:
        print("Interview cancelled.")
        return

    # Step 4: Conduct the interview
    print("Step 4: Starting interview...")
    conversations = start_interview_with_ai(name, resume_highlights, job_description)

    # Step 5: Calculate overall score and prepare final data
    print("Step 5: Calculating final results...")
    final_evaluation_score = get_overall_evaluation_score(conversations)

    # Step 6: Prepare final interview data according to JSON schema
    current_time = datetime.now().isoformat() + "Z"

    interview_data = {
        "name": name,
        "createdAt": current_time,
        "updatedAt": current_time,
        "id": 1,  # You might want to make this dynamic
        "job_description": job_description,
        "resume_highlights": resume_highlights,
        "conversations": conversations,
        "overall_score": round(final_evaluation_score, 2),
    }

    # Step 7: Save results
    print("Step 6: Saving results...")
    save_interview_data(interview_data, candidate_name=name)

    print(f"\n=== Interview Summary ===")
    print(f"Candidate: {name}")
    print(f"Total Questions: {len(conversations)}")
    print(f"Overall Score: {final_evaluation_score:.2f}/10")
    print("Interview data saved successfully!")


if __name__ == "__main__":
    app()
