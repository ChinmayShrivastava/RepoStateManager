def create_cot(data):
    for i in data:
        education_text = ''
        data[i]['exp_chunks_mod'] = [None] * len(data[i]['exp_chunks'])
        for j in range(len(data[i]['edu_chunks'])):
            i_ = f'{i}'
            j_ = int(j)
            education_text += f'{data[i_]["edu_chunks"][j_]}\n'
        prompt_pre = COT_GEN_PROMPT.replace('<<EDUCATION>>', education_text)
        for j in range(len(data[i]['exp_chunks'])):
            message = {
                "role": "user",
                "content": prompt_pre.replace('<<ENTRY>>', data[i]['exp_chunks'][int(j)])
            }
            threadid = create_thread([message]).id
            runid = run_assistant(AGENT_ID, threadid).id
            while True:
                time.sleep(2)
                run = get_run(runid, threadid)
                if run.status == 'completed':
                    break
            response = get_response(threadid)
            last_message = response.data[0].content[0].text.value
            data[i]['exp_chunks_mod'][j] = last_message
            print(last_message)
