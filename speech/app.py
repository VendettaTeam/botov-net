import subprocess
import uuid

from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    voice = request.form.get("voice")
    message = request.form.get("message")

    supported_voices = ['anna', 'alan', 'aleksandr', 'anatol', 'azamat', 'elena', 'irina',
                        'natalia', 'natia', 'nazgul', 'spomenka', 'talgat']

    if message is None or voice not in supported_voices:
        return Response("message is empty or voice not in array" , status=500)

    uniq_str = str(uuid.uuid4()) + '.wav'
    audio_path = '/usr/share/RHVoice-data/' + uniq_str

    try:
        shell_command = "echo '{}' | RHVoice-test -o {} -p {}".format(message, audio_path, voice)
        process = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            return Response(uniq_str, status=200)

        return Response(str(process.returncode), status=500)
    except Exception as ex:
        return Response(str(ex), status=500)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
