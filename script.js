document.getElementById("submit-btn").addEventListener("click", function () {
    let markdown = "# Quiz Answers\n\n";

    const questions = [
        { name: "cause", label: "### 1. What cause matters most to you?" },
        { name: "groups", label: "### 2. Do you prefer to help specific groups?" },
        { name: "region", label: "### 3. Do you want to focus on a specific region?" },
        { name: "faith", label: "### 4. Do you prefer faith-based charities?" },
        { name: "support", label: "### 5. Would you rather support urgent relief or long-term change?" }
    ];

    questions.forEach(question => {
        let selectedOptions = document.querySelectorAll(`input[name="${question.name}"]:checked`);
        let selectedValues = Array.from(selectedOptions)
            .map(option => `- ${option.value}`)
            .join("\n");

        if (!selectedValues) {
            let radioOption = document.querySelector(`input[name="${question.name}"]:checked`);
            if (radioOption) selectedValues = `- ${radioOption.value}`;
        }

        markdown += `${question.label}\n${selectedValues || "- No answer selected"}\n\n`;
    });

    // Display the generated markdown for reference
    document.getElementById("results").textContent = markdown;
    document.getElementById("results-container").style.display = "block";

    // Send the quiz markdown to the backend API endpoint
    fetch('/api/charity-match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quiz_markdown: markdown })
    })
    .then(response => response.json())
    .then(data => {
        // Process and display the Together API response (assuming response contains charity names)
        console.log('API response:', data);
        document.getElementById("results").textContent += "\n\nCharity Matches:\n" + JSON.stringify(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
