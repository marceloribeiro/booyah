if [[ "$VIRTUAL_ENV" == "" ]]
then
    echo "Please run under a pyenv environment"
    exit
fi

if ! command -v pip &> /dev/null
then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi
gunicorn application
