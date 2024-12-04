function calculateE1RM(weight, reps, rpe) {
    function percentage(reps, rpe) {
        let x = (10.0 - rpe) + (reps - 1);
        if (x >= 16) return 0.0;
        let intersection = 2.92;
        if (x <= intersection) {
            let a = 0.347619, b = -4.60714, c = 99.9667;
            return a * x * x + b * x + c;
        }
        let m = -2.64249, b = 97.0955;
        return m * x + b;
    }
    let p = percentage(reps, rpe);
    return (weight / p) * 100;
}

document.querySelectorAll('#exercise-list .card select').forEach(select => {
    select.addEventListener('change', function () {
        let option = this.options[this.selectedIndex];
        let weight = parseFloat(option.value);
        let reps = parseInt(option.dataset.reps);
        let rpe = parseFloat(option.dataset.rpe);
        let e1rm = calculateE1RM(weight, reps, rpe);
        document.getElementById('e1rm-' + this.id.split('-')[1]).textContent = e1rm.toFixed(1);
    });
    select.dispatchEvent(new Event('change'));
});