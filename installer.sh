DIR="pycraft"
URL="https://github.com/NinIcaty/pycraft"
INP="D"
PKG=("ursina pygame" )
if command -v python3 >/dev/null 2>&1; then
    if [ -d "$DIR" ]; then
        echo "Please delete or rename the Directory $DIR"
        read -p "Delete(D) or Exit(E/Default)" INP
        exit 1
        #broken:(
        : '
        if [["$INP"="D"]]; then
            echo Deleting $DIR
            rm -f -r $DIR
            echo Deleted $DIR
            #Starting Install
            echo "Continuing..."
            echo Starting install
            git clone $URL
            echo Cloned repo
            cd $DIR
            python -m venv .venv
            echo Venv Created
            source .venv/bin/activate
            echo Activated


        else
            exit 1
        fi
        '
    else
        echo 'Starting install'
        git clone $URL
        echo 'Cloned repo'
        cd $DIR
        python -m venv .venv
        echo 'Venv Created'
        source .venv/bin/activate
        echo 'Activated'

    fi
else
    echo "Python 3 is not installed,Please install it."
fi
#In the venv
python --version
echo "Packages that will be installed are:"
for i in ${!myArray[@]}; do
  echo "${myArray[$i]}"
done
echo Installing packages
pip install $PKG
echo "Packages that have been succesfully innstalled are:"
pip list
echo 'To re-activate the venv run the command "source .venv/bin/activate"'
