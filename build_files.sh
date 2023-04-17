echo "============> INSTALLING REQUIREMENTS <==============="
pip install -r requirements.txt
echo "============> REQUIREMENTS INSTALLED <===============" 

echo "============> COLLECTING STATIC FILES <==============="
python3.9 manage.py collectstatic --noinput --clear
echo "============> STATIC FILES COLLECTED <==============="

echo "============> MAKE-MIGRATIONS <==============="
python3.9 manage.py makemigartions --noinput
python3.9 manage.py migrate --noinput
echo "============> MAKE-MIGRATIONS-END <==============="
