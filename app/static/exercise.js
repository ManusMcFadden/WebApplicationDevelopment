document.addEventListener('DOMContentLoaded', function () {
    const exerciseInput = document.getElementById('exercise');
    const workoutHiddenInput = document.getElementById('workout');
    const suggestionsContainer = document.getElementById('exercise-suggestions');

    exerciseInput.addEventListener('input', function () {
        const query = this.value;

        if (!query) {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.classList.remove('show');
            return;
        }

        fetch(`/suggest_exercises?q=${query}`)
            .then(response => response.json())
            .then(data => {

                suggestionsContainer.innerHTML = '';

                data.suggestions.forEach(suggestion => {
                    const item = document.createElement('a');
                    item.className = 'dropdown-item';
                    item.href = '#';
                    item.textContent = suggestion;

                    item.addEventListener('click', function () {
                        exerciseInput.value = suggestion;
                        workoutHiddenInput.value = suggestion;
                        suggestionsContainer.innerHTML = '';
                        suggestionsContainer.classList.remove('show');
                        loadExerciseDetails(suggestion);
                    });

                    suggestionsContainer.appendChild(item);
                });

                
                suggestionsContainer.classList.add('show');
            })
            .catch(error => console.error('Error fetching suggestions:', error));
    });

    function loadExerciseDetails(exerciseName) {
    fetch(`/get_exercise/${exerciseName}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            document.getElementById('muscle').textContent = `Muscle: ${data.muscle}`;
            document.getElementById('equipment').textContent = `Equipment: ${data.equipment}`;

            const videoIframe = document.getElementById('video');
            if (data.video_url) {
                const embedUrl = data.video_url.replace('watch?v=', 'embed/');
                videoIframe.src = embedUrl;
                videoIframe.style.display = 'block';
            } else {
                videoIframe.src = '';
                videoIframe.style.display = 'none';
            }
        })
        .catch(error => console.error('Error fetching exercise details:', error));
    }

});