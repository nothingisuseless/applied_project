import pandas as pd
import requests
import json
import subprocess
import random


def execute_shell_command(command):
    """
    Execute a shell command and return the output and error messages.

    :param command: The shell command to execute (string).
    :return: A tuple containing the command's output and error messages.
    """
    try:
        # Execute the shell command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Return the command's output and error messages
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

execute_shell_command('pip install tenacity')

from tenacity import retry, stop_after_attempt, wait_fixed

pd.options.display.max_colwidth = 100

def llm_langchain(string, prompt_type):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3.1",
        "prompt": string + " Use the template and write an " + prompt_type + ".",
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data.get("response", "").strip()
        return actual_response
    else:
        print("error:", response.status_code, response.text)
        return None

# Define the URL for sending messages
url = 'http://174.138.122.252:5000/receive_message'

# Retry logic for the POST request
@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def send_message_with_retry(message_data):
    """
    Send a POST request with retry logic.
    
    :param message_data: The JSON payload to send.
    :return: The response object.
    """
    response = requests.post(url, json=message_data)
    response.raise_for_status()  # Raise an error for bad status codes
    return response

# Read user input data
user_input = pd.read_csv('sample.csv', dtype='str', index_col=False)

# Filter required data
required_data = user_input[user_input['ingestion_time'] == user_input['ingestion_time'].max()]
required_category = required_data['categories'].to_string(index=False).strip()
required_sub_category = required_data['sub_categories'].to_string(index=False).strip()

# Create the prompt string
string = f"{required_sub_category} from a {required_category} "

if 'university' in required_category.lower():
    if 'iit-j' in required_sub_category.lower():
        #csv_templates = pd.read_csv('templates.csv', dtype='str')
        csv_templates = pd.read_excel('templates.xlsx', dtype='str')
        cnt = csv_templates['template'].count()
        
# Read student data
student_list_wth_header = pd.read_csv('IIT_Jammu_Students_Final.csv', dtype='str', index_col=None)

# Prepare output DataFrame
df_output = pd.DataFrame(columns=['To', 'Subject', 'Message'])

# Lists to store results
to_list = []
sub_list = []
msg_list = []

# Process each student
for row in student_list_wth_header.itertuples():
    
    randm = random.randint(0, cnt)
    prompt_gen = csv_templates['template'].iloc[randm]
    # Create input string for the AI model
    inp = (f"The name of the student is {row.Student_Name}. The student id is {row.Student_ID}. "
           f"The email id of the student is {row.Student_Personal_Gmail_ID}. Department of the student is {row.IIT_Jammu_Department}. "
           f"The name of the student's mentor is {row.Mentors_Name}. The department of the mentor is {row.Mentors_Department}. "
           f"The course name of the student is {row.Course_Name}. The student participated in {row.Cocurricular_Activities_Participated_Last_Year} "
           f"activities last year. The club name of the student is {row.Club_Name}. The public mobile number of the student is {row.Student_Mobile_Number}. "
           f"The public mobile number of the student's mentor is {row.Mentor_Mobile_Number}.")
    
    # Get the subject and message from the AI model
    email = llm_langchain(prompt_gen + inp, "email")
    email_var_list = email.split('\n')
    for iter in range(len(email_var_list)):
        
        if 'subject' in email_var_list[iter].lower():
            subject = email_var_list[iter]
            message = ','.join(email_var_list[iter+1:]).replace(',', '\n')
    

    # Append results to lists
    to_list.append(row.Student_Personal_Gmail_ID)
    sub_list.append(subject)
    msg_list.append(message)

    # Prepare message data for sending
    message_data = {"to": row.Student_Personal_Gmail_ID, "subject": subject, "message": message}
    
    # Send the POST request with retry logic
    response = send_message_with_retry(message_data)

# Create the output DataFrame
df_output["To"] = to_list
df_output["Subject"] = sub_list
df_output["Message"] = msg_list

# Save the output to a CSV file
df_output.to_csv('output.csv', index=False)

exit(0)
