const runEmotionAnalysis = async () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const systemResponse = document.getElementById("system_response");
    const submitButton = document.getElementById("analyzeButton");
    const query = new URLSearchParams({ textToAnalyze });

    systemResponse.textContent = "Analyzing...";
    systemResponse.classList.remove("text-danger");
    submitButton.disabled = true;

    try {
        const response = await fetch(`/emotionDetector?${query.toString()}`);
        const message = await response.text();

        systemResponse.textContent = message;
        systemResponse.classList.toggle("text-danger", !response.ok);
    } catch (error) {
        systemResponse.textContent = "Could not contact the server. Please try again.";
        systemResponse.classList.add("text-danger");
    } finally {
        submitButton.disabled = false;
    }
};

document.getElementById("analyzeButton").addEventListener("click", runEmotionAnalysis);
