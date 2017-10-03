from subprocess import Popen, PIPE


def run_cmd(cmd):
    components = []
    current_word = []
    in_quoted = False
    for char in cmd:
        if not in_quoted:
            if char == ' ':
                components.append(''.join(current_word))
                current_word = []
            elif char != '"':
                current_word.append(char)
        elif char != '"':
            current_word.append(char)
        if char == '"':
            in_quoted = not in_quoted
    components.append(''.join(current_word))
    p = Popen(components, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    return p.communicate()[0]
