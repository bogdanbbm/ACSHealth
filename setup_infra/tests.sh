
if [ $@ < 2 ]
then
    echo "Not enough arguements: use tests.sh <what_to_test> <email>"
    exit
fi
echo $1

if [ "$1" = "reviews" ]
then
    curl -X POST -H 'Content-Type: application/json' localhost:5000/register -d '{"email":"ciubotaruion195@gmail.com", "username":"ceva1", "pass_hash":"de la", "is_medic":1}'
    curl -X POST -H 'Content-Type: application/json' localhost:5000/register -d '{"email":"ciubotaruion195@gmail.com", "username":"ceva2", "pass_hash":"de la", "is_medic":1}'
    curl -X POST -H "Content-type:application/json" localhost:5000/medic_reviews/ceva1 -d '{"review": "O mizerie"}'
fi