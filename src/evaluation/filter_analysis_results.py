import os
import subprocess
import time

def execute_command_with_deadline(command, deadline=60):
    """
    Run a command with a specific deadline.
    :param command: Command to be run.
    :param deadline: Duration (in seconds) before the command is forced to stop.
    :return: Standard output and error from the executed command.
    """
    process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    start = time.time()

    while True:
        if process.poll() is not None:
            break
        if deadline and (time.time() - start) > deadline:
            process.terminate()
            return 'TIMEOUT', 'TIMEOUT'
        time.sleep(1)

    stdout, stderr = process.communicate()
    return stdout, stderr


def analyze_java_with_pmd():
    """
    Execute PMD on Java files to detect code smells and save the results.
    """
    code_directory = "path/to/data/results/code/java/"
    report_directory = "path/to/data/results/reports/java/pmd/"

    if not os.path.exists(report_directory):
        os.makedirs(report_directory)

    for java_file in os.listdir(code_directory):
        path = code_directory + java_file
        output_path = report_directory + java_file + ".txt"
        os.system(f"pmd check -d {path} -R rulesets/java/all.xml -f text -r {output_path}")

def analyze_java_with_checkstyle():
    """
    Analyze Java files using Checkstyle and append the results to text files.
    """
    code_directory = "path/to/data/results/code/java/"
    report_directory = "path/to/data/results/reports/java/checkstyle/"

    if not os.path.exists(report_directory):
        os.makedirs(report_directory)

    for java_file in os.listdir(code_directory):
        if java_file.endswith(".java"):
            path = code_directory + java_file
            result_path = report_directory + java_file + ".txt"
            output, error = execute_command_with_deadline(
                ["java", "-jar", "checkstyle/checkstyle-10.9.3-all.jar", "-c", "checkstyle/sun_checks.xml", path],
                deadline=10
            )
            with open(result_path, "a") as result_file:
                result_file.write(str(output))

if __name__ == "__main__":
    analyze_python_files()
    analyze_python_with_flake8()
    analyze_java_with_pmd()
    analyze_java_with_checkstyle()
