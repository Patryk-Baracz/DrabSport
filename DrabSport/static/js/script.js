const apihost = 'http://0.0.0.0.:8000';


function apiListExerciseHistory() {
    return fetch(
        apihost + '/api_exercisehistory/exercisehistory/',
    ).then(
        function (resp) {
            if (!resp.ok) {
                alert('Wystąpił błąd! Otwórz devtools i zakładkę Sieć/Network, i poszukaj przyczyny');
            }
            return resp.json();
        }
    );
}

function renderExercise(exId, exUser, exReps, exWeight, exDate, exExercise) {
    console.log('id =', exId);
    console.log('user = ', exUser);
    console.log('reps = ', exReps);
    console.log('weight = ', exWeight);
    console.log('date = ', exDate);
    console.log('exercise = ', exExercise)
}

document.addEventListener('DOMContentLoaded', () => {
    apiListExerciseHistory().then(
         (response) => {
            response.forEach(
                (exercise) => {
                    renderExercise(exercise.id, exercise.user, exercise.total_reps, exercise.weight, exercise.date, exercise.exercise)
                }
            );
        }
    );
});


BURP
try except suspissious operations
connector do bazy
mokup local settingsy