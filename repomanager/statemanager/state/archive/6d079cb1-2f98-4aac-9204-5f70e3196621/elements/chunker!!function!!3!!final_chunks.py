def final_chunks(edu_exp_element):
    education = edu_exp_element[0]
    experience = edu_exp_element[1]
    education_chunks = education.split('#')
    experience_chunks = experience.split('#')
    return education_chunks, experience_chunks
