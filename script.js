document.getElementById("submit-btn").addEventListener("click", function () {
    let markdown = "# Quiz Answers\n\n";

    // Define the questions with their labels
    const questions = [
        { name: "cause", label: "### 1. What cause matters most to you?" },
        { name: "groups", label: "### 2. Do you prefer to help specific groups?" }
        // Include additional questions as needed
    ];

    // Loop through each question and build the markdown string from selected answers
    questions.forEach(question => {
        let selectedOptions = document.querySelectorAll(`input[name="${question.name}"]:checked`);
        let selectedValues = Array.from(selectedOptions)
            .map(option => `- ${option.value}`)
            .join("\n");

        markdown += `${question.label}\n${selectedValues || "- No answer selected"}\n\n`;
    });

    // Show the generated markdown in the results container
    document.getElementById("results").textContent = markdown;
    document.getElementById("results-container").style.display = "block";

    // IMPORTANT: Change the URL below to your deployed backend's domain.
    fetch('https://your-backend-domain.com/api/charity-match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quiz_markdown: markdown })
    })
    .then(response => response.json())
    .then(data => {
        // Append the backend response to the results container
        console.log('API response:', data);
        document.getElementById("results").textContent += "\n\nCharity Matches:\n" + JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("results").textContent += "\n\nError calling the backend API.";
    });
});
