from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import re

app = Flask(__name__)

# 音频文件夹路径
AUDIO_FOLDER = 'audio_files'
@app.route('/')
def index():
    audio_files = [f for f in os.listdir('audio_files') if f.endswith('.mp3')]  # 替换为你的音频文件夹
    audio_files.sort(key=lambda f: int(re.search(r'\d+', f).group()))  # 提取数字进行排序
    return render_template('index.html', audio_files=audio_files)

@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)


@app.route('/rename', methods=['POST'])
def rename_file():
    old_filename = request.form['old_filename']
    new_filename = request.form['new_filename']

    # 仅更改文件名，不更改后缀名
    if new_filename and old_filename:
        old_filepath = os.path.join('audio_files', old_filename)  # 完整路径
        new_filepath = os.path.join('audio_files', new_filename + '.mp3')  # 保持后缀名为 .mp3

        try:
            os.rename(old_filepath, new_filepath)
            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)  # 确保使用的端口与 start.py 中一致