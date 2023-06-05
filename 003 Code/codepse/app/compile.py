import os
import subprocess
import py_compile


def c_compile_code(code):
    file = open("user_code.c", "w")
    file.write(code)
    file.close()

    # 컴파일 명령어
    compile_command = "gcc -o executable user_code.c"

    # 컴파일 실행
    result = subprocess.run(
        compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )

    # 컴파일 결과에 따라 결과 반환
    if result.returncode == 0:
        output = subprocess.run(
            "./executable", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        output_str = output.stdout.decode("utf-8")
    else:
        output_str = result.stderr.decode("utf-8")

    os.remove("user_code.c")  # user_code.c 파일 삭제
    os.remove("executable")  # executable 파일 삭제

    return output_str


def python_run_code(code):
    file = open("user_code.py", "w")
    file.write(code)
    file.close()

    try:
        py_compile.compile("user_code.py", doraise=True)

        # Python 코드 실행
        run_result = subprocess.run(
            ["python", "user_code.py"], capture_output=True, text=True
        )

        # 출력 결과 또는 오류 메시지 반환
        output_str = run_result.stdout or run_result.stderr
    except py_compile.PyCompileError as e:
        output_str = str(e)

    os.remove("user_code.py")  # user_code.py 파일 삭제

    return output_str


def java_run_code(code):
    # Write the code to a file
    with open("UserProgram.java", "w") as file:
        file.write(code)

    # Compile the java code
    compile_result = subprocess.run(
        ["javac", "UserProgram.java"], text=True, capture_output=True
    )

    # If the compilation fails, return the error
    if compile_result.returncode != 0:
        os.remove("UserProgram.java")  # remove the .java file
        return compile_result.stderr

    # If the compilation is successful, run the java program
    run_result = subprocess.run(["java", "UserProgram"], text=True, capture_output=True)

    # Delete the .java and .class files
    os.remove("UserProgram.java")
    os.remove("UserProgram.class")

    # Return the output of the program
    return run_result.stdout


def grade_code(output_str, expected_output):
    if output_str.strip() == expected_output:
        return "정답입니다!"  # 정답인 경우
    else:
        return "오답입니다! ( ✋˙࿁˙ )"  # 오답인 경우