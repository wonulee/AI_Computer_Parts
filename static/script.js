async function getRecommendation() {
    const budget = document.getElementById("budget").value;
    const purpose = document.getElementById("purpose").value;

    const response = await fetch(`/recommend?budget=${budget}&purpose=${purpose}`);
    const data = await response.json();

    document.getElementById("result").textContent = JSON.stringify(data, null, 2);
}
