# __main__.py in the taskmux package

import argparse
from .config_reader import read_config
from .tmux_manager import create_session, run_commands, generate_commands
import subprocess
import threading
import os
from flask import Flask, request

app = Flask(__name__)

# Example global state to track job statuses
job_statuses = {}

@app.route('/report', methods=['POST'])
def report_status():
    data = request.json
    job_statuses[data['job_name']] = data['status']
    print(f"Job {data['job_name']} reported status: {data['status']}")
    return {"message": "Status updated"}, 200

def start_api_server():
    app.run(port=5000, debug=False)

def main():
    parser = argparse.ArgumentParser(description="TMUX session manager with monitoring and restart capabilities.")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration YAML file.")
    parser.add_argument("--monitor", action="store_true", help="Enable real-time monitoring of tasks.")
    args = parser.parse_args()

    config = read_config(args.config)
    session_names = [job['name'] for job in config.get('jobs', [])]

    if args.monitor:
        # Start the API server in a separate thread
        api_server_thread = threading.Thread(target=start_api_server, daemon=True)
        api_server_thread.start()
        print("API server started for monitoring.")

    api_url = "http://localhost:5000/report" if args.monitor else ""

    for job in config.get('jobs', []):
        session_name = job['name']
        create_session(session_name)
        index = 0
        for command_template in job.get('commands', []):
            commands = generate_commands(command_template, job)
            # Pass API URL to run_commands for client communication
            run_commands(session_name, commands, index, api_url)
            index += len(commands)

    if args.monitor:
        api_server_thread.join()

if __name__ == '__main__':
    main()
