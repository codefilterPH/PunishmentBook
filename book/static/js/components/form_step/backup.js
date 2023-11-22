
    let showSlashIcon = false; // Variable to track if the slash icon should be shown

    function updateStepName(step) {
    const stepNames = [
        { name: "SELECT PERSONNEL", icon: '<i class="fas fa-briefcase"></i>' },
        { name: "ADD VIOLATIONS", icon: '<i class="fas fa-exclamation-triangle"></i>' },
        { name: "SELECT DATE & ENTER PLACE OF OMISSION", icon: '<i class="fa fa-ban"></i>' },
        { name: "ADD PUNISHMENTS", icon: '<i class="fa fa-balance-scale"></i>' },
        { name: "SELECT IMPOSED BY WHOM", icon: '<i class="fas fa-user"></i>' },
        { name: "DATE NOTICED ACCUSED", icon: '<i class="fa fa-calendar"></i>' },
    ];

    const stepNameElement = document.getElementById("stepNameSubmitOffense");

    // Check if the element exists
    if (stepNameElement) {
            try {
                const stepInfo = stepNames[step - 1];

                if (step === 2) {
                    if (showSlashIcon) {
                        // Show the forward slash icon on the second "Next" click
                        stepNameElement.innerHTML = `${stepInfo.icon} ${stepInfo.name} <i class="fas fa-slash"></i>`;
                    } else {
                        // Show just the step name and icon
                        stepNameElement.innerHTML = `${stepInfo.icon} ${stepInfo.name}`;
                        showSlashIcon = true;
                    }
                } else {
                    // Show the step name and icon for other steps
                    stepNameElement.innerHTML = `${stepInfo.icon} ${stepInfo.name}`;
                }
            } catch (error) {
                // Handle any errors here, e.g., display an error message to the user
                console.error(error);
                stepNameElement.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
            }
        }
    }

    let currentStep = 1;  // Start at the first step
    showStep(currentStep);

    function showStep(step) {
        updateStepName(step); // Update the step name when showing the step

        // Check if any elements with the class "form-step" exist
        const steps = document.querySelectorAll(".form-step");

        if (steps.length > 0) {
            steps.forEach((step) => step.style.display = "none");

            // Show the current step
            steps[step - 1].style.display = "block";

            // Update the current step
            currentStep = step;
        } else {
            console.error("No elements with the class 'form-step' found on this page.");
        }
    }
