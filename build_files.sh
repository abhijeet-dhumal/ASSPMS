echo "============> INSTALLING REQUIREMENTS <==============="
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "============> REQUIREMENTS INSTALLED <===============" 

echo "============> COLLECTING STATIC FILES <==============="
python3.9 manage.py collectstatic --noinput --clear
echo "============> STATIC FILES COLLECTED <==============="

echo "============> MAKE-MIGRATIONS <==============="
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput
echo "============> MAKE-MIGRATIONS-END <==============="
