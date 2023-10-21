Set-Location -Path ".\audio"

$url = Read-Host "Enter YouTube URL"

& yt-dlp $url -x --audio-format mp3

Set-Location -Path ".."

python -m venv run_env

.\run_env\Scripts\Activate

pip install openai-whisper torch==2.1.0+cu118 -f https://download.pytorch.org/whl/cu118/torch_stable.html

python .\main.py

deactivate

Remove-Item -Recurse -Force run_env

Set-Location -Path ".\audio"

Get-ChildItem | Remove-Item

Set-Location -Path ".."