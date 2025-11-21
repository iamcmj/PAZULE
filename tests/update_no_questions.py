import json
import random

def improve_no_questions(input_path, output_path):
    """
    Replaces 'NO' questions for each landmark with 'YES' questions from other landmarks
    to improve the dataset's distinctiveness.

    Args:
        input_path (str): Path to the original landmark_qa_labeled.json file.
        output_path (str): Path to save the updated landmark_qa_labeled_updated.json file.
    """
    # Load the original JSON data
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_landmarks = list(data.keys())
    updated_data = {}

    # Create a pool of all 'YES' questions from all landmarks
    all_yes_questions = []
    for landmark_name, qa_pairs in data.items():
        yes_questions = [qa[0] for qa in qa_pairs if qa[1] == 'yes']
        all_yes_questions.extend(yes_questions)
    
    # Remove duplicates to create a clean pool
    all_yes_questions = list(set(all_yes_questions))

    # Process each landmark
    for current_landmark in all_landmarks:
        # Keep the original 'YES' questions
        original_yes_questions = [qa for qa in data[current_landmark] if qa[1] == 'yes']
        
        # Create a pool of 'YES' questions from OTHER landmarks
        other_landmarks_yes_pool = []
        for other_landmark in all_landmarks:
            if other_landmark != current_landmark:
                yes_questions = [qa[0] for qa in data[other_landmark] if qa[1] == 'yes']
                other_landmarks_yes_pool.extend(yes_questions)
        
        # Remove duplicates
        other_landmarks_yes_pool = list(set(other_landmarks_yes_pool))

        # Randomly sample 20 questions for the new 'NO' questions
        # Ensure we don't pick a question that happens to be a 'YES' question for the current landmark
        current_yes_question_texts = [qa[0] for qa in original_yes_questions]
        
        candidate_pool = [q for q in other_landmarks_yes_pool if q not in current_yes_question_texts]

        # If the candidate pool is smaller than 20, we might have to allow some duplicates,
        # but for this dataset, it should be large enough.
        num_samples = min(20, len(candidate_pool))
        new_no_question_texts = random.sample(candidate_pool, num_samples)
        
        new_no_questions = [[text, 'no'] for text in new_no_question_texts]

        # Combine original 'YES' and new 'NO' questions
        updated_data[current_landmark] = original_yes_questions + new_no_questions

    # Save the updated data to a new file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully created updated QA file at: {output_path}")
    print(f"Total landmarks processed: {len(all_landmarks)}")

if __name__ == '__main__':
    # Define file paths
    input_file = r'C:\Users\Seongbeom\Desktop\데이콘 출판마을 프로젝트\github\data\landmark_qa_labeled.json'
    output_file = r'C:\Users\Seongbeom\Desktop\데이콘 출판마을 프로젝트\github\data\landmark_qa_labeled_updated.json'
    
    # Run the function
    improve_no_questions(input_file, output_file)
