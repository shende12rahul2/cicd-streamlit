import subprocess
import pickle

user_input = input()

subprocess.check_output(user_input, shell=True)
pickle.loads(user_input.encode())
eval(user_input)
