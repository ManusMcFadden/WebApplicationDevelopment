document.addEventListener('DOMContentLoaded', function () {
    const exerciseInput = document.getElementById('exercise');
    const workoutHiddenInput = document.getElementById('workout'); // Hidden form field
    const suggestionsContainer = document.getElementById('exercise-suggestions');

    // Show suggestions when the user types
    exerciseInput.addEventListener('input', function () {
        const query = this.value;

        // Clear suggestions if the input is empty
        if (!query) {
            suggestionsContainer.innerHTML = ''; // Clear suggestions
            suggestionsContainer.classList.remove('show'); // Hide the dropdown
            return;
        }

        fetch(`/suggest_exercises?q=${query}`)
            .then(response => response.json())
            .then(data => {
                console.log("Suggestions fetched:", data);  // Debugging line

                // Clear old suggestions
                suggestionsContainer.innerHTML = '';

                // Populate suggestions
                data.suggestions.forEach(suggestion => {
                    const item = document.createElement('a');  // Use <a> for compatibility with Bootstrap
                    item.className = 'dropdown-item';
                    item.href = '#';
                    item.textContent = suggestion;

                    // Handle click event for suggestion
                    item.addEventListener('click', function () {
                        exerciseInput.value = suggestion; // Set input value
                        workoutHiddenInput.value = suggestion; // Update the hidden field
                        suggestionsContainer.innerHTML = ''; // Hide suggestions
                        suggestionsContainer.classList.remove('show'); // Hide the dropdown
                        loadExerciseDetails(suggestion);
                    });

                    suggestionsContainer.appendChild(item);
                });

                // Show the suggestions dropdown after populating it
                suggestionsContainer.classList.add('show');  // Add the 'show' class to display it
            })
            .catch(error => console.error('Error fetching suggestions:', error));
    });

    // Fetch and display exercise details when a suggestion is selected
    // Fetch and display exercise details when a suggestion is selected
function loadExerciseDetails(exerciseName) {
    fetch(`/get_exercise/${exerciseName}`)
        .then(response => response.json())
        .then(data => {
            console.log("Exercise details fetched:", data);  // Debugging line
            if (data.error) {
                console.error(data.error);
                return;
            }

            // Update exercise details in the UI
            document.getElementById('muscle').textContent = `Muscle: ${data.muscle}`;
            document.getElementById('equipment').textContent = `Equipment: ${data.equipment}`;

            // Update iframe for embedding YouTube video
            const videoIframe = document.getElementById('video');
            if (data.video_url) {
                // Convert YouTube watch URL to embed URL if necessary
                const embedUrl = data.video_url.replace('watch?v=', 'embed/');
                videoIframe.src = embedUrl;
                videoIframe.style.display = 'block'; // Ensure iframe is visible
            } else {
                videoIframe.src = ''; // Clear iframe source if no video is available
                videoIframe.style.display = 'none'; // Hide iframe
            }
        })
        .catch(error => console.error('Error fetching exercise details:', error));
}

});