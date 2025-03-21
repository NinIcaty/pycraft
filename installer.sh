exh Starting Download
if command -v python3 >/dev/null 2>&1; then
    echo Starting install
    git clone https://github.com/NinIcaty/pycraft
    echo Cloned repo
    cd pycraft
    python -m venv venv
    echo Venv Created
    source venv/bin/activate
    echo Activated


else
    echo "Python 3 is not installed,Please install it."
fi

python --version
pip  install ursina

