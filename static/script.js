async function getRecommendation() {
    const budget = document.getElementById("budget").value;
    const purpose = document.getElementById("purpose").value;
    const result = document.getElementById("result");

    const response = await fetch(`/search?budget=${budget}&purpose=${purpose}`);
    const data = await response.json();

    result.textContent = JSON.stringify(data, null, 2);
}